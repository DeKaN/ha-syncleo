DOMAIN = "syncleo"

VENDOR_RUSCLIMATE = "rusclimate"
VENDOR_POLARIS = "polaris"

FIRMVARE_HOST_BY_VENDOR = {
    VENDOR_RUSCLIMATE: "firmware.cdn.rusklimat.ru",
    VENDOR_POLARIS: "firmware.cdn.polaris-iot.com",
}

CONF_ATTRIBUTES = "attributes"
CONF_FIRMWARE = "firmware"
CONF_MANUFACTURER = "manufacturer"
CONF_PROTOCOL = "protocol"
CONF_PUBLIC_KEY = "public"
CONF_VENDOR = "vendor"
CONF_MODEL_CLASS = "model_class"

FAN_MAX = "max"
FAN_MID_HIGH = "mid_high"
FAN_MID_LOW = "mid_low"
FAN_MIN = "min"
FAN_QUITE = "quite"
FAN_TURBO = "turbo"

KETTLE_MODE_BOILING = "boiling"
KETTLE_MODE_BOILING_KEEP = "boiling_keep"
KETTLE_MODE_WARM_UP = "warm_up"
KETTLE_MODE_WARM_UP_KEEP = "warm_up_keep"
KETTLE_MODE_IQ_BOILING = "iq_boiling"
KETTLE_MODE_TEA_TIME = "tea_time"

KETTLE_PRESET_NONE = "kettle_preset_none"
KETTLE_PRESET_BLACK_TEA = "kettle_preset_black_tea"
KETTLE_PRESET_BABY_BOTTLE = "kettle_preset_baby_bottle"
KETTLE_PRESET_INSTANT_COFFEE = "kettle_preset_instant_coffee"
KETTLE_PRESET_GREEN_TEA = "kettle_preset_green_tea"
KETTLE_PRESET_FLOWER_TEA = "kettle_preset_flower_tea"
KETTLE_PRESET_TEA_BAG = "kettle_preset_tea_bag"
KETTLE_PRESET_RED_TEA = "kettle_preset_red_tea"
KETTLE_PRESET_PUER = "kettle_preset_puer"
KETTLE_PRESET_OOLONG_TEA = "kettle_preset_oolong_tea"
KETTLE_PRESET_WHITE_TEA = "kettle_preset_white_tea"
KETTLE_PRESET_HERBAL_TEA = "kettle_preset_herbal_tea"

PD_ANGLE_HORIZONTAL = "angle_horizontal"
PD_ANGLE_VERTICAL = "angle_vertical"
PD_ANTI_FROST_TEMP = "anti_frost_temp"
PD_AUTO_OFF_DISPLAY = "auto_off_display"
PD_BACKLIGHT_BLUE = "backlight_blue"
PD_BACKLIGHT_GREEN = "backlight_green"
PD_BACKLIGHT_RED = "backlight_red"
PD_BREEZE_AWAY = "breeze_away"
PD_CO2_INSTALLED = "co2_installed"
PD_UV_INSTALLED = "uv_installed"
PD_CURRENT_PRESET = "current_preset"
PD_COOLDOWN = "cooldown"
PD_DAMPER = "damper"
PD_DISPLAY_HALF_POWER = "display_half_power"
PD_ECO_DELTA = "eco_delta"
PD_ENERGY_SAVING = "energy_saving"
PD_EXPENDABLES_ANODE = "expendables_anode"
PD_FIREPLACE = "fireplace"
PD_FREEZE_PROTECTION = "freeze_protection"
PD_FUNGUS_PROOF = "fungus_proof"
PD_HEATER_INSTALLED = "heater_installed"
PD_LAST_PROGRAM = "last_program"
PD_MIN_VOLTAGE = "min_voltage"
PD_NIGHT_SPEED = "night_speed"
PD_NOISELESS = "noiseless"
PD_POWER = "power"
PD_SELFCLEAN = "selfclean"
PD_SILENCE_MODE = "silence_mode"
PD_SWING_HORIZONTAL = "swing_horizontal"
PD_SWING_VERTICAL = "swing_vertical"
PD_TIME_START = "time_start"
PD_TIME_END = "time_end"
PD_TURN_ON = "turn_on"
PD_VACATION_TEMPERATURE = "vacation_temperature"

# Custom device specific values
PD_AURUS_A_AIR_CLEAN = "aurus_a_air_clean"
PD_AURUS_SCREENSAVER_MODE = "aurus_screensaver_mode"
PD_BREEZER_AUTO_INTENSITY = "breezer_auto_intensity"
PD_BREEZER_DAMPER = "breezer_damper"

PRESET_ANTI_FROST = "anti_frost"
PRESET_AUTO = "auto"
PRESET_NIGHT = "night"
PRESET_MANUAL = "manual"
PRESET_TURBO = "turbo"
PRESET_VACATION = "vacation"
PRESET_VENTILATION = "ventilation"
PRESET_HEALTH = "health"
PRESET_BABY = "baby"
PRESET_ECO = "eco"
PRESET_FITNES = "fitnes"
PRESET_YOGA = "yoga"
PRESET_MEDITATION = "meditation"
PRESET_PRANA_HANDS = "prana_hands"
PRESET_PRANA_AUTO = "prana_auto"
PRESET_AROMA = "aroma"

# Custom device specific values
PRESET_AURUS_SCREENSAVER_MODE_OFF = "screensaver_off"
PRESET_AURUS_SCREENSAVER_MODE_1 = "screensaver_1"
PRESET_AURUS_SCREENSAVER_MODE_3 = "screensaver_3"
PRESET_AURUS_SCREENSAVER_MODE_5 = "screensaver_5"

PRESET_MELODY_BIRDS_SINGING = "melody_birds_singing"
PRESET_MELODY_FIREPLACE_SOUND = "melody_fireplace_sound"
PRESET_MELODY_FOREST_SOUND = "melody_forest_sound"
PRESET_MELODY_RAIN_SOUND = "melody_rain_sound"
PRESET_MELODY_SEA_SOUND = "melody_sea_sound"

PRESET_NIGHT_MODE_OFF = "night_mode_off"
PRESET_NIGHT_MODE_AGED = "night_mode_aged"
PRESET_NIGHT_MODE_CHILD = "night_mode_child"
PRESET_NIGHT_MODE_STANDARD = "night_mode_standard"
PRESET_NIGHT_MODE_TEEN = "night_mode_teen"

PRESET_TOSHIBA_POWER_50 = "power_50"
PRESET_TOSHIBA_POWER_75 = "power_75"
PRESET_TOSHIBA_POWER_100 = "power_100"

PRESET_TOSHIBA_NOISELESS_OFF = "noiseless_off"
PRESET_TOSHIBA_NOISELESS_1 = "noiseless_1"
PRESET_TOSHIBA_NOISELESS_2 = "noiseless_2"

FEATURE_ACCESS_CONTROL = "access_control"
FEATURE_ANTI_MELDEW = "anti_meldew"
FEATURE_BACKLIGHT = "backlight"
FEATURE_BSS = "bss"
FEATURE_CHILD_LOCK = "child_lock"
FEATURE_CURRENT_CO2 = "current_co2"
FEATURE_CURRENT_TEMPERATURE = "current_temperature"
FEATURE_CURRENT_HUMIDITY = "current_humidity"
FEATURE_DAMPER = "damper"
FEATURE_ECO_AS_SMART_MODE = "energy_saving"
FEATURE_ERROR = "error"
FEATURE_EXPENDABLES_ANODE = "expendables_anode"
FEATURE_EXPENDABLES_CLEAN = "expendables_clean"
FEATURE_EXPENDABLES_FILTER = "expendables_filter"
FEATURE_EXPENDABLES_PREFILTER = "expendables_prefilter"
FEATURE_IONIZATION = "ionization"
FEATURE_KEEP_WARM = "keep_warm"
FEATURE_NIGHT = "night"
FEATURE_PM2 = "pm2"
FEATURE_POWER_LEVEL = "power_level"
FEATURE_RSSI = "rssi"
FEATURE_SMART_MODE = "smart_mode"
FEATURE_SPEED = "speed"
FEATURE_TANK = "tank"
FEATURE_TIMER = "timer"
FEATURE_TURBO = "turbo"
FEATURE_ULTRAVIOLET = "ultraviolet"
FEATURE_VOLUME = "volume"
FEATURE_WEIGHT = "weight"
FEATURE_WARM_STREAM = "warm_stream"
FEATURE_HUMIDIFIER_WARM_STREAM = "humidifier_warm_stream"

# Custom device specific features
FEATURE_AURUS_PF_AUTO_OFF_DISPLAY = "aurus_pf_auto_off_display"
FEATURE_AURUS_PF_HALF_POWER = "aurus_pf_half_power"
FEATURE_AURUS_SCREENSAVER_MODE = "aurus_screensaver_mode"
FEATURE_AURUS_VRF_CHILD_LOCK = "aurus_vrf_child_lock"
FEATURE_AURUS_VRF_ECO_MODE = "aurus_vrf_eco_mode"
FEATURE_AURUS_VRF_NOISELESS_MODE = "aurus_vrf_noiseless_mode"
FEATURE_BREEZER_DAMPER = "breezer_damper"
FEATURE_BREEZER_MELODY = "breezer_melody"
FEATURE_BREEZER_TEMPERATURE = "breezer_temperature"
FEATURE_KETTLE_TEMPERATURE_PRESET = "kettle_temperature_preset"
FEATURE_GOLDSTAR_GSTI_BREEZE_AWAY = "breeze_away"
FEATURE_GOLDSTAR_GSTI_CLEAN = "selfclean"
FEATURE_GOLDSTAR_GSTI_DAMPER = "goldstar_gsti_damper"
FEATURE_GOLDSTAR_GSTI_FREEZE_PROTECTION = "freeze_protection"
FEATURE_SHUFT_SFMS_07_09_FREEZE_PROTECTION = "freeze_protection"
FEATURE_SHUFT_SFMS_09_ANTI_MELDEW = "shuft_sfms_09_anti_meldew"
FEATURE_HUMIDIFIER_INTENSITY = "humidifier_intensity"

PROFILE_TYPE_AC = "ac"
PROFILE_TYPE_AIR_FRYER = "air_fryer"
PROFILE_TYPE_BOILER = "boiler"
PROFILE_TYPE_BREEZER = "breezer"
PROFILE_TYPE_HEATER = "heater"
PROFILE_TYPE_HUMIDIFIER = "humidifier"
PROFILE_TYPE_KETTLE = "kettle"
PROFILE_TYPE_AIRCLEANER = "air_cleaner"

TRANLATION_KEY_CLIMATE = DOMAIN + "_climate"
TRANLATION_KEY_FAN = DOMAIN + "_fan"

ZEROCONF_CURVE = "curve"
ZEROCONF_DEVICE_TYPE = "devtype"
ZEROCONF_MAC_ADDRESS = "macaddr"


POLARIS_DEVICE = {
    0:   "Unknown",
# kettle
    37:  "PWK-7111CGLD",
    245: "PWK-0105",
    205: "PWK-1538CC",
    271: "PWK-1701CGLD",
    36:  "PWK-17107CGLD",
    29:  "PWK-1712CGLD",
    38:  "PWK-1712CGLD",
    54:  "PWK-1712CGLD",
    59:  "PWK-1712CGLD",
    63:  "PWK-1712CGLD",
    97:  "PWK-1712CGLD",
    117: "PWK-1712CGLD",
    208: "PWK-1712CGLD",
    83:  "PWK-1712CGLD RGB",
    253: "PWK-1715",
    244: "PWK-1716CGLD",
    67:  "PWK-1720CGLD",
    84:  "PWK-1720CGLD RGB",
    6:   "PWK-1725CGLD",
    52:  "PWK-1725CGLD",
    57:  "PWK-1725CGLD",
    61:  "PWK-1725CGLD",
    82:  "PWK-1725CGLD",
    86:  "PWK-1725CGLD",
    105: "PWK-1725CGLD",
    106: "PWK-1725CGLD",
    177: "PWK-1725CGLD",
    194: "PWK-1725CGLD",
    196: "PWK-1725CGLD",
    164: "PWK-1728CGLDA",
    209: "PWK-1729CAD",
    189: "PWK-1746CA",
    260: "PWK-1746CA",
    308: "PWK-1746CA",
    8:   "PWK-1755CAD",
    53:  "PWK-1755CAD",
    58:  "PWK-1755CAD",
    62:  "PWK-1755CAD",
    185: "PWK-1755CAD",
    165: "PWK-1755CAD VOICE",
    121: "PWK-1774CAD",
    2:   "PWK-1775CGLD",
    51:  "PWK-1775CGLD",
    56:  "PWK-1775CGLD",
    60:  "PWK-1775CGLD",
    98:  "PWK-1775CGLD",
    188: "PWK-1775CGLD",
    223: "PWK-1775CGLD",
    262: "PWK-1775CGLD",
    263: "PWK-1775CGLD",
    275: "PWK-1775CGLD",
    294: "PWK-1775CGLD",
    85:  "PWK-1775CGLD SMART",
    139: "PWK-1775CGLD VOICE",
    175: "PWK-1823CGLD",
    254: "PWK-1823CGLD",
    176: "PWK-1841CGLD",
    255: "PWK-1841CGLD",
# humidifier
    147: "PUH-0205",
    71:  "PUH-1010",
    72:  "PUH-2300",
    73:  "PUH-3030",
    75:  "PUH-4040",
    99:  "PUH-4040",
    153: "PUH-4055",
    137: "PUH-4066",
    157: "PUH-4550",
    158: "PUH-6060",
    25:  "PUH-6090",
    15:  "PUH-7406",
    87:  "PUH-8080/PUH-4606",
    155: "PUH-8802",
    74:  "PUH-9009",
    4:   "PUH-9105/PUH-2709",
    17:  "PUH-9105/PUH-2709",
    18:  "PUH-9105/PUH-2709",
    44:  "PUH-9105/PUH-2709",
    70:  "PUH-9105/PUH-2709",
# cooker
    1:   "EVO-0225",
    95:  "PMC-00000",
    303: "PMC-0510",
    301: "PMC-0515",
    10:  "PMC-0521",
    41:  "PMC-0521",
    267: "PMC-0521",
    55:  "PMC-0524",
    206: "PMC-0524",
    9:   "PMC-0526",
    40:  "PMC-0526",
    138: "PMC-0526",
    39:  "PMC-0528",
    48:  "PMC-0528",
    268: "PMC-0528",
    47:  "PMC-0530",
    270: "PMC-0530",
    210: "PMC-0590AD",
    302: "PMC-0597",
    215: "PMC-5001",
    79:  "PMC-5017",
    192: "PMC-5017",
    80:  "PMC-5020",
    266: "PMC-5020",
    77:  "PMC-5040",
    78:  "PMC-5050",
    89:  "PMC-5055",
    114: "PMC-5060 Smart Motion",
    240: "PMC-5060 Smart Motion",
    162: "PMC-5063",
    169: "PPC-1505",
    183: "PPC-1505",
# coffeemaker
    235: "AM-7310",
    305: "PACM-2072",
    103: "PACM-2080AC",
    261: "PACM-2080AC",
    276: "PACM-2080AC",
    277: "PACM-2080AC",
    200: "PACM-2081AC",
    265: "PACM-2081AC",
    280: "PACM-2081AC",
    166: "PACM-2085GC",
    278: "PACM-2085GC",
    247: "PCM-1255",
    45:  "PCM-1540",
    222: "PCM-1540",
    274: "PCM-1540",
    279: "PCM-1540",
    190: "PCM-1560",
    207: "PCM-2070CG",
# air_cleaner
    172: "PAW-0804",
    140: "PAW-0804",
    151: "PPA-2025",
    203: "PPA-2025",
    250: "PPA-2025",
    152: "PPA-4050",
    204: "PPA-4050",
    251: "PPA-4050",
    236: "PPAT-02A",
    238: "PPAT-80P",
    239: "PPAT-90GDi",
# irrigator
    132: "PWF-2005",
    252: "PWF-2005",
# air_fryer
    273: "PAF-4001",
    290: "PAF-6003",
    291: "PAF-8003",
    292: "PAF-8005",
# boiler
    31:  "ENIGMA",
    11:  "PWH-IDF06",
    30:  "SIGMA",
    249: "VEKTOR",
# heater
    46:  "PCH-0320",
    65:  "PCH-0320",
    16:  "PHV-1401",
    49:  "PMH-21XX",
    64:  "PMH-21XX",
# cleaner
    101: "PVCR-0726 Aqua",
    108: "PVCR-0726 GYRO",
    21:  "PVCR-0735",
    163: "PVCR-0735",
    19:  "PVCR-0833",
    43:  "PVCR-0833",
    104: "PVCR-0905",
    156: "PVCR-0905",
    107: "PVCR-0926",
    23:  "PVCR-1028",
    22:  "PVCR-1050",
    102: "PVCR-1226 Aqua",
    109: "PVCR-1226 GYRO",
    24:  "PVCR-1229",
    68:  "PVCR-3100",
    7:   "PVCR-3200",
    76:  "PVCR-3200",
    115: "PVCR-3200",
    12:  "PVCR-3300",
    81:  "PVCR-3400",
    130: "PVCR-3600",
    112: "PVCR-3700",
    88:  "PVCR-3800",
    66:  "PVCR-3900",
    131: "PVCR-3900",
    113: "PVCR-4000",
    197: "PVCR-4000",
    110: "PVCR-4105",
    127: "PVCR-4105",
    199: "PVCR-4250",
    241: "PVCR-4250",
    211: "PVCR-4260",
    269: "PVCR-4260",
    142: "PVCR-4500",
    195: "PVCR-4500",
    307: "PVCR-4750",
    119: "PVCR-5001",
    146: "PVCR-5001",
    154: "PVCR-5001",
    201: "PVCR-5003",
    242: "PVCR-5005",
    123: "PVCR-6001",
    148: "PVCR-6001",
    221: "PVCR-6001",
    187: "PVCR-6003",
    256: "PVCR-7026",
    128: "PVCRAC-7050",
    212: "PVCRAC-7290",
    178: "PVCRAC-7750",
    198: "PVCRAC-7790",
    264: "PVCRAC-7790",
    126: "PVCRDC-0101",
    160: "PVCRDC-0101",
    124: "PVCRDC-5002",
    149: "PVCRDC-5002",
    213: "PVCRDC-5002",
    202: "PVCRDC-5004",
    181: "PVCRDC-5006",
    125: "PVCRDC-6002",
    150: "PVCRDC-6002",
    186: "PVCRDC-6004",
    257: "PVCRDC-7028",
    217: "PVCRDC-G2-5002",
    218: "PVCRDC-G2-6002",
    133: "PVCR-G2-0726W",
    193: "PVCR-G2-0826",
    134: "PVCR-G2-0926W",
    135: "PVCR-G2-1226",
    129: "PVCR-G2-3200",
    122: "PVCR-G2-3600",
    219: "PVCR-G2-5001",
    220: "PVCR-G2-6001",
    100: "PVCR Wave-15",
# window_cleaner
    246: "PRWC-3001",
# blender
    93:  "PHB-1350",
    35:  "PHB-1503",
    34:  "PHB-1551",
# cooktop
    282: "induction-hob",
    286: "XFC302I-B3SF",
    288: "XFC302T-B1D",
    285: "XFC604I",
    304: "XFC604I",
    284: "XFC604I-B8F",
    287: "XFC604T-B7D",
    289: "XFG640F-B3P",
# cordless_cleaner
    111: "PVCS-1150",
    90:  "PVCS-2090",
    136: "PVCS-4070",
    229: "PVCS-4070",
    232: "PVCS-6020",
    281: "PVCS-6020",
    230: "PVCS-8200",
    234: "PVCSDC-3000",
    233: "PVCSDC-3005",
    306: "PVCSDC-3005",
# fan
    180: "PSF-3315",
    248: "PSF-4025",
# grill
    179: "PGP-3010 SMOKELESS",
    96:  "PGP-4001",
# hair_care
    120: "PHD-4000",
    184: "PHS-1300",
    171: "PHSB-5000DF",
    145: "PHSC-1234",
# hood
    297: "8006",
    296: "8029",
    295: "6065A-600",
# iron
    283: "PGS-2250VA",
    91:  "PIR-2624AK 3m",
    161: "PIR-3074SG",
    173: "PIR-3210AK 3m",
    174: "PIR-3225AK 3m",
    191: "PSS-2002K",
    259: "PSS-8010K",
    159: "PSS-9090K",
# kitchen_machine
    237: "SM-8095",
    272: "SM-8095",
# meat_grinder
    32:  "PMG-2580",
    216: "PMG-3060",
# other
    116: "Smart Lid",
# oven
    299: "xbcook55",
    300: "xbcook56",
    298: "xbcook62",
# steamer
    92:  "PGS-1450C",
    94:  "PSS-7070K",
# toothbrush
    50:  "PETB-0202TC",
}
HOMMYN_DEVICE = {
    0:   "Unknown",
# air_cleaner
    1:   "Electrolux EAP-1040D/1055D",
    26:  "Electrolux EAP-2050D/2075D",
    117: "Ballu AP-135",
# breezer
    3:   "Ballu ONEAIR ASP-200",
    30:  "Ballu ONEAIR ASP-200S",
    32:  "Ballu ASP-100/Electrolux EASP-100",
    34:  "Electrolux EPVS/ERVX inv",
    36:  "Electrolux EPVS/ERVX inv",
    59:  "Ballu ONEAIR ASP-200S",
    69:  "Ballu ASP-100/Electrolux EASP-100",
    98:  "Shuft Allston VH/ERV",
    100: "Shuft Allston VH/ERV",
    102: "Ballu ONEAIR ASP-90",
    105: "Ballu ONEAIR ASP-90",
    106: "Ballu ONEAIR ASP-90",
    107: "Ballu ONEAIR ASP-90",
# recirculator
    27:  "Ballu RDU ANTICOVID generator",
# air_conditioner
    8:   "Electrolux Atrium DC/Zanussi Siena DC/Ballu Lagoon",
    10:  "Zanussi Massimo Solar",
    13:  "Electrolux Smartline/Ballu Eco Smart/Ice Peak",
    15:  "Electrolux Viking DC/Zanussi Perfecto DC/Ballu Greenland DC",
    20:  "Ballu Platinum Evol DC/Olympio Legend",
    21:  "Zanussi Moderno DC/Electrolux Loft DC",
    38:  "Toshiba Shorai EE",
    41:  "Electrolux Monaco DC",
    51:  "Zanussi Massimo Solar 2023",
    55:  "Zanussi Barocco DC/Royal Thermo Barocco DC",
    56:  "Toshiba",
    57:  "Shuft Berg/MBO M-1",
    60:  "Ballu Discovery DC",
    68:  "Electrolux Loft DC/Ballu Platinum Black DC",
    70:  "Ballu Universal 3/DC/Free Match",
    72:  "Zanussi Barocco/Royal Thermo Barocco",
    82:  "Goldstar GSAC/GSACI",
    83:  "Ballu Aura",
    84:  "Ballu Aura",
    85:  "Aurus D",
    95:  "Climer Dresden",
    99:  "AURUS A",
    108: "Royal Thermo Diamond DC",
# boiler
    2:   "SmartInverter",
    7:   "Zanussi Artendo/Azurro PRO",
    12:  "Electrolux Centurio IQ 2.0/Maximus",
    16:  "Ballu Smart",
    18:  "Electrolux Maximus/Megapolis/Zanussi Splendore XP 2.0/Artendo PRO-C",
    19:  "Electrolux Regency",
    33:  "Electrolux Centurio IQ 3.0",
    44:  "Royal Thermo Aqua Inverter/Royal Thermo Aqua Inox Inverter",
    74:  "Aurus S",
    76:  "Electrolux Royal Flash/Centurio IQ Inverter",
    77:  "Royal Thermo Major Inverter/Smalto Inverter",
    80:  "Aurus F",
    90:  "Ballu Cetrion Inverter/Ballu Cetrion Inox Inverter",
    91:  "Royal Thermo Regency",
# fireplace
    50:  "Electrolux 3D Fireplace",
# heater
    6:   "Transformer DI 3.0",
    9:   "Transformer DI 3.0 S",
    11:  "Ballu Rapid",
    14:  "Transformer DI",
    17:  "Convection Heater",
    28:  "Transformer DI 4.0",
    31:  "Transformer 4.0",
    42:  "Transformer DI 3.0 XS",
    46:  "Transformer DI 4.0",
    47:  "Convection Heater",
    49:  "Transformer 4.0",
    71:  "Transformer DI 4.0",
    89:  "Aurus",
# humidifier
    4:   "Electrolux EHU-3910D/EHU-3915D",
    35:  "Electrolux YOGA healthline 2.0",
    81:  "UHB-960 ET",
# ir_heater
    75:  "Aurus Infrared",
# other
    5:   "WFN-02",
    25:  "WFN-02-D4",
    43:  "WFN-02-01/02",
    22:  "Hommyn Hub HH-01",
    97:  "Hommyn-Hub HH-01*",
# thermostat
    29:  "Electrolux/Royal Thermo",
    65:  "SmartControl",
    67:  "Electrolux/Royal Thermo",
    73:  "SmartControl Pro",
    78:  "Electrolux/Royal Thermo",
}

KETTLE_ERROR = {
    0: "no_error",
    1: "low_water",
    2: "kettle_out_of_base",
    3: "temperature_sensor_failure",
    4: "temperature_sensor_failure",
    5: "child_lock",
    6: "recommended_to_change_water",
    7: "changed_water_for_long_time",
}
HUMIDDIFIER_POLARIS_ERROR = {
    0: "no_error",
    1: "low_water",
    2: "child_lock",
    3: "replace_filter",
    4: "maximum_schedules",
    5: "clean_tank",
}
HUMIDDIFIER_RUSCLIMATE_ERROR = {
    0: "no_error",
    1: "temperature_sensor_failure",
    2: "replace_filter",
}