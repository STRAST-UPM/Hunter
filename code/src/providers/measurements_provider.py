# external imports

# internal imports
from .database_provider import DatabaseProvider

from ..data_models.data_models_conversor import DataModelsConversor
from ..data_models.hunter_models.measurement_model import MeasurementModel


class MeasurementsProvider(DatabaseProvider):
    def __init__(self):
        super().__init__()

    def save_measurement(self, measurement_model: MeasurementModel, track_id: int):
        measurement_db_model = DataModelsConversor.measurement_to_db(
            measurement_model=measurement_model, track_id=track_id
        )

        return DataModelsConversor.measurement_to_hunter_model(
            self.add(measurement_db_model)
        )