# external imports
from enum import Enum

# internal imports


class TrackStatus(int, Enum):
    FINISHED: int = 0
    IN_PROGRESS: int = 1
    ERROR: int = -1


class AddressFamilyRIPEMeasurementRequest(int, Enum):
    IPV4: int = 4
    IPV6: int = 6


class DefinitionTypeRIPEMeasurementRequest(str, Enum):
    PING: str = "ping"
    TRACEROUTE: str = "traceroute"
    DNS: str = "DNS"
    SSL: str = "SSL"
    NTP: str = "NTP"
    HTTP: str = "http"


class ProbeObjectTypeRIPEMeasurementRequest(str, Enum):
    AREA: str = "area"
    COUNTRY: str = "country"
    PREFIX: str = "prefix"
    ASN: str = "asn"
    PROBES: str = "probes"
    MSM: str = "msm"

class MeasurementStatusRIPE(int, Enum):
    SPECIFIED: int = 0
    SCHEDULED: int = 1
    ONGOING: int = 2
    STOPPED: int = 4
    FORCED_TO_STOP: int = 5
    NO_SUITABLE_PROBES: int = 6
    FAILED: int = 7
    ARCHIVED: int = 8