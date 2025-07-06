# external imports

# internal imports
from .hunter_models.measurement_model import MeasurementModel

from .database_models.measurement_db_model import MeasurementDBModel

from ..utilities.enums import (
    AddressFamilyRIPEMeasurementRequest,
    DefinitionTypeRIPEMeasurementRequest
)


class DataModelsConversor:
    @staticmethod
    def measurement_to_db(measurement_model: MeasurementModel, track_id: int) -> MeasurementDBModel:
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
    def measurement_to_hunter_model(measurement_db_model: MeasurementDBModel) -> MeasurementModel:
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