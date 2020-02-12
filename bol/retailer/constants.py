from enum import Enum


class ToStringableEnum(object):
    @classmethod
    def to_string(cls, v):
        if isinstance(v, cls):
            v = v.value
        assert v in map(lambda c: c.value, list(cls))
        return v


class FulfilmentMethod(ToStringableEnum, Enum):
    """
    The fulfilment method. Fulfilled by the retailer (FBR) or fulfilled by
    bol.com (FBB).
    """

    FBR = "FBR"
    FBB = "FBB"


class TransporterCode(ToStringableEnum, Enum):
    """
    https://api.bol.com/retailer/public/redoc/v3#tag/Transports
    """

    BPOST_BE = "BPOST_BE"
    BPOST_BRIEF = "BPOST_BRIEF"
    BRIEFPOST = "BRIEFPOST"
    COURIER = "COURIER"
    DHL = "DHL"
    DHLFORYOU = "DHLFORYOU"
    DHL_DE = "DHL_DE"
    DHL_GLOBAL_MAIL = "DHL-GLOBAL-MAIL"
    DPD_BE = "DPD-BE"
    DPD_NL = "DPD-NL"
    DYL = "DYL"
    FEDEX_BE = "FEDEX_BE"
    FEDEX_NL = "FEDEX_NL"
    FIEGE = "FIEGE"
    GLS = "GLS"
    LOGOIX = "LOGOIX"
    OTHER = "OTHER"
    PACKS = "PACKS"
    PARCEL_NL = "PARCEL-NL"
    RJP = "RJP"
    TNT = "TNT"
    TNT_BRIEF = "TNT_BRIEF"
    TNT_EXPRESS = "TNT-EXPRESS"
    TNT_EXTRA = "TNT-EXTRA"
    TRANSMISSION = "TRANSMISSION"
    TSN = "TSN"
    UPS = "UPS"
