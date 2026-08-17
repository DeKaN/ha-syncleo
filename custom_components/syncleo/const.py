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
FEATURE_DAMPER = "damper"
FEATURE_ECO_AS_SMART_MODE = "energy_saving"
FEATURE_ERROR = "error"
FEATURE_EXPENDABLES_ANODE = "expendables_anode"
FEATURE_EXPENDABLES_FILTER = "expendables_filter"
FEATURE_EXPENDABLES_PREFILTER = "expendables_prefilter"
FEATURE_IONIZATION = "ionization"
FEATURE_KEEP_WARM = "keep_warm"
FEATURE_NIGHT = "night"
FEATURE_POWER_LEVEL = "power_level"
FEATURE_RSSI = "rssi"
FEATURE_SMART_MODE = "smart_mode"
FEATURE_TANK = "tank"
FEATURE_TIMER = "timer"
FEATURE_TURBO = "turbo"
FEATURE_ULTRAVIOLET = "ultraviolet"
FEATURE_VOLUME = "volume"
FEATURE_WARM_STREAM = "warm_stream"

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

PROFILE_TYPE_AC = "ac"
PROFILE_TYPE_AIR_FRYER = "air_fryer"
PROFILE_TYPE_BOILER = "boiler"
PROFILE_TYPE_BREEZER = "breezer"
PROFILE_TYPE_HEATER = "heater"
PROFILE_TYPE_KETTLE = "kettle"

TRANLATION_KEY_CLIMATE = DOMAIN + "_climate"
TRANLATION_KEY_FAN = DOMAIN + "_fan"

ZEROCONF_CURVE = "curve"
ZEROCONF_DEVICE_TYPE = "devtype"
ZEROCONF_MAC_ADDRESS = "macaddr"


POLARIS_DEVICE = {
    0:   {"model": "Unknown", "class": "all"},
    37:  {"model": "PWK-7111CGLD-WIFI", "class": "kettle"},
    245: {"model": "PWK-0105", "class": "kettle"},
    205: {"model": "PWK-1538CC", "class": "kettle"},
    271: {"model": "PWK-1701CGLD", "class": "kettle"},
    36:  {"model": "PWK-17107CGLD-WIFI", "class": "kettle"},
    29:  {"model": "PWK-1712CGLD", "class": "kettle"},
    38:  {"model": "PWK-1712CGLD", "class": "kettle"},
    54:  {"model": "PWK-1712CGLD", "class": "kettle"},
    59:  {"model": "PWK-1712CGLD", "class": "kettle"},
    63:  {"model": "PWK-1712CGLD", "class": "kettle"},
    97:  {"model": "PWK-1712CGLD", "class": "kettle"},
    117: {"model": "PWK-1712CGLD", "class": "kettle"},
    208: {"model": "PWK-1712CGLD", "class": "kettle"},
    83:  {"model": "PWK-1712CGLD-RGB", "class": "kettle"},
    253: {"model": "PWK-1715", "class": "kettle"},
    244: {"model": "PWK-1716CGLD", "class": "kettle"},
    67:  {"model": "PWK-1720CGLD", "class": "kettle"},
    84:  {"model": "PWK-1720CGLD-RGB", "class": "kettle"},
    6:   {"model": "PWK-1725CGLD", "class": "kettle"},
    52:  {"model": "PWK-1725CGLD", "class": "kettle"},
    57:  {"model": "PWK-1725CGLD", "class": "kettle"},
    61:  {"model": "PWK-1725CGLD", "class": "kettle"},
    82:  {"model": "PWK-1725CGLD", "class": "kettle"},
    86:  {"model": "PWK-1725CGLD", "class": "kettle"},
    105: {"model": "PWK-1725CGLD", "class": "kettle"},
    106: {"model": "PWK-1725CGLD", "class": "kettle"},
    177: {"model": "PWK-1725CGLD", "class": "kettle"},
    194: {"model": "PWK-1725CGLD", "class": "kettle"},
    196: {"model": "PWK-1725CGLD", "class": "kettle"},
    164: {"model": "PWK-1728CGLDA", "class": "kettle"},
    209: {"model": "PWK-1729CAD", "class": "kettle"},
    189: {"model": "PWK-1746CA", "class": "kettle"},
    260: {"model": "PWK-1746CA", "class": "kettle"},
    308: {"model": "PWK-1746CA", "class": "kettle"},
    8:   {"model": "PWK-1755CAD", "class": "kettle"},
    53:  {"model": "PWK-1755CAD", "class": "kettle"},
    58:  {"model": "PWK-1755CAD", "class": "kettle"},
    62:  {"model": "PWK-1755CAD", "class": "kettle"},
    185: {"model": "PWK-1755CAD", "class": "kettle"},
    165: {"model": "PWK-1755CAD-VOICE", "class": "kettle"},
    121: {"model": "PWK-1774CAD", "class": "kettle"},
    2:   {"model": "PWK-1775CGLD", "class": "kettle"},
    51:  {"model": "PWK-1775CGLD", "class": "kettle"},
    56:  {"model": "PWK-1775CGLD", "class": "kettle"},
    60:  {"model": "PWK-1775CGLD", "class": "kettle"},
    98:  {"model": "PWK-1775CGLD", "class": "kettle"},
    188: {"model": "PWK-1775CGLD", "class": "kettle"},
    223: {"model": "PWK-1775CGLD", "class": "kettle"},
    262: {"model": "PWK-1775CGLD", "class": "kettle"},
    263: {"model": "PWK-1775CGLD", "class": "kettle"},
    275: {"model": "PWK-1775CGLD", "class": "kettle"},
    294: {"model": "PWK-1775CGLD", "class": "kettle"},
    85:  {"model": "PWK-1775CGLD-SMART", "class": "kettle"},
    139: {"model": "PWK-1775CGLD-VOICE", "class": "kettle"},
    175: {"model": "PWK-1823CGLD", "class": "kettle"},
    254: {"model": "PWK-1823CGLD", "class": "kettle"},
    176: {"model": "PWK-1841CGLD", "class": "kettle"},
    255: {"model": "PWK-1841CGLD", "class": "kettle"},
    147: {"model": "PUH-0205", "class": "humidifier"},
    71:  {"model": "PUH-1010", "class": "humidifier"},
    72:  {"model": "PUH-2300", "class": "humidifier"},
    73:  {"model": "PUH-3030", "class": "humidifier"},
    75:  {"model": "PUH-4040", "class": "humidifier"},
    99:  {"model": "PUH-4040", "class": "humidifier"},
    153: {"model": "PUH-4055", "class": "humidifier"},
    137: {"model": "PUH-4066", "class": "humidifier"},
    157: {"model": "PUH-4550", "class": "humidifier"},
    158: {"model": "PUH-6060", "class": "humidifier"},
    25:  {"model": "PUH-6090", "class": "humidifier"},
    15:  {"model": "PUH-7406", "class": "humidifier"},
    87:  {"model": "PUH-8080_PUH-4606", "class": "humidifier"},
    155: {"model": "PUH-8802", "class": "humidifier"},
    74:  {"model": "PUH-9009", "class": "humidifier"},
    4:   {"model": "PUH-9105_PUH-2709", "class": "humidifier"},
    17:  {"model": "PUH-9105_PUH-2709", "class": "humidifier"},
    18:  {"model": "PUH-9105_PUH-2709", "class": "humidifier"},
    44:  {"model": "PUH-9105_PUH-2709", "class": "humidifier"},
    70:  {"model": "PUH-9105_PUH-2709", "class": "humidifier"},
    1:   {"model": "EVO-0225", "class": "cooker"},
    95:  {"model": "PMC-00000", "class": "cooker"},
    303: {"model": "PMC-0510", "class": "cooker"},
    301: {"model": "PMC-0515", "class": "cooker"},
    10:  {"model": "PMC-0521WIFI", "class": "cooker"},
    41:  {"model": "PMC-0521WIFI", "class": "cooker"},
    267: {"model": "PMC-0521WIFI", "class": "cooker"},
    55:  {"model": "PMC-0524WIFI", "class": "cooker"},
    206: {"model": "PMC-0524WIFI", "class": "cooker"},
    9:   {"model": "PMC-0526WIFI", "class": "cooker"},
    40:  {"model": "PMC-0526WIFI", "class": "cooker"},
    138: {"model": "PMC-0526WIFI", "class": "cooker"},
    39:  {"model": "PMC-0528WIFI", "class": "cooker"},
    48:  {"model": "PMC-0528WIFI", "class": "cooker"},
    268: {"model": "PMC-0528WIFI", "class": "cooker"},
    47:  {"model": "PMC-0530WIFI", "class": "cooker"},
    270: {"model": "PMC-0530WIFI", "class": "cooker"},
    210: {"model": "PMC-0590AD", "class": "cooker"},
    302: {"model": "PMC-0597", "class": "cooker"},
    215: {"model": "PMC-5001WIFI", "class": "cooker"},
    79:  {"model": "PMC-5017WIFI", "class": "cooker"},
    192: {"model": "PMC-5017WIFI", "class": "cooker"},
    80:  {"model": "PMC-5020WIFI", "class": "cooker"},
    266: {"model": "PMC-5020WIFI", "class": "cooker"},
    77:  {"model": "PMC-5040WIFI", "class": "cooker"},
    78:  {"model": "PMC-5050WIFI", "class": "cooker"},
    89:  {"model": "PMC-5055WIFI", "class": "cooker"},
    114: {"model": "PMC-5060-Smart-Motion", "class": "cooker"},
    240: {"model": "PMC-5060-Smart-Motion", "class": "cooker"},
    162: {"model": "PMC-5063WIFI", "class": "cooker"},
    169: {"model": "PPC-1505-WiFI", "class": "cooker"},
    183: {"model": "PPC-1505-WiFI", "class": "cooker"},
    235: {"model": "AM7310", "class": "coffeemaker"},
    305: {"model": "PACM-2072", "class": "coffeemaker"},
    103: {"model": "PACM-2080AC", "class": "coffeemaker"},
    261: {"model": "PACM-2080AC", "class": "coffeemaker"},
    276: {"model": "PACM-2080AC", "class": "coffeemaker"},
    277: {"model": "PACM-2080AC", "class": "coffeemaker"},
    200: {"model": "PACM-2081AC", "class": "coffeemaker"},
    265: {"model": "PACM-2081AC", "class": "coffeemaker"},
    280: {"model": "PACM-2081AC", "class": "coffeemaker"},
    166: {"model": "PACM-2085GC", "class": "coffeemaker"},
    278: {"model": "PACM-2085GC", "class": "coffeemaker"},
    247: {"model": "PCM-1255", "class": "coffeemaker"},
    45:  {"model": "PCM-1540WIFI", "class": "coffeemaker"},
    222: {"model": "PCM-1540WIFI", "class": "coffeemaker"},
    274: {"model": "PCM-1540WIFI", "class": "coffeemaker"},
    279: {"model": "PCM-1540WIFI", "class": "coffeemaker"},
    190: {"model": "PCM-1560", "class": "coffeemaker"},
    207: {"model": "PCM-2070CG", "class": "coffeemaker"},
    172: {"model": "PAW-0804", "class": "air_cleaner"},
    140: {"model": "PAW-0804", "class": "air_cleaner"},
    151: {"model": "PPA-2025", "class": "air_cleaner"},
    203: {"model": "PPA-2025", "class": "air_cleaner"},
    250: {"model": "PPA-2025", "class": "air_cleaner"},
    152: {"model": "PPA-4050", "class": "air_cleaner"},
    204: {"model": "PPA-4050", "class": "air_cleaner"},
    251: {"model": "PPA-4050", "class": "air_cleaner"},
    236: {"model": "PPAT-02A", "class": "air_cleaner"},
    238: {"model": "PPAT-80P", "class": "air_cleaner"},
    239: {"model": "PPAT-90GDi", "class": "air_cleaner"},
    132: {"model": "PWF-2005", "class": "irrigator"},
    252: {"model": "PWF-2005", "class": "irrigator"},
    273: {"model": "PAF-4001WIFI", "class": "air_fryer"},
    290: {"model": "PAF-6003WIFI", "class": "air_fryer"},
    291: {"model": "PAF-8003WIFI", "class": "air_fryer"},
    292: {"model": "PAF-8005WIFI", "class": "air_fryer"},
    31:  {"model": "ENIGMA-WI-FI", "class": "boiler"},
    11:  {"model": "PWH-IDF06", "class": "boiler"},
    30:  {"model": "SIGMA-WIFI", "class": "boiler"},
    249: {"model": "VEKTOR-WIFI", "class": "boiler"},
    46:  {"model": "PCH-0320WIFI", "class": "heater"},
    65:  {"model": "PCH-0320WIFI", "class": "heater"},
    16:  {"model": "PHV-1401", "class": "heater"},
    49:  {"model": "PMH-21XX", "class": "heater"},
    64:  {"model": "PMH-21XX", "class": "heater"},
    101: {"model": "PVCR-0726-Aqua", "class": "cleaner"},
    108: {"model": "PVCR-0726-GYRO", "class": "cleaner"},
    21:  {"model": "PVCR-0735", "class": "cleaner"},
    163: {"model": "PVCR-0735", "class": "cleaner"},
    19:  {"model": "PVCR-0833", "class": "cleaner"},
    43:  {"model": "PVCR-0833", "class": "cleaner"},
    104: {"model": "PVCR-0905", "class": "cleaner"},
    156: {"model": "PVCR-0905", "class": "cleaner"},
    107: {"model": "PVCR-0926", "class": "cleaner"},
    23:  {"model": "PVCR-1028", "class": "cleaner"},
    22:  {"model": "PVCR-1050", "class": "cleaner"},
    102: {"model": "PVCR-1226-Aqua", "class": "cleaner"},
    109: {"model": "PVCR-1226-GYRO", "class": "cleaner"},
    24:  {"model": "PVCR-1229", "class": "cleaner"},
    68:  {"model": "PVCR-3100", "class": "cleaner"},
    7:   {"model": "PVCR-3200", "class": "cleaner"},
    76:  {"model": "PVCR-3200", "class": "cleaner"},
    115: {"model": "PVCR-3200", "class": "cleaner"},
    12:  {"model": "PVCR-3300", "class": "cleaner"},
    81:  {"model": "PVCR-3400", "class": "cleaner"},
    130: {"model": "PVCR-3600", "class": "cleaner"},
    112: {"model": "PVCR-3700", "class": "cleaner"},
    88:  {"model": "PVCR-3800", "class": "cleaner"},
    66:  {"model": "PVCR-3900", "class": "cleaner"},
    131: {"model": "PVCR-3900", "class": "cleaner"},
    113: {"model": "PVCR-4000", "class": "cleaner"},
    197: {"model": "PVCR-4000", "class": "cleaner"},
    110: {"model": "PVCR-4105", "class": "cleaner"},
    127: {"model": "PVCR-4105", "class": "cleaner"},
    199: {"model": "PVCR-4250", "class": "cleaner"},
    241: {"model": "PVCR-4250", "class": "cleaner"},
    211: {"model": "PVCR-4260", "class": "cleaner"},
    269: {"model": "PVCR-4260", "class": "cleaner"},
    142: {"model": "PVCR-4500", "class": "cleaner"},
    195: {"model": "PVCR-4500", "class": "cleaner"},
    307: {"model": "PVCR-4750", "class": "cleaner"},
    119: {"model": "PVCR-5001", "class": "cleaner"},
    146: {"model": "PVCR-5001", "class": "cleaner"},
    154: {"model": "PVCR-5001", "class": "cleaner"},
    201: {"model": "PVCR-5003", "class": "cleaner"},
    242: {"model": "PVCR-5005", "class": "cleaner"},
    123: {"model": "PVCR-6001", "class": "cleaner"},
    148: {"model": "PVCR-6001", "class": "cleaner"},
    221: {"model": "PVCR-6001", "class": "cleaner"},
    187: {"model": "PVCR-6003", "class": "cleaner"},
    256: {"model": "PVCR-7026", "class": "cleaner"},
    128: {"model": "PVCRAC-7050", "class": "cleaner"},
    212: {"model": "PVCRAC-7290", "class": "cleaner"},
    178: {"model": "PVCRAC-7750", "class": "cleaner"},
    198: {"model": "PVCRAC-7790", "class": "cleaner"},
    264: {"model": "PVCRAC-7790", "class": "cleaner"},
    126: {"model": "PVCRDC-0101", "class": "cleaner"},
    160: {"model": "PVCRDC-0101", "class": "cleaner"},
    124: {"model": "PVCRDC-5002", "class": "cleaner"},
    149: {"model": "PVCRDC-5002", "class": "cleaner"},
    213: {"model": "PVCRDC-5002", "class": "cleaner"},
    202: {"model": "PVCRDC-5004", "class": "cleaner"},
    181: {"model": "PVCRDC-5006", "class": "cleaner"},
    125: {"model": "PVCRDC-6002", "class": "cleaner"},
    150: {"model": "PVCRDC-6002", "class": "cleaner"},
    186: {"model": "PVCRDC-6004", "class": "cleaner"},
    257: {"model": "PVCRDC-7028", "class": "cleaner"},
    217: {"model": "PVCRDC-G2-5002", "class": "cleaner"},
    218: {"model": "PVCRDC-G2-6002", "class": "cleaner"},
    133: {"model": "PVCR-G2-0726W", "class": "cleaner"},
    193: {"model": "PVCR-G2-0826", "class": "cleaner"},
    134: {"model": "PVCR-G2-0926W", "class": "cleaner"},
    135: {"model": "PVCR-G2-1226", "class": "cleaner"},
    129: {"model": "PVCR-G2-3200", "class": "cleaner"},
    122: {"model": "PVCR-G2-3600", "class": "cleaner"},
    219: {"model": "PVCR-G2-5001", "class": "cleaner"},
    220: {"model": "PVCR-G2-6001", "class": "cleaner"},
    100: {"model": "PVCR-Wave-15", "class": "cleaner"},
    246: {"model": "PRWC-3001", "class": "window_cleaner"},
    93:  {"model": "PHB-1350-WIFI", "class": "blender"},
    35:  {"model": "PHB-1503-WIFI", "class": "blender"},
    34:  {"model": "PHB-1551-WIFI", "class": "blender"},
    282: {"model": "induction-hob", "class": "cooktop"},
    286: {"model": "XFC302I-B3SF", "class": "cooktop"},
    288: {"model": "XFC302T-B1D", "class": "cooktop"},
    285: {"model": "XFC604I", "class": "cooktop"},
    304: {"model": "XFC604I-(test)", "class": "cooktop"},
    284: {"model": "XFC604I-B8F", "class": "cooktop"},
    287: {"model": "XFC604T-B7D", "class": "cooktop"},
    289: {"model": "XFG640F-B3P", "class": "cooktop"},
    111: {"model": "PVCS-1150", "class": "cordless_cleaner"},
    90:  {"model": "PVCS-2090", "class": "cordless_cleaner"},
    136: {"model": "PVCS-4070", "class": "cordless_cleaner"},
    229: {"model": "PVCS-4070", "class": "cordless_cleaner"},
    232: {"model": "PVCS-6020", "class": "cordless_cleaner"},
    281: {"model": "PVCS-6020", "class": "cordless_cleaner"},
    230: {"model": "PVCS-8200", "class": "cordless_cleaner"},
    234: {"model": "PVCSDC-3000", "class": "cordless_cleaner"},
    233: {"model": "PVCSDC-3005", "class": "cordless_cleaner"},
    306: {"model": "PVCSDC-3005", "class": "cordless_cleaner"},
    180: {"model": "PSF-3315", "class": "fan"},
    248: {"model": "PSF-4025", "class": "fan"},
    179: {"model": "PGP-3010-SMOKELESS", "class": "grill"},
    96:  {"model": "PGP-4001", "class": "grill"},
    120: {"model": "PHD-4000", "class": "hair_care"},
    184: {"model": "PHS-1300", "class": "hair_care"},
    171: {"model": "PHSB-5000DF", "class": "hair_care"},
    145: {"model": "PHSC-1234", "class": "hair_care"},
    297: {"model": "8006", "class": "hood"},
    296: {"model": "8029", "class": "hood"},
    295: {"model": "6065A-600", "class": "hood"},
    283: {"model": "PGS-2250VA", "class": "iron"},
    91:  {"model": "PIR-2624AK-3m", "class": "iron"},
    161: {"model": "PIR-3074SG", "class": "iron"},
    173: {"model": "PIR-3210AK-3m", "class": "iron"},
    174: {"model": "PIR-3225AK-3m", "class": "iron"},
    191: {"model": "PSS-2002K", "class": "iron"},
    259: {"model": "PSS-8010K", "class": "iron"},
    159: {"model": "PSS-9090K", "class": "iron"},
    237: {"model": "SM-8095", "class": "kitchen_machine"},
    272: {"model": "SM-8095", "class": "kitchen_machine"},
    32:  {"model": "PMG-2580", "class": "meat_grinder"},
    216: {"model": "PMG-3060", "class": "meat_grinder"},
    116: {"model": "Smart-Lid", "class": "other"},
    299: {"model": "xbcook55", "class": "oven"},
    300: {"model": "xbcook56", "class": "oven"},
    298: {"model": "xbcook62", "class": "oven"},
    92:  {"model": "PGS-1450CWIFI", "class": "steamer"},
    94:  {"model": "PSS-7070KWIFI", "class": "steamer"},
    50:  {"model": "PETB-0202TC", "class": "toothbrush"},
}
HOMMYN_DEVICE = {
    0:   {"model": "Unknown", "class": "all"},
    1:   {"model": "Electrolux-EAP-1040D_1055D", "class": "air_cleaner"},
    26:  {"model": "Electrolux-EAP-2050D_2075D", "class": "air_cleaner"},
    3:   {"model": "Ballu-ONEAIR-ASP-200", "class": "ventilation"},
    30:  {"model": "Ballu-ONEAIR-ASP-200S", "class": "ventilation"},
    32:  {"model": "Ballu-ASP-100_Electrolux-EASP-100", "class": "ventilation"},
    34:  {"model": "Electrolux-EPVS_ERVX-inv", "class": "ventilation"},
    36:  {"model": "Electrolux-EPVS_ERVX-inv", "class": "ventilation"},
    59:  {"model": "Ballu-ONEAIR-ASP-200S", "class": "ventilation"},
    69:  {"model": "Ballu-ASP-100_Electrolux-EASP-100", "class": "ventilation"},
    98:  {"model": "Shuft-Allston-VH_ERV", "class": "ventilation"},
    100: {"model": "Shuft-Allston-VH_ERV", "class": "ventilation"},
    102: {"model": "Ballu-ONEAIR-ASP-90", "class": "ventilation"},
    105: {"model": "Ballu-ONEAIR-ASP-90", "class": "ventilation"},
    106: {"model": "Ballu-ONEAIR-ASP-90", "class": "ventilation"},
    107: {"model": "Ballu-ONEAIR-ASP-90", "class": "ventilation"},
    27:  {"model": "Ballu-RDU-ANTICOVID-generator", "class": "recirculator"},
    8:   {"model": "Electrolux-Atrium-DC_Zanussi-Siena-DC_Ballu-Lagoon", "class": "air_conditioner"},
    10:  {"model": "Zanussi-Massimo-Solar", "class": "air_conditioner"},
    13:  {"model": "Electrolux-Smartline_Ballu-Eco-Smart_Ice-Peak", "class": "air_conditioner"},
    15:  {"model": "Electrolux-Viking-DC_Zanussi-Perfecto-DC_Ballu-Greenland-DC", "class": "air_conditioner"},
    20:  {"model": "Ballu-Platinum-Evol-DC_Olympio-Legend", "class": "air_conditioner"},
    21:  {"model": "Zanussi-Moderno-DC_Electrolux-Loft-DC", "class": "air_conditioner"},
    38:  {"model": "Toshiba-Shorai-EE", "class": "air_conditioner"},
    41:  {"model": "Electrolux-Monaco-DC", "class": "air_conditioner"},
    51:  {"model": "Zanussi-Massimo-Solar-2023", "class": "air_conditioner"},
    55:  {"model": "Zanussi-Barocco-DC_Royal-Thermo-Barocco-DC", "class": "air_conditioner"},
    56:  {"model": "Toshiba", "class": "air_conditioner"},
    57:  {"model": "Shuft-Berg_MBO-M-1", "class": "air_conditioner"},
    60:  {"model": "Ballu-Discovery-DC", "class": "air_conditioner"},
    68:  {"model": "Electrolux-Loft-DC_Ballu-Platinum-Black-DC", "class": "air_conditioner"},
    70:  {"model": "Ballu-Universal-3_DC_Free-Match", "class": "air_conditioner"},
    72:  {"model": "Zanussi-Barocco_Royal-Thermo-Barocco", "class": "air_conditioner"},
    82:  {"model": "Goldstar-GSAC_GSACI", "class": "air_conditioner"},
    83:  {"model": "Ballu-Aura", "class": "air_conditioner"},
    84:  {"model": "Ballu-Aura", "class": "air_conditioner"},
    85:  {"model": "Aurus-D", "class": "air_conditioner"},
    95:  {"model": "Climer-Dresden", "class": "air_conditioner"},
    99:  {"model": "AURUS-A", "class": "air_conditioner"},
    108: {"model": "Royal-Thermo-Diamond-DC", "class": "air_conditioner"},
    2:   {"model": "SmartInverter", "class": "boiler"},
    7:   {"model": "Zanussi-Artendo_Azurro-PRO", "class": "boiler"},
    12:  {"model": "Electrolux-Centurio-IQ-2_Maximus", "class": "boiler"},
    16:  {"model": "Ballu-Smart", "class": "boiler"},
    18:  {"model": "Electrolux-Maximus_Megapolis_Zanussi-Splendore-XP-2_Artendo-PRO-C", "class": "boiler"},
    19:  {"model": "Electrolux-Regency", "class": "boiler"},
    33:  {"model": "Electrolux-Centurio-IQ-3", "class": "boiler"},
    44:  {"model": "Royal-Thermo-Aqua-Inverter_Royal-Thermo-Aqua-Inox-Inverter", "class": "boiler"},
    74:  {"model": "Aurus-S", "class": "boiler"},
    76:  {"model": "Electrolux-Royal-Flash_Centurio-IQ-Inverter", "class": "boiler"},
    77:  {"model": "Royal-Thermo-Major-Inverter_Smalto-Inverter", "class": "boiler"},
    80:  {"model": "Aurus-F", "class": "boiler"},
    90:  {"model": "Ballu-Cetrion-Inverter_Ballu-Cetrion-Inox-Inverter", "class": "boiler"},
    91:  {"model": "Royal-Thermo-Regency", "class": "boiler"},
    50:  {"model": "Electrolux-3D-Fireplace", "class": "fireplace"},
    6:   {"model": "Transformer-DI-3", "class": "heater"},
    9:   {"model": "Transformer-DI-3-S", "class": "heater"},
    11:  {"model": "Ballu-Rapid", "class": "heater"},
    14:  {"model": "Transformer-DI", "class": "heater"},
    17:  {"model": "Convection-Heater", "class": "heater"},
    28:  {"model": "Transformer-DI-4", "class": "heater"},
    31:  {"model": "Transformer-4", "class": "heater"},
    42:  {"model": "Transformer-DI-3-XS", "class": "heater"},
    46:  {"model": "Transformer-DI-4", "class": "heater"},
    47:  {"model": "Convection-Heater", "class": "heater"},
    49:  {"model": "Transformer-4", "class": "heater"},
    71:  {"model": "Transformer-DI-4", "class": "heater"},
    89:  {"model": "Aurus", "class": "heater"},
    4:   {"model": "Electrolux-EHU-3910D_EHU-3915D", "class": "humidifier"},
    35:  {"model": "Electrolux-YOGA-healthline-2", "class": "humidifier"},
    81:  {"model": "UHB-960-ET", "class": "humidifier"},
    75:  {"model": "Aurus-Infrared", "class": "ir_heater"},
    5:   {"model": "WFN-02", "class": "other"},
    25:  {"model": "WFN-02-D4", "class": "other"},
    43:  {"model": "WFN-02-01_02", "class": "other"},
    22:  {"model": "Hommyn-Hub-HH-01", "class": "other"},
    97:  {"model": "Hommyn-Hub-HH-01*", "class": "other"},
    29:  {"model": "Electrolux_Royal-Thermo", "class": "thermostat"},
    65:  {"model": "SmartControl", "class": "thermostat"},
    67:  {"model": "Electrolux_Royal-Thermo", "class": "thermostat"},
    73:  {"model": "SmartControl-Pro", "class": "thermostat"},
    78:  {"model": "Electrolux_Royal-Thermo", "class": "thermostat"},
}