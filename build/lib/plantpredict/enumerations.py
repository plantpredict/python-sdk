class AirMassModelTypeEnum(object):
    """Air Mass Model"""
    BIRD_HULSTROM = 0
    KASTEN_SANDIA = 1


class BacktrackingTypeEnum(object):
    """Backtracking Type"""
    TRUE_TRACKING = 0   # no backtracking
    BACKTRACKING = 1    # shade avoidance


class CellTechnologyTypeEnum(object):
    """Cell Technology"""
    NTYPE_MONO_CSI = 1
    PTYPE_MONO_CSI_PERC = 2
    PTYPE_MONO_CSI_BSF = 3
    POLY_CSI_PERC = 4
    POLY_CSI_BSF = 5
    CDTE = 6
    CIGS = 7


class CleaningFrequencyEnum(object):
    """Cleaning Frequency"""
    NONE = 0
    DAILY = 1
    MONTHLY = 2
    QUARTERLY = 3
    YEARLY = 4


class ConstructionTypeEnum(object):
    """Construction Type"""
    GLASS_GLASS = 1
    GLASS_BACKSHEET = 2


class DataSourceEnum(object):
    """Data Source"""
    MANUFACTURER = 1
    PVSYST = 2
    UNIVERSITY_OF_GENEVA = 3
    PHOTON = 4
    SANDIA_DATABASE = 5
    CUSTOM = 6


class DegradationModelEnum(object):
    """Degradation Model"""
    NONE = 0
    STEPPED_AC = 1
    LINEAR_AC = 2
    LINEAR_DC = 3
    NON_LINEAR_DC = 4


class DiffuseDirectDecompositionModelEnum(object):
    """Diffuse Direct Decomposition Model"""
    ERBS = 0
    REINDL = 1
    DIRINT = 2
    NONE = 3


class DiffuseShadingModelEnum(object):
    """Diffuse Shading Model"""
    NONE = 0
    SCHAAR_PANCHULA = 1


class DirectBeamShadingModelEnum(object):
    """Direct Beam Shading Model"""
    LINEAR = 0
    NONE = 1
    TWO_DIMENSION = 2       # Retired
    FRACTIONAL_EFFECT = 3   # Fractional Electric Shading
    CSI_3_DIODE = 4
    MODULE_FILE_DEFINED = 5


class EntityTypeEnum(object):
    """Entity Type"""
    PROJECT = 1
    MODULE = 2
    INVERTER = 3
    WEATHER = 4
    PREDICTION = 5


class ESSChargeAlgorithmEnum(object):
    """Energy Storage System (ESS) Charge Algorithm"""
    LGIA_EXCESS = 0
    ENERGY_AVAILABLE = 1
    CUSTOM = 2


class ESSDispatchCustomCommandEnum(object):
    """Energy Storage System (ESS) Dispatch Custom Command"""
    NONE = 0
    DISCHARGE = 1
    CHARGE = 2


class FacialityEnum(object):
    """Faciality"""
    MONOFACIAL = 0
    BIFACIAL = 1


class IncidenceAngleModelTypeEnum(object):
    """Incidence Angle Model Type"""
    SANDIA = 2
    ASHRAE = 3
    NONE = 4
    TABULAR_IAM = 5


class LibraryStatusEnum(object):
    """Library Status (for Module, Inverter, Weather)"""
    UNKNOWN = 0
    DRAFT_PRIVATE = 1
    DRAFT_SHARED = 2
    ACTIVE = 3
    RETIRED = 4
    GLOBAL = 5
    GLOBAL_RETIRED = 6


class ModuleDegradationModelEnum(object):
    """Module Degradation Model"""
    UNSPECIFIED = 0
    LINEAR = 1
    NONLINEAR = 2


class ModuleOrientationEnum(object):
    """Module Orientation"""
    LANDSCAPE = 0
    PORTRAIT = 1


class ModuleShadingResponseEnum(object):
    """Module Shading Response"""
    NONE = 0
    LINEAR = 1
    FRACTIONAL_EFFECT = 2   # Fractional Electrical Shading
    CSI_3_DIODE = 3
    CUSTOM = 4


class ModuleTemperatureModelEnum(object):
    """Module Temperature Model"""
    HEAT_BALANCE = 0
    SANDIA = 1


class ModuleTypeEnum(object):
    """Module Type"""
    SINGLE_DIODE = 0
    ADVANCED_DIODE = 1


class PredictionStatusEnum(object):
    """Prediction Status"""
    DRAFT_PRIVATE = 1
    DRAFT_SHARED = 2
    ANALYSIS = 3
    BID = 4
    CONTRACT = 5
    DEVELOPMENT = 6
    AS_BUILT = 7
    WARRANTY = 8
    ARCHIVED = 9


class PredictionVersionEnum(object):
    """Prediction Version"""
    VERSION_3 = 3
    VERSION_4 = 4
    VERSION_5 = 5
    VERSION_6 = 6
    VERSION_7 = 7


class ProcessingStatusEnum(object):
    """Processing Status"""
    NONE = 0
    QUEUED = 1
    RUNNING = 2
    SUCCESS = 3
    ERROR = 4


class ProjectStatusEnum(object):
    """Project Status"""
    ACTIVE = 0
    ARCHIVED = 1


class PVModelTypeEnum(object):
    """PV Model"""
    ONE_DIODE_RECOMBINATION = 0
    ONE_DIODE = 1
    ONE_DIODE_RECOMBINATION_NONLINEAR = 3


class SoilingModelTypeEnum(object):
    """Soiling Model"""
    CONSTANT_MONTHLY = 0
    WEATHER_FILE = 1
    NONE = 2


class SpectralShiftModelEnum(object):
    """Spectral Shift Model"""
    NO_SPECTRAL_SHIFT = 0
    ONE_PARAM_PWAT_OR_SANDIA = 1
    TWO_PARAM_PWAT_AND_AM = 2
    MONTHLY_OVERRIDE = 3


class SpectralWeatherTypeEnum(object):
    """Spectral Weather Type"""
    NONE = 0
    NGAN_PWAT = 1
    NGAN_RH = 2
    NGAN_DEWPOINT = 3


class TrackingTypeEnum(object):
    """Tracking Type"""
    FIXED_TILT = 0
    HORIZONTAL_TRACKER = 1
    SEASONAL_TILT = 2


class TranspositionModelEnum(object):
    """Transposition Model"""
    HAY = 0
    PEREZ = 1


class WeatherDataProviderEnum(object):
    """Weather Data Provider"""
    NREL = 1
    AWS = 2
    WIND_LOGICS = 3
    METEONORM = 4
    THREE_TIER = 5
    CLEAN_POWER_RESEARCH = 6
    GEO_MODEL_SOLAR = 7
    GEO_SUN_AFRICA = 8
    SODA = 9
    HELIO_CLIM = 10
    SOLAR_RESOURCE_ASSESSMENT = 11
    ENERGY_PLUS = 12
    OTHER = 13
    CUSTOMER = 14
    SOLAR_PROSPECTOR = 15
    GLOBAL_FED = 16
    NSRDB = 17
    WHITE_BOX_TECHNOLOGIES = 18
    SOLARGIS = 19
    NASA = 20


class WeatherDataTypeEnum(object):
    """Weather Data Type"""
    SYNTHETIC_MONTHLY = 0
    SATELLITE = 1
    GROUND_CORRECTED = 2
    MEASURED = 3
    TMY3 = 4
    TGY = 5
    TMY = 6
    PSM = 7
    SUNY = 8
    MTS2 = 9
    CZ2010 = 10


class WeatherFileColumnTypeEnum(object):
    """Weather File Column Type"""
    GHI = 1
    DNI = 2
    DHI = 3
    TEMP = 4
    WINDSPEED = 5
    RELATIVE_HUMIDITY = 6
    PWAT = 7
    RAIN = 8
    PRESSURE = 9
    DEWPOINT_TEMP = 10
    WIND_DIRECTION = 11
    SOILING_LOSS = 12
    POAI = 13


class WeatherPLevelEnum(object):
    """Weather P-Level"""
    P50 = 0
    P90 = 1
    P95 = 3
    P99 = 4
    NA = 2      # N/A
    P75 = 5


class WeatherSourceTypeAPIEnum(object):
    """
    Weather Source Type API (web-service downloadable vendors). This Enum is used when calling
    :py:meth:`~plantpredict.weather.Weather.download`.
    """
    UNKNOWN = 0   # Default
    METEONORM = 1
    CPR_SOLAR_ANYWHERE = 2
    NSRDB_PSM = 3
    NSRDB_SUNY = 4
    NSRDB_MTS2 = 5
    SOLAR_GIS = 6
    NASA = 7


class WeatherTimeResolution(object):
    """Weather Time Resolution"""
    UNKNOWN = 0
    HALF_HOUR = 1
    HOUR = 2
    MINUTE = 3
