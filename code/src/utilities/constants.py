# external imports
from os import getenv

# internal imports

# Texts
TRACEROUTE_MEASUREMENT_DESCRIPTION = "Hunter traceroute"

TRACK_STATUS_IN_PROGRESS_DESCRIPTION = "Track in progress"
TRACK_STATUS_FINISHED_DESCRIPTION = "Track finished"
TRACK_STATUS_ERROR_DESCRIPTION = "Track with error"

# Database
DATABASE_ENGINE = "postgresql"
DATABASE_HOST = getenv("DATABASE_HOST") if getenv("DATABASE_HOST") is not None else "localhost"
DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "password"
DATABASE_PORT = 5432
DATABASE_NAME = "postgres"
DATABASE_URL = (
    f"{DATABASE_ENGINE}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# RIPE Atlas
RIPE_ATLAS_TIME_BETWEEN_RESULTS_REQUESTS_SECONDS = 30
RIPE_ATLAS_PERCENTAGE_ENOUGH_RESULTS = 0.9
RIPE_ATLAS_MAXIMUM_TIME_TO_WAIT_RESULTS_SECONDS = 270

## Endpoints
RIPE_ATLAS_URL = "https://atlas.ripe.net"
RIPE_ATLAS_API_BASE_URL = f"{RIPE_ATLAS_URL}/api/v2"
RIPE_ATLAS_MEASUREMENTS_URL = f"{RIPE_ATLAS_API_BASE_URL}/measurements"
RIPE_ATLAS_MEASUREMENTS_RESULTS_URL = f"{RIPE_ATLAS_MEASUREMENTS_URL}"+"/{measurement_id}/results"
RIPE_ATLAS_MEASUREMENTS_STATUS_CHECK = f"{RIPE_ATLAS_MEASUREMENTS_URL}"+"/{measurement_id}/status-check"
RIPE_ATLAS_PROBES_URL = f"{RIPE_ATLAS_API_BASE_URL}/probes"

# IPInformationProvider
IPINFO_CACHE_HOST = getenv("IPINFO_CACHE_HOST") if getenv("IPINFO_CACHE_HOST") is not None else "localhost"
IPINFO_CACHE_PORT = 5000
IPINFO_CACHE_BASE_URL = f"http://{IPINFO_CACHE_HOST}:{IPINFO_CACHE_PORT}"
IPINFO_CACHE_IP_INFO = f"{IPINFO_CACHE_BASE_URL}/ip/"+"{ip_address}"

HUNTER_PORT=getenv("HUNTER_PORT", 8000)