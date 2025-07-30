import copy
from typing import Optional
import multimodalsim.simulator.request as request


class Stop:
    """A stop is located somewhere along the network.  New requests
    arrive at the stop.
    ----------
    arrival_time: float
        Date and time at which the vehicle arrives the stop
    departure_time: float
        Date and time at which the vehicle leaves the stop
    min_departure_time: float
        Minimum time at which the vehicle is allowed to leave the stop
    cumulative_distance: float
        Cumulative distance travelled by the vehicle when arriving at the stop
    passengers_to_board: list of Trip objects
        list of passengers who need to board
    boarding_passengers: list of Trip objects
        list of passengers who are boarding
    boarded_passengers: list of Trip objects
        list of passengers who are already boarded
    passengers_to_alight: list of Trip objects
        list of passengers to alight
        OLD: list of passengers who are alighted
    alighted_passengers: list of Trip objects
        list of passengers who are alighted
    location: Location
        Object of type Location referring to the location of the stop
        (e.g., GPS coordinates)
    capacity: int
        The maximal number of passengers that can wait at the stop.
    tags: list[str]
            List of tags associated with the stop.
    """

    def __init__(self, arrival_time: float, departure_time: float,
                 location: 'LabelLocation',
                 cumulative_distance: Optional[float] = None,
                 min_departure_time: Optional[float] = None,
                 capacity: Optional[int] = None,
                 tags: Optional[list[str]] = None) -> None:
        super().__init__()

        self.__arrival_time = arrival_time
        self.__departure_time = departure_time
        self.__min_departure_time = min_departure_time
        self.__passengers_to_board = []
        self.__boarding_passengers = []
        self.__boarded_passengers = []
        self.__passengers_to_alight = []
        self.__alighting_passengers = []
        self.__alighted_passengers = []
        self.__location = location
        self.__cumulative_distance = cumulative_distance
        self.__capacity = capacity
        self.__tags = [] if tags is None else tags

    def __str__(self) -> str:
        class_string = str(self.__class__) + ": {"
        for attribute, value in self.__dict__.items():
            if "__passengers_to_board" in attribute:
                class_string += str(attribute) + ": " \
                                + str(list(str(x.id) for x in value)) + ", "
            elif "__boarding_passengers" in attribute:
                class_string += str(attribute) + ": " \
                                + str(list(str(x.id) for x in value)) + ", "
            elif "__boarded_passengers" in attribute:
                class_string += str(attribute) + ": " \
                                + str(list(str(x.id) for x in value)) + ", "
            elif "__passengers_to_alight" in attribute:
                class_string += str(attribute) + ": " \
                                + str(list(str(x.id) for x in value)) + ", "
            elif "alighting_passengers" in attribute:
                class_string += str(attribute) + ": " \
                                + str(list(str(x.id) for x in value)) + ", "
            elif "alighted_passengers" in attribute:
                class_string += str(attribute) + ": " \
                                + str(list(str(x.id) for x in value)) + ", "
            else:
                class_string += str(attribute) + ": " + str(value) + ", "

        class_string += "}"

        return class_string

    @property
    def arrival_time(self) -> float:
        return self.__arrival_time

    @arrival_time.setter
    def arrival_time(self, arrival_time: float):
        self.__arrival_time = arrival_time

    @property
    def departure_time(self) -> float:
        return self.__departure_time

    @departure_time.setter
    def departure_time(self, departure_time: float):
        if self.__min_departure_time is not None \
                and departure_time < self.__min_departure_time:
            raise ValueError(
                "departure_time ({}) must be greater than or  equal to "
                "min_departure_time ({}).".format(departure_time,
                                                  self.__min_departure_time))
        self.__departure_time = departure_time

    @property
    def min_departure_time(self) -> float:
        return self.__min_departure_time

    @property
    def passengers_to_board(self) -> list['request.Trip']:
        return self.__passengers_to_board

    @passengers_to_board.setter
    def passengers_to_board(self, passengers_to_board: list['request.Trip']):
        self.__passengers_to_board = passengers_to_board

    @property
    def boarding_passengers(self) -> list['request.Trip']:
        return self.__boarding_passengers

    @boarding_passengers.setter
    def boarding_passengers(self, boarding_passengers: list['request.Trip']):
        self.__boarding_passengers = boarding_passengers

    @property
    def boarded_passengers(self) -> list['request.Trip']:
        return self.__boarded_passengers

    @boarded_passengers.setter
    def boarded_passengers(self, boarded_passengers: list['request.Trip']):
        self.__boarded_passengers = boarded_passengers

    @property
    def passengers_to_alight(self) -> list['request.Trip']:
        return self.__passengers_to_alight

    @passengers_to_alight.setter
    def passengers_to_alight(self, passengers_to_alight: list['request.Trip']):
        self.__passengers_to_alight = passengers_to_alight

    @property
    def alighting_passengers(self) -> list['request.Trip']:
        return self.__alighting_passengers

    @property
    def alighted_passengers(self) -> list['request.Trip']:
        return self.__alighted_passengers

    @property
    def location(self) -> 'LabelLocation':
        return self.__location

    @property
    def cumulative_distance(self) -> Optional[float]:
        return self.__cumulative_distance

    @property
    def capacity(self) -> Optional[int]:
        return self.__capacity

    @property
    def tags(self) -> list[str]:
        return self.__tags

    def initiate_boarding(self, trip: 'request.Trip'):
        """Passengers who are ready to be picked up in the stop get in the
        vehicle """
        self.passengers_to_board.remove(trip)
        self.boarding_passengers.append(trip)

    def board(self, trip: 'request.Trip'):
        """Passenger who is boarding becomes boarded"""
        self.boarding_passengers.remove(trip)
        self.boarded_passengers.append(trip)

    def initiate_alighting(self, trip: 'request.Trip'):
        """Passengers who reached their stop leave the vehicle"""
        self.passengers_to_alight.remove(trip)
        self.alighting_passengers.append(trip)

    def alight(self, trip: 'request.Trip'):
        """Passenger who is alighting becomes alighted"""
        self.alighting_passengers.remove(trip)
        self.alighted_passengers.append(trip)

    def __deepcopy__(self, memo: dict) -> 'Stop':
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k == "_Stop__alighted_passengers":
                setattr(result, k, [])
            elif k == "_Stop__alighting_passengers":
                setattr(result, k, [])
            elif k == "_Stop__boarded_passengers":
                setattr(result, k, [])
            elif k == "_Stop__boarding_passengers":
                setattr(result, k, [])
            else:
                setattr(result, k, copy.deepcopy(v, memo))
        return result


class Location:
    """The ``Location`` class is a base class that mostly serves as a
    structure for storing basic information about the location of a vehicle
    or a passenger (i.e., Request). """

    def __init__(self, lon: Optional[float] = None,
                 lat: Optional[float] = None) -> None:
        self.lon = lon
        self.lat = lat

    def __eq__(self, other: 'Location') -> bool:
        pass


class LabelLocation(Location):
    def __init__(self, label: str, lon: Optional[float] = None,
                 lat: Optional[float] = None) -> None:
        super().__init__(lon, lat)
        self.label = label

    def __str__(self) -> str:

        if self.lon is not None or self.lat is not None:
            ret_str = "{}: ({},{})".format(self.label, self.lon, self.lat)
        else:
            ret_str = "{}".format(self.label)

        return ret_str

    def __eq__(self, other: 'LabelLocation') -> bool:
        if isinstance(other, LabelLocation):
            return self.label == other.label
        return False

    def __deepcopy__(self, memo: dict) -> 'LabelLocation':
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result


class TimeCoordinatesLocation(Location):
    def __init__(self, time: float, lon: float, lat: float) -> None:
        super().__init__(lon, lat)
        self.time = time

    def __str__(self) -> str:
        return "{}: ({},{})".format(self.time, self.lon, self.lat)

    def __eq__(self, other) -> bool:
        if isinstance(other, TimeCoordinatesLocation):
            return self.time == other.time and self.lon == other.lon \
                   and self.lat == other.lat
        return False

    def __deepcopy__(self, memo: dict) -> 'TimeCoordinatesLocation':
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result
