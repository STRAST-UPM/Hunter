#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# external imports
import requests
import json
import time
import random
from shapely import (
    Point,
    Polygon,
    from_geojson
)
# internal imports
from src.utils.custom_exceptions import (
    RequestSubmissionError
)
from src.utils.common_functions import (
    json_file_to_dict
)
from src.utils.constants import (
    RIPE_ATLAS_PROBES_BASE_URL,
    RIPE_ATLAS_MEASUREMENTS_BASE_URL,
    KEY_FILEPATH,
    TRACEROUTE_PROTOCOL
)


class RIPEAtlas:
    def __init__(self):
        self._ripe_atlas_api_key = ""
        self.charge_ripe_atlas_api_key()
        self._ripe_measurement_request_data = {}

    @property
    def measurement_request_data(self):
        return self._ripe_measurement_request_data.copy()

    def charge_ripe_atlas_api_key(self):
        self._ripe_atlas_api_key = json_file_to_dict(KEY_FILEPATH)["key"]

    def make_ripe_measurement(
            self,
            target: str,
            description: str,
            type_measurement_list: list[str],
            probes_id_list: list[str],
            domain_name: str = "",
    ) -> dict:

        self.build_petition_data_structure(
            target=target,
            description=description,
            type_measurement_list=type_measurement_list,
            probes_id_list=probes_id_list,
            domain_name=domain_name,
        )
        url = (f"{RIPE_ATLAS_MEASUREMENTS_BASE_URL}"
               f"?key={self._ripe_atlas_api_key}")
        try:
            results = requests.post(
                url,
                json=self._ripe_measurement_request_data).json()
        except requests.HTTPError as e:
            raise RequestSubmissionError(
                "Status %s, reason \"%s\"" % (e.code, e.read())
            )

        if "error" in results:
            print("Waiting 30 seconds to repeat measurement request because "
                  "there was an error")
            print(results)
            time.sleep(30)
            self.make_ripe_measurement(
                target=target,
                description=description,
                type_measurement_list=type_measurement_list,
                probes_id_list=probes_id_list,
                domain_name=domain_name
            )

        return results

    def get_measurement_results(
            self,
            measurement_id: int,
            delay: int,
            attempts_max: int = -1,
            probes_can_fail: int = 0) -> list:
        results_measurement_url = (
            f"{RIPE_ATLAS_MEASUREMENTS_BASE_URL}"
            f"{measurement_id}/results/"
        )
        print(f"Getting results of measurement id {measurement_id}")
        probes_scheduled = self.get_probes_scheduled(measurement_id)
        attempts = 0

        while True:
            print(f"Wait {delay} seconds. Number of attempts: {attempts}")
            time.sleep(delay)
            attempts += 1
            results = requests.get(results_measurement_url).json()

            if len(results) >= probes_scheduled - probes_can_fail:
                print("Results retrieved")
                break
            elif attempts > attempts_max > 0:
                print("Maximum attempts reached. Retrieved latest results")
                print(f"Probes scheduled: {probes_scheduled}. "
                      f"Number of results {len(results)}")
                break
            # 4 is the id for Stopped status of measurement
            elif self.is_measurement_stopped(measurement_id):
                print("Measurement stop. Retrieved results")
                print(f"Probes scheduled: {probes_scheduled}. "
                      f"Number of results {len(results)}")
                break
            else:
                continue
        return results

    def is_measurement_stopped(self, measurement_id: int) -> bool:
        results_measurement_url = (
            f"{RIPE_ATLAS_MEASUREMENTS_BASE_URL}"
            f"{measurement_id}/"
        )
        response = requests.get(results_measurement_url).json()

        if response["status"]["id"] == 4:
            return True
        else:
            return False

    def get_probes_scheduled(self, measurement_id: int) -> int:
        probes_scheduled_url = (f"{RIPE_ATLAS_MEASUREMENTS_BASE_URL}"
                                f"{measurement_id}/?fields=probes_scheduled")
        retrieved = False
        while not retrieved:
            time.sleep(2)
            try:
                response = requests.get(probes_scheduled_url).json()
                return int(response["probes_scheduled"])
            except:
                print("Measure not scheduled yet")

    def get_probes(self, measurement_id: int) -> list[dict]:
        probes_scheduled_url = (f"{RIPE_ATLAS_MEASUREMENTS_BASE_URL}"
                                f"{measurement_id}/?fields=probes")
        retrieved = False
        while not retrieved:
            time.sleep(2)
            try:
                response = requests.get(probes_scheduled_url).json()
                return response["probes"]
            except:
                print("Measure not scheduled yet")

    def build_petition_data_structure(
            self,
            target: str,
            description: str,
            type_measurement_list: list[str],
            probes_id_list: list[str],
            domain_name: str,
    ):
        definitions = []
        for type_measurement in type_measurement_list:
            if ":" in target:
                af = 6
            else:
                af = 4
            definition = {
                "target": target,
                "description": f"{description} {type_measurement}",
                "type": type_measurement,
                "is_oneoff": True,
                "af": af
            }
            if type_measurement == "dns":
                definition["resolve_on_probe"] = True
                definition["query_argument"] = domain_name
                definition["query_type"] = "A"
                definition["query_class"] = "IN"
                definition["use_probe_resolver"] = True
                del definition["target"]
            elif type_measurement == "traceroute":
                definition["protocol"] = TRACEROUTE_PROTOCOL

            definitions.append(definition)

        self._ripe_measurement_request_data["definitions"] = definitions
        self._ripe_measurement_request_data["probes"] = (
            self.get_probes_id_list_data_petition(probes_id_list))

    def get_probes_id_list_data_petition(
            self, probes_id_list: list[str]) -> list[dict]:
        probes_data = [{
            "requested": len(probes_id_list),
            "type": "probes",
            "value": ",".join(map(str, probes_id_list))
        }]
        return probes_data

    # Maybe static functions
    def get_usable_probes_in_area(
            self, area: Polygon, in_countries: list) -> list:
        probes = self.get_probes_in_area(area=area, in_countries=in_countries)
        probes_usables = filter(
            lambda probe:
            self.is_probe_usable(probe=probe, in_countries=in_countries),
            probes["results"])
        return list(probes_usables)

    def get_usable_probes_in_radius(
            self, origin: Point,
            radius_km: float,
            min_probes: int,
            in_countries: list) -> list:
        probes = self.get_probes_in_radius(
            origin=origin, radius_km=radius_km, in_countries=in_countries
        )

        probes_usables = filter(
            lambda probe:
            self.is_probe_usable(probe=probe, in_countries=in_countries),
            probes["results"])
        probes_usables = list(probes_usables)

        if len(probes_usables) < min_probes:
            return self.get_usable_probes_in_radius(
                origin=origin,
                radius_km=radius_km + 10,
                min_probes=min_probes,
                in_countries=in_countries
            )
        probes_usables = random.sample(probes_usables, min_probes)
        probes_usables = [probe["id"] for probe in probes_usables]
        return probes_usables

    def get_probes_in_area(self, area: Polygon, in_countries: list) -> dict:
        lon, lat = area.exterior.coords.xy
        probes_box_filter = (f"longitude__gte={min(lon)}&"
                             f"longitude__lte={max(lon)}&"
                             f"latitude__gte={min(lat)}&"
                             f"latitude__lte={max(lat)}")
        probes_fields_filter = "fields=id,geometry,country_code"
        probes_connected_filter = "status_name=Connected"
        if len(in_countries) != 0:
            probes_in_country = ",".join(in_countries)
        else:
            probes_in_country = ""
        petition_url = (RIPE_ATLAS_PROBES_BASE_URL +
                        f"?{probes_box_filter}"
                        f"&{probes_fields_filter}"
                        f"&{probes_connected_filter}"
                        f"&{probes_in_country}")
        return requests.get(url=petition_url).json()

    def get_probes_in_radius(
            self,
            origin: Point,
            radius_km: float,
            in_countries: list) -> dict:
        lon = origin.x
        lat = origin.y
        probes_radius_filter = f"radius={lat},{lon}:{radius_km}"
        probes_fields_filter = "fields=id,geometry,country_code"
        probes_connected_filter = "status_name=Connected"
        if len(in_countries) != 0:
            probes_in_country = ",".join(in_countries)
        else:
            probes_in_country = ""
        petition_url = (RIPE_ATLAS_PROBES_BASE_URL +
                        f"?{probes_radius_filter}"
                        f"&{probes_fields_filter}"
                        f"&{probes_connected_filter}"
                        f"&{probes_in_country}")
        return requests.get(url=petition_url).json()

    def get_probe_by_id(self, probe_id: int) -> dict:
        petition_url = (RIPE_ATLAS_PROBES_BASE_URL +
                        f"/{probe_id}")
        return requests.get(url=petition_url).json()

    def is_probe_usable(self, probe: dict, in_countries: list) -> bool:
        # Establish condition of country in
        if len(in_countries) != 0:
            if "country_code" in probe.keys():
                probe_country = probe["country_code"]
            else:
                probe_country = ""
            in_valid_country = (probe_country in in_countries)
        else:
            in_valid_country = True

        return in_valid_country

    def is_probe_inside_area(self, probe: dict, area: Polygon) -> bool:
        probe_location = from_geojson(json.dumps(probe["geometry"]))
        return area.contains(probe_location)
