# external imports
from datetime import datetime
from sqlalchemy.orm import joinedload, selectinload
from typing import Optional

# internal imports
from .database_provider import DatabaseProvider
from .ip_address_provider import IPAddressProvider

from ..data_models.data_models_conversor import DataModelsConversor
from ..data_models.hunter_models.track_model import TrackModel
from ..data_models.hunter_models.traceroute_model import TracerouteModel
from ..data_models.database_models import (
    TrackDBModel,
    MeasurementDBModel,
    TracerouteDBModel,
    TracerouteHopDBModel,
    HopResponseDBModel,
    PingDBModel
)
from ..utilities.enums import (
    TrackStatus, DefinitionTypeRIPEMeasurementRequest
)
from ..utilities.constants import (
    TRACK_STATUS_IN_PROGRESS_DESCRIPTION
)


class TracksProvider(DatabaseProvider):
    def __init__(self):
        super().__init__()

    def create_new_track(
            self,
            ip_address: str,
            slim: bool,
            check_if_anycast: bool) -> TrackModel:

        ip_address_provider = IPAddressProvider()
        track_db_model = TrackDBModel(
            timestamp=datetime.now(),
            status=TrackStatus.IN_PROGRESS.value,
            status_description=TRACK_STATUS_IN_PROGRESS_DESCRIPTION,
            slim=slim,
            ip_address=ip_address
        )

        if ip_address_provider.is_address_in_db(ip_address):
            track_added = self.add(track_db_model)
        else:
            ip_address_provider.add_new_ip_address(
                ip_address=ip_address,
                check_if_anycast=check_if_anycast
            )
            track_added = self.add(track_db_model)

        return DataModelsConversor.track_to_hunter_model(track_added)

    def mark_track_with_error(self, track_id: int):
        track_db = self.get_by_id(model_class=TrackDBModel, obj_id=track_id)
        track_db.status = TrackStatus.ERROR.value
        self.update(track_db)

    def get_track_with_relations(self, track_id: int) -> Optional[TrackModel]:
        """
        Obtains a track with all its relations charged as a TrackModel

        Args:
            track_id: ID of the track to search

        Returns:
            TrackModel with all the relations or None if not found
        """
        # try:
        with self.get_session() as session:
            track_db = session.query(TrackDBModel).options(
                # load tracks results
                selectinload(TrackDBModel.tracks_results),
                # load traceroute measurements
                selectinload(TrackDBModel.measurements)
                .selectinload(MeasurementDBModel.traceroutes)
                .selectinload(TracerouteDBModel.traceroutes_hops)
                .selectinload(TracerouteHopDBModel.hops_responses),
                #load ping measurements
                selectinload(TrackDBModel.measurements)
                .selectinload(MeasurementDBModel.pings)
            ).filter(TrackDBModel.id == track_id).first()

            if track_db:
                # Convert to TrackModel
                # Basic attributes parsing
                track_model = DataModelsConversor.track_to_hunter_model(
                    track_db_model=track_db
                )

                # track results parsing
                # TODO

                # measurements parsing
                for measurement_db_model in track_db.measurements:
                    measurement = DataModelsConversor.measurement_to_hunter_model(
                        measurement_db_model=measurement_db_model
                    )

                    # ping parsing
                    if measurement.type == DefinitionTypeRIPEMeasurementRequest.PING:
                        # TODO
                        pass

                    # traceroute parsing
                    if measurement.type == DefinitionTypeRIPEMeasurementRequest.TRACEROUTE:
                        for traceroute_db_model in measurement_db_model.traceroutes:
                            traceroute_hunter_model = self.parsing_traceroute_with_all_relations(
                                traceroute_db_model=traceroute_db_model,
                            )

                            measurement.results.append(traceroute_hunter_model)

                    track_model.measurements.append(measurement)

                return track_model

            return None

        # except Exception as e:
        #     print(f"Error getting track with relations for ID {track_id}: {e}")
        #     return None

    def parsing_traceroute_with_all_relations(self, traceroute_db_model: TracerouteDBModel) -> TracerouteModel:
        traceroute_hunter_model = DataModelsConversor.traceroute_to_hunter_model(
            traceroute_db_model=traceroute_db_model
        )

        for traceroute_hop_db_model in traceroute_db_model.traceroutes_hops:
            traceroute_hop_hunter_model = DataModelsConversor.traceroute_hop_to_hunter_model(
                traceroute_hop_db_model=traceroute_hop_db_model,
            )

            for hop_response_db_model in traceroute_hop_db_model.hops_responses:
                traceroute_hop_hunter_model.hop_responses.append(
                    DataModelsConversor.hop_response_to_hunter_model(
                        hop_response_db_model=hop_response_db_model
                    )
                )

            traceroute_hunter_model.hops.append(traceroute_hop_hunter_model)

        return traceroute_hunter_model
