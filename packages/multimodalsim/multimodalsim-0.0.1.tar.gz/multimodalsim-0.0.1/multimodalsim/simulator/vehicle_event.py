import logging
import copy
from typing import Optional

from multimodalsim.simulator.event import Event, ActionEvent
import multimodalsim.simulator.vehicle as vehicle_module
import multimodalsim.simulator.request as request
from multimodalsim.state_machine.status import VehicleStatus, PassengerStatus

import multimodalsim.simulator.optimization_event \
    as optimization_event
import multimodalsim.simulator.passenger_event \
    as passenger_event
import multimodalsim.simulator.environment as environment
import multimodalsim.simulator.event_queue as event_queue

logger = logging.getLogger(__name__)


class VehicleReady(Event):
    def __init__(self, vehicle: vehicle_module.Vehicle,
                 route: vehicle_module.Route,
                 queue: 'event_queue.EventQueue',
                 update_position_time_step: Optional[float] = None) -> None:
        super().__init__('VehicleReady', queue, vehicle.release_time)
        self.__vehicle = vehicle
        self.__route = route
        self.__update_position_time_step = update_position_time_step

    @property
    def vehicle(self) -> 'vehicle_module.Vehicle':
        return self.__vehicle

    def _process(self, env: 'environment.Environment') -> str:
        env.add_vehicle(self.__vehicle)

        if self.__route is None:
            self.__route = vehicle_module.Route(
                self.__vehicle)

        env.add_route(self.__route, self.__vehicle.id)

        VehicleWaiting(self.__route, self.queue).add_to_queue()

        if env.coordinates is not None and self.__update_position_time_step \
                is not None:
            self.__vehicle.polylines = \
                env.coordinates.update_polylines(self.__route)
            VehicleUpdatePositionEvent(
                self.__vehicle, self.queue,
                self.time + self.__update_position_time_step,
                self.__update_position_time_step).add_to_queue()
        elif env.coordinates is not None:
            self.__vehicle.polylines = \
                env.coordinates.update_polylines(self.__route)

        return 'Vehicle Ready process is implemented'


class VehicleWaiting(ActionEvent):
    def __init__(
            self, route: vehicle_module.Route,
            queue: 'event_queue.EventQueue',
            time: Optional[float] = None) -> None:
        time = time if time is not None else queue.env.current_time
        super().__init__('VehicleWaiting', queue, time,
                         state_machine=route.vehicle.state_machine,
                         event_priority=Event.LOW_PRIORITY)
        self.__route = route

    def _process(self, env: 'environment.Environment') -> str:

        optimization_event.Optimize(env.current_time, self.queue). \
            add_to_queue()

        if len(self.__route.requests_to_pickup()) > 0:
            # Passengers to board
            VehicleBoarding(self.__route, self.queue).add_to_queue()
            if self.__route.current_stop.departure_time > env.current_time:
                VehicleWaiting(
                    self.__route, self.queue,
                    self.__route.current_stop.departure_time).add_to_queue()
        elif len(self.__route.next_stops) > 0:
            # No passengers to board
            if self.__route.current_stop.departure_time > env.current_time:
                VehicleWaiting(
                    self.__route, self.queue,
                    self.__route.current_stop.departure_time).add_to_queue()
            else:
                VehicleDeparture(self.__route, self.queue).add_to_queue()
        else:
            # No next stops for now. If the route of the vehicle is not
            # modified, its status will remain IDLE until Vehicle.end_time,
            # at which point the VehicleComplete event will be processed.
            VehicleComplete(self.__route, self.queue).add_to_queue()

        return 'Vehicle Waiting process is implemented'

    def add_to_queue(self) -> None:
        # Before adding the event, cancel all priorly added VehicleWaiting
        # events associated with the vehicle since they have now become
        # obsolete.
        self.queue.cancel_event_type(self.__class__, time=None,
                                     owner=self.__route.vehicle)

        super().add_to_queue()


class VehicleBoarding(ActionEvent):
    def __init__(self, route: vehicle_module.Route,
                 queue: 'event_queue.EventQueue') -> None:
        super().__init__('VehicleBoarding', queue,
                         queue.env.current_time,
                         state_machine=route.vehicle.state_machine,
                         event_priority=Event.LOW_PRIORITY)
        self.__route = route

    def _process(self, env: 'environment.Environment') -> str:
        passengers_to_board_copy = self.__route.current_stop. \
            passengers_to_board.copy()

        passengers_ready = [trip for trip in passengers_to_board_copy
                            if trip.status == PassengerStatus.READY]

        for req in passengers_ready:
            self.__route.initiate_boarding(req)
            passenger_event.PassengerToBoard(
                req, self.queue).add_to_queue()

        return 'Vehicle Boarding process is implemented'


class VehicleDeparture(ActionEvent):
    def __init__(self, route: vehicle_module.Route,
                 queue: 'event_queue.EventQueue') -> None:
        super().__init__('Vehicle Departure', queue,
                         route.current_stop.departure_time,
                         state_machine=route.vehicle.state_machine
                         )
        self.__route = route

    def _process(self, env: 'environment.Environment') -> str:

        if env.travel_times is not None:
            from_stop = copy.deepcopy(self.__route.current_stop)
            to_stop = copy.deepcopy(self.__route.next_stops[0])
            vehicle = copy.deepcopy(self.__route.vehicle)
            actual_arrival_time = env.travel_times.get_expected_arrival_time(
                from_stop, to_stop, vehicle)
        else:
            actual_arrival_time = self.__route.next_stops[0].arrival_time

        self.__route.depart()

        VehicleArrival(self.__route, self.queue,
                       actual_arrival_time).add_to_queue()

        return 'Vehicle Departure process is implemented'


class VehicleArrival(ActionEvent):
    def __init__(self, route: vehicle_module.Route,
                 queue: 'event_queue.EventQueue',
                 arrival_time: float) -> None:
        super().__init__('VehicleArrival', queue, arrival_time,
                         state_machine=route.vehicle.state_machine)
        self.__route = route

    def _process(self, env: 'environment.Environment') -> str:

        self.__update_stop_times(env.current_time)

        self.__route.arrive()

        if len(self.__route.next_stops) == 0 \
                and not self.__route.vehicle.reusable:
            VehicleComplete(self.__route, self.queue,
                            self.queue.env.current_time).add_to_queue(
                forced_insertion=True)

        passengers_to_alight_copy = self.__route.current_stop. \
            passengers_to_alight.copy()
        for trip in passengers_to_alight_copy:
            if trip.current_leg in self.__route.onboard_legs:
                self.__route.initiate_alighting(trip)
                passenger_event.PassengerAlighting(
                    trip, self.queue).add_to_queue()

        if len(passengers_to_alight_copy) == 0:
            VehicleWaiting(self.__route, self.queue).add_to_queue()

        return 'Vehicle Arrival process is implemented'

    def __update_stop_times(self, arrival_time):

        planned_arrival_time = self.__route.next_stops[0].arrival_time
        delta_time = arrival_time - planned_arrival_time

        for stop in self.__route.next_stops:
            stop.arrival_time += delta_time
            if stop.min_departure_time is None:
                new_departure_time = stop.departure_time + delta_time
            else:
                new_departure_time = max(stop.departure_time + delta_time,
                                         stop.min_departure_time)
            delta_time = new_departure_time - stop.departure_time
            stop.departure_time = new_departure_time


class VehicleNotification(Event):
    def __init__(self, route_update: vehicle_module.RouteUpdate,
                 queue: 'event_queue.EventQueue') -> None:
        self.__env = None
        self.__route_update = route_update
        self.__vehicle = queue.env.get_vehicle_by_id(
            self.__route_update.vehicle_id)
        self.__route = queue.env.get_route_by_vehicle_id(self.__vehicle.id)
        super().__init__('VehicleNotification', queue)

    def _process(self, env: 'environment.Environment') -> str:

        self.__env = env

        if self.__route_update.next_stops is not None:
            self.__route.next_stops = \
                copy.deepcopy(self.__route_update.next_stops)
            for stop in self.__route.next_stops:
                self.__update_stop_with_actual_trips(stop)

        if self.__route_update.current_stop_modified_passengers_to_board \
                is not None:
            # Modify passengers_to_board of current_stop according to the
            # results of the optimization.
            actual_modified_passengers_to_board = \
                self.__replace_copy_trips_with_actual_trips(
                    self.__route_update.
                    current_stop_modified_passengers_to_board)
            self.__route.current_stop.passengers_to_board = \
                actual_modified_passengers_to_board

        if self.__route_update.current_stop_departure_time is not None \
                and self.__route.current_stop is not None:
            # If self.__route.current_stop.departure_time is equal to
            # env.current_time, then the vehicle may have already left the
            # current stop. In this case self.__route.current_stop should
            # be None (because optimization should not modify current stops
            # when departure time is close to current time), and we do not
            # modify it.
            if self.__route.current_stop.departure_time \
                    != self.__route_update.current_stop_departure_time:
                self.__route.current_stop.departure_time \
                    = self.__route_update.current_stop_departure_time
                VehicleWaiting(self.__route, self.queue).add_to_queue()

        if self.__route_update.modified_assigned_legs is not None:
            # Add the assigned legs that were modified by optimization and
            # that are not already present in self.__route.assigned_legs.
            actual_modified_assigned_legs = \
                self.__replace_copy_legs_with_actual_legs(
                    self.__route_update.modified_assigned_legs)
            for leg in actual_modified_assigned_legs:
                if leg not in self.__route.assigned_legs:
                    self.__route.assigned_legs.append(leg)

        # Update polylines
        if env.coordinates is not None:
            self.__vehicle.polylines = \
                env.coordinates.update_polylines(self.__route)

        return 'Notify Vehicle process is implemented'

    def __update_stop_with_actual_trips(self, stop):

        stop.passengers_to_board = self.__replace_copy_trips_with_actual_trips(
            stop.passengers_to_board)
        stop.boarding_passengers = self.__replace_copy_trips_with_actual_trips(
            stop.boarding_passengers)
        stop.boarded_passengers = self.__replace_copy_trips_with_actual_trips(
            stop.boarded_passengers)
        stop.passengers_to_alight = self \
            .__replace_copy_trips_with_actual_trips(stop.passengers_to_alight)

    def __replace_copy_trips_with_actual_trips(self, trips_list):

        return list(self.__env.get_trip_by_id(req.id) for req in trips_list)

    def __replace_copy_legs_with_actual_legs(self, legs_list):

        return list(self.__env.get_leg_by_id(leg.id) for leg in legs_list)


class VehicleBoarded(Event):
    def __init__(self, trip: 'request.Trip',
                 queue: 'event_queue.EventQueue') -> None:
        self.__trip = trip
        self.__route = queue.env.get_route_by_vehicle_id(
            self.__trip.current_leg.assigned_vehicle.id)
        super().__init__('VehicleBoarded', queue)

    def _process(self, env: 'environment.Environment') -> str:
        self.__route.board(self.__trip)

        if len(self.__route.current_stop.boarding_passengers) == 0:
            # All passengers are on board
            VehicleWaiting(self.__route, self.queue).add_to_queue()
            # Else we wait until all the boarding passengers are on board
            # before creating the event VehicleWaiting.
        elif len(self.__route.requests_to_pickup()) > 0:
            # Passengers to board
            VehicleBoarding(self.__route, self.queue).add_to_queue()

        return 'Vehicle Boarded process is implemented'


class VehicleAlighted(Event):
    def __init__(self, leg: 'request.Leg',
                 queue: 'event_queue.EventQueue') -> None:
        self.__leg = leg
        self.__route = leg.assigned_vehicle
        self.__route = queue.env.get_route_by_vehicle_id(
            leg.assigned_vehicle.id)
        super().__init__('VehicleAlighted', queue)

    def _process(self, env: 'environment.Environment') -> str:
        self.__route.alight(self.__leg)

        if len(self.__route.current_stop.alighting_passengers) == 0:
            # All passengers are alighted
            VehicleWaiting(self.__route, self.queue).add_to_queue()
            # Else we wait until all the passengers on board are alighted
            # before creating the event VehicleWaiting.

        return 'Vehicle Alighted process is implemented'


class VehicleUpdatePositionEvent(Event):
    def __init__(self, vehicle: vehicle_module.Vehicle,
                 queue: 'event_queue.EventQueue', event_time: float,
                 time_step: Optional[float] = None):
        super().__init__("VehicleUpdatePositionEvent", queue, event_time)

        self.__vehicle = vehicle
        self.__route = queue.env.get_route_by_vehicle_id(vehicle.id)
        self.__event_time = event_time
        self.__queue = queue
        self.__time_step = time_step

    @property
    def time_step(self) -> float:
        return self.__time_step

    def _process(self, env: 'environment.Environment') -> str:
        self.__vehicle.position = env.coordinates.update_position(
            self.__vehicle, self.__route, self.__event_time)

        time_step = env.simulation_config.update_position_time_step

        if self.__vehicle.status != VehicleStatus.COMPLETE \
                and time_step is not None:
            VehicleUpdatePositionEvent(self.__vehicle, self.__queue,
                                       self.__event_time + time_step,
                                       time_step).add_to_queue()

        return 'VehicleUpdatePositionEvent processed'

    @property
    def vehicle(self) -> vehicle_module.Vehicle:
        return self.__vehicle


class VehicleComplete(ActionEvent):
    def __init__(self, route: vehicle_module.Route,
                 queue: 'event_queue.EventQueue',
                 event_time: Optional[float] = None):
        if event_time is None:
            event_time = max(route.vehicle.end_time, queue.env.current_time)
        super().__init__('VehicleComplete', queue, event_time,
                         state_machine=route.vehicle.state_machine,
                         event_priority=Event.VERY_LOW_PRIORITY)
        self.__route = route

    def _process(self, env: 'environment.Environment') -> str:

        return 'Vehicle Complete process is implemented'

    def add_to_queue(self, forced_insertion: bool = False) -> None:
        if not self.queue.is_event_type_in_queue(self.__class__,
                                                 owner=self.__route.vehicle) \
                or forced_insertion:
            super().add_to_queue()
