import json
from typing import Optional

import networkx as nx
from geopy import distance

from multimodalsim.config.request_generator_config \
    import RequestsGeneratorConfig
from multimodalsim.reader.requests_generator import CAPFormatter


class AvailableConnectionsExtractor:
    def __init__(
            self, cap_file_path: str, stop_times_file_path: str,
            config: Optional[str | RequestsGeneratorConfig] = None) -> None:

        self.__load_config(config)

        self.__cap_formatter = CAPFormatter(cap_file_path,
                                            stop_times_file_path, config)

        self.__max_connection_time = config.max_connection_time
        self.__available_connections = None

    def extract_available_connections(self, max_distance: float) -> list[list]:
        formatted_cap_df = \
            self.__cap_formatter.format_cap(self.__max_connection_time)

        cap_wit_lags_df = self.__add_lags_to_cap(formatted_cap_df)
        connections_different_stops_df = \
            self.__get_connections_with_different_stops_df(cap_wit_lags_df)

        connections_connected_components = \
            self.__get_stop_connections_connected_components(
                connections_different_stops_df, max_distance)

        self.__available_connections = [sorted(list(c)) for c in
                                        connections_connected_components]

        return self.__available_connections

    def save_to_json(self, available_connections_file_path: str) -> None:
        if self.__available_connections is None:
            raise ValueError("Available connections must be extracted first!")

        with open(available_connections_file_path, 'w') as f:
            json.dump(self.__available_connections, f)

    def __load_config(self, config):
        if isinstance(config, str):
            config = RequestsGeneratorConfig(config)
        elif not isinstance(config, RequestsGeneratorConfig):
            config = RequestsGeneratorConfig()

        self.__max_connection_time = config.max_connection_time
        self.__id_col = config.id_col
        self.__arrival_time_col = config.arrival_time_col
        self.__boarding_time_col = config.boarding_time_col
        self.__origin_stop_id_col = config.origin_stop_id_col
        self.__destination_stop_id_col = config.destination_stop_id_col
        self.__boarding_type_col = config.boarding_type_col
        self.__origin_stop_lat_col = config.origin_stop_lat_col
        self.__origin_stop_lon_col = config.origin_stop_lon_col
        self.__destination_stop_lat_col = config.destination_stop_lat_col
        self.__destination_stop_lon_col = config.destination_stop_lon_col

    def __add_lags_to_cap(self, formatted_cap_df):
        cap_columns = [self.__id_col, self.__origin_stop_id_col,
                       self.__destination_stop_id_col,
                       self.__boarding_time_col,
                       self.__arrival_time_col, "boarding_type",
                       self.__origin_stop_lat_col, self.__origin_stop_lon_col,
                       self.__destination_stop_lat_col,
                       self.__destination_stop_lon_col]
        cap_with_lags_df = \
            formatted_cap_df.sort_values(
                [self.__id_col, self.__boarding_time_col])[
                cap_columns].dropna()

        cap_with_lags_df["origin_stop_coord"] = list(
            zip(cap_with_lags_df[self.__origin_stop_lat_col],
                cap_with_lags_df[self.__origin_stop_lon_col]))
        cap_with_lags_df["destination_stop_coord"] = list(
            zip(cap_with_lags_df[self.__destination_stop_lat_col],
                cap_with_lags_df[self.__destination_stop_lon_col]))

        cap_grouped_by_id_client_columns = cap_with_lags_df.groupby(
            self.__id_col)

        cap_with_lags_df["destination_stop_id_lag"] = \
            cap_grouped_by_id_client_columns[
                self.__destination_stop_id_col].shift(1)
        cap_with_lags_df["destination_stop_coord_lag"] = \
            cap_grouped_by_id_client_columns["destination_stop_coord"].shift(1)

        return cap_with_lags_df

    def __get_connections_with_different_stops_df(self, cap_with_lags_df):
        connections_columns = ["boarding_type", self.__origin_stop_id_col,
                               "destination_stop_id_lag", "origin_stop_coord",
                               "destination_stop_coord_lag"]
        connections_df = cap_with_lags_df[
            cap_with_lags_df["boarding_type"] == "Correspondance"][
            connections_columns]
        connections_different_stops_df = connections_df[
            connections_df[self.__origin_stop_id_col] != connections_df[
                "destination_stop_id_lag"]].dropna()

        return connections_different_stops_df

    def __get_stop_connections_connected_components(
            self, connections_different_stops_df, max_distance):
        connections_different_stops_df[
            "stops_distance"] = connections_different_stops_df.apply(
            lambda x: distance.distance(
                x["origin_stop_coord"], x["destination_stop_coord_lag"]).km,
            axis=1)

        connections_different_stops_max_dist_df = \
            connections_different_stops_df[
                connections_different_stops_df[
                    "stops_distance"] < max_distance]

        stop_connections_graph = nx.Graph()

        connections_different_stops_max_dist_df.apply(
            lambda x: stop_connections_graph.add_edge(
                int(x[self.__origin_stop_id_col]),
                int(x["destination_stop_id_lag"])), axis=1)
        connections_connected_components = sorted(
            nx.connected_components(stop_connections_graph), key=len,
            reverse=True)

        return connections_connected_components
