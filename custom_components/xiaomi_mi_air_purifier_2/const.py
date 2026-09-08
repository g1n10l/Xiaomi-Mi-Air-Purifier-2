"""Constants for the Xiaomi Mi Air Purifier 2 integration."""

from datetime import timedelta

DOMAIN = "xiaomi_mi_air_purifier_2"
MANUFACTURER = "Xiaomi"
NAME = "Xiaomi Mi Air Purifier 2"
CONF_TOKEN = "token"
PLATFORMS = ["binary_sensor", "fan", "number", "select", "sensor", "switch"]
UPDATE_INTERVAL = timedelta(seconds=30)
SUPPORTED_MODELS = {
    "zhimi.airpurifier.m1",
    "zhimi.airpurifier.m2",
    "zhimi.airpurifier.ma1",
    "zhimi.airpurifier.ma2",
}
