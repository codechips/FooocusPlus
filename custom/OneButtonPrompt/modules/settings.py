import json
from os.path import exists
#from custom.OneButtonPrompt.shared import path_manager
from custom.OneButtonPrompt.utils import path_fixed

DEFAULT_SETTINGS = {
    "OBP_preset": "Standard",
    "hint_chance": 25,
}


def load_settings():
    if exists(path_fixed("settings/settings.json")):
        with open(path_fixed("settings/settings.json")) as f:
            settings = json.load(f)
    else:
        settings = {}

    # Add any missing default settings
    changed = False
    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value
            changed = True

    if changed:
        with open(path_fixed("settings/settings.json"), "w") as f:
            json.dump(settings, f, indent=2)

    return settings


default_settings = load_settings()
