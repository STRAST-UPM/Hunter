from enum import Enum

class TrackStatus(Enum):
    FINISHED: int = 0
    IN_PROGRESS: int = 1
    ERROR: int = -1

class AddressFamilyRIPEMeasurementRequest(Enum):
    IPV4: int = 4
    IPV6: int = 6

class DefinitionTypeRIPEMeasurementRequest(Enum):
    PING: str = "ping"
    TRACEROUTE: str = "traceroute"
    DNS: str = "DNS"
    SSL: str = "SSL"
    NTP: str = "NTP"
    HTTP: str = "http"

class ProbeObjectTypeRIPEMeasurementRequest(Enum):
    AREA: str = "area"
    COUNTRY: str = "country"
    PREFIX: str = "prefix"
    ASN: str = "asn"
    PROBES: str = "probes"
    MSM: str = "msm"