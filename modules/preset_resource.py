import os
import json
from pathlib import Path

def get_preset_foldernames():
    preset_folder = '.\presets'
    preset_foldernames = []
    if os.path.exists(preset_folder):
        preset_foldernames = [f.name for f in os.scandir('.\presets') if f.is_dir()]
    return preset_foldernames

def get_presets():
    preset_path = Path('.\presets')
    presets = list(preset_path.rglob('*.json'))
    if not [presets]:
        print('No presets found')
        presets = ['initial']
        return presets
    return presets # + [f[:f.index(".json")] for f in os.listdir(preset_folder) if f.endswith('.json')]

def update_presets():
    global available_presets
    available_presets = get_presets()
    return

def try_get_preset_content(preset):
    preset_path = Path('.\presets')
    for preset_path in preset_path.rglob(preset):
      if not preset_path:
        print(f'Could not find the {preset} preset')
        print()
        return
    try:
      with open(preset_path, "r", encoding="utf-8") as json_file:
          json_content = json.load(json_file)
          print(f'Loaded the {preset} preset from {preset_path}')
          return json_content
    except Exception as e:
        print(f'Load not load the {preset} preset from {preset_path}')
        print(e)
    print()
    return {}
