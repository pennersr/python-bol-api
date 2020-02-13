class FulfilmentMethod:
    """
    The fulfilment method. Fulfilled by the retailer (FBR) or fulfilled by
    bol.com (FBB).
    """

    FBR = "FBR"
    FBB = "FBB"


class TransporterCode:
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


class CancellationReasonCode:
    OUT_OF_STOCK = "OUT_OF_STOCK"
    REQUESTED_BY_CUSTOMER = "REQUESTED_BY_CUSTOMER"
    BAD_CONDITION = "BAD_CONDITION"
    HIGHER_SHIPCOST = "HIGHER_SHIPCOST"
    INCORRECT_PRICE = "INCORRECT_PRICE"
    NOT_AVAIL_IN_TIME = "NOT_AVAIL_IN_TIME"
    NO_BOL_GUARANTEE = "NO_BOL_GUARANTEE"
    ORDERED_TWICE = "ORDERED_TWICE"
    RETAIN_ITEM = "RETAIN_ITEM"
    TECH_ISSUE = "TECH_ISSUE"
    UNFINDABLE_ITEM = "UNFINDABLE_ITEM"
    OTHER = "OTHER"
