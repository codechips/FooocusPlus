import os
import json
from pathlib import Path


category_selection = 'Favorite'
def get_category_selection(arg_category_selection):
    global category_selection
    if category_selection == '':
        category_selection = 'Favorite'
    category_selection = arg_category_selection
    return category_selection

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

def get_preset_foldernames():
    preset_folder = '.\presets'
    preset_foldernames = []
    if os.path.exists(preset_folder):
        preset_foldernames = [f.name for f in os.scandir('.\presets') if f.is_dir()]
    return preset_foldernames

def get_presets_in_folder(folder_name):
    if not folder_name:
        folder_name = category_selection
    preset_folder = []
    if os.path.exists(folder_name):
        presets_in_folder = [f.name for f in os.scandir('.\presets') if f.is_file() and f.endswith(".json")]
        if not presets_in_folder:
            print(f'Could not find presets in the {folder_name} folder.')
            print()
    return presets_in_folder  

def get_presetnames_in_folder(folder_name):
    presets_in_folder = get_presets_in_folder(folder_name)
    for file in presets_in_folder:
        presetname, ext = os.path.splitext(file)
        presetnames_in_folder.append(presetname)
    return presetnames_in_folder

def get_preset_names():
    preset_folder = '.\presets'
    preset_names = []
    if os.path.exists(preset_folder):
        preset_names = [f.name for f in os.scandir('.\presets') if f.is_file() and f.endswith(".json")]
        if not presets_names:
            print(f'Could not find presets in the {preset_folder} subfolders.')
            print()
    return preset_names

def get_preset_paths():    # called by update_files() in modules.config
    preset_path = Path('.\presets')
    presets = list(preset_path.rglob('*.json'))
    if not [presets]:
        print('No presets found')
        presets = ['initial']
        return presets
    return presets

#def update_presets():
#    global available_presets
#    available_presets = get_presets()
#    return
