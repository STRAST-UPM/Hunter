# external imports

# internal imports
from .database_provider import DatabaseProvider

from ..data_models.data_models_conversor import DataModelsConversor
from ..data_models.hunter_models.measurement_model import MeasurementModel
from ..data_models.hunter_models.traceroute_model import TracerouteModel


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

    def save_traceroute_results(
            self,
            traceroute_result: TracerouteModel,
            measurement_id: int):
        traceroute_db_model = self.add(
            DataModelsConversor.traceroute_to_db_model(
                traceroute_model=traceroute_result,
                measurement_id=measurement_id,
            )
        )

        for traceroute_hop in traceroute_result.hops:
            traceroute_hop_db_model = self.add(
                DataModelsConversor.traceroute_hop_to_db_model(
                    traceroute_hop_model=traceroute_hop,
                    traceroute_id=traceroute_db_model.id,
                )
            )

            for hop_response in traceroute_hop.hop_responses:
                self.add(
                    DataModelsConversor.hop_response_to_db_model(
                        hop_response_model=hop_response,
                        hop_id=traceroute_hop_db_model.id,
                    )
                )


