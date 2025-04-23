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
    return presets

def update_presets():
    global available_presets
    available_presets = get_presets()
    return

def get_preset_content(preset):
    preset_json = f'{preset}.json'
    preset_file = ''
    preset_path = Path('.\presets')
    for preset_file in preset_path.rglob(preset_json):
      if not preset_file:
        print(f'Could not find the {preset} preset')
        print()
        return {}
    try:
      with open(preset_file, "r", encoding="utf-8") as json_file:
          json_content = json.load(json_file)
          print(f'Loaded the {preset} preset from {preset_file}')
          return json_content
    except Exception as e:
        print(f'Could not load the {preset} preset from {preset_file}')
        print(e)
    print()
    return {}
