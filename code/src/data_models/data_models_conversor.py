# external imports

# internal imports

from .database_models import (
    TrackDBModel,
    TrackResultDBModel,
    MeasurementDBModel,
    TracerouteDBModel,
    TracerouteHopDBModel,
    HopResponseDBModel,
    PingDBModel
)

from .hunter_models.track_model import TrackModel
from .hunter_models.track_result_model import TrackResultModel
from .hunter_models.measurement_model import MeasurementModel
from .hunter_models.traceroute_model import TracerouteModel
from .hunter_models.traceroute_hop_model import TracerouteHopModel
from .hunter_models.hop_response_model import HopResponseModel

from ..utilities.enums import (
    AddressFamilyRIPEMeasurementRequest,
    DefinitionTypeRIPEMeasurementRequest,
    TrackStatus
)


class DataModelsConversor:
    @classmethod
    def track_to_hunter_model(cls, track_db_model: TrackDBModel) -> TrackModel:
        return TrackModel(
            id=track_db_model.id,
            timestamp=track_db_model.timestamp,
            status=TrackStatus(track_db_model.status),
            status_description=track_db_model.status_description,
            slim=track_db_model.slim,
            ip_address=track_db_model.ip_address,
        )

    @staticmethod
    def measurement_to_db(
            measurement_model: MeasurementModel,
            track_id: int
    ) -> MeasurementDBModel:
        return MeasurementDBModel(
            id=measurement_model.id,
            timestamp=measurement_model.timestamp,
            address_family=measurement_model.address_family.value,
            description=measurement_model.description,
            is_oneoff=measurement_model.is_oneoff,
            is_public=measurement_model.is_public,
            resolve_on_probe=measurement_model.resolve_on_probe,
            target=measurement_model.target,
            target_ip=measurement_model.target_ip,
            target_asn=measurement_model.target_asn,
            type=measurement_model.type.value,
            track_id=track_id,
        )

    @staticmethod
    def measurement_to_hunter_model(
            measurement_db_model: MeasurementDBModel
    ) -> MeasurementModel:
        return MeasurementModel(
            id=measurement_db_model.id,
            timestamp=measurement_db_model.timestamp,
            address_family=AddressFamilyRIPEMeasurementRequest(
                measurement_db_model.address_family),
            description=measurement_db_model.description,
            is_oneoff=measurement_db_model.is_oneoff,
            is_public=measurement_db_model.is_public,
            resolve_on_probe=measurement_db_model.resolve_on_probe,
            target=measurement_db_model.target,
            target_ip=measurement_db_model.target_ip,
            target_asn=measurement_db_model.target_asn,
            type=DefinitionTypeRIPEMeasurementRequest(
                measurement_db_model.type),
        )

    @staticmethod
    def traceroute_to_db_model(
            traceroute_model: TracerouteModel,
            measurement_id: int
    ) -> TracerouteDBModel:
        return TracerouteDBModel(
            timestamp=traceroute_model.timestamp,
            probe_id=traceroute_model.probe_id,
            origin_ip=traceroute_model.origin_ip,
            public_origin_ip=traceroute_model.public_origin_ip,
            destination_name=traceroute_model.destination_name,
            destination_ip=traceroute_model.destination_ip,
            measurement_id=measurement_id,
        )

    @staticmethod
    def traceroute_to_hunter_model(
            traceroute_db_model: TracerouteDBModel
    ) -> TracerouteModel:
        return TracerouteModel(
            id=traceroute_db_model.id,
            timestamp=traceroute_db_model.timestamp,
            probe_id=traceroute_db_model.probe_id,
            origin_ip=traceroute_db_model.origin_ip,
            public_origin_ip=traceroute_db_model.public_origin_ip,
            destination_ip=traceroute_db_model.destination_ip,
            destination_name=traceroute_db_model.destination_name,
        )

    @staticmethod
    def traceroute_hop_to_db_model(
            traceroute_hop_model: TracerouteHopModel,
            traceroute_id: int
    ) -> TracerouteHopDBModel:
        return TracerouteHopDBModel(
            hop_position=traceroute_hop_model.hop_position,
            traceroute_id=traceroute_id,
        )

    @staticmethod
    def traceroute_hop_to_hunter_model(
            traceroute_hop_db_model: TracerouteHopDBModel
    ) -> TracerouteHopModel:
        return TracerouteHopModel(
            id=traceroute_hop_db_model.id,
            hop_position=traceroute_hop_db_model.hop_position,
        )
        pass

    @staticmethod
    def hop_response_to_db_model(
            hop_response_model: HopResponseModel,
            hop_id: int
    ) -> HopResponseDBModel:
        return HopResponseDBModel(
            ip_address=hop_response_model.ip_address,
            ttl=hop_response_model.ttl,
            rtt_ms=hop_response_model.rtt_ms,
            hop_id=hop_id,
        )

    @staticmethod
    def hop_response_to_hunter_model(
            hop_response_db_model: HopResponseDBModel
    ) -> HopResponseModel:
        return HopResponseModel(
            id=hop_response_db_model.id,
            ip_address=hop_response_db_model.ip_address,
            ttl=hop_response_db_model.ttl,
            rtt_ms=hop_response_db_model.rtt_ms,
        )
