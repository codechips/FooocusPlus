import os
import json
import random
import args_manager
from ldm_patched.modules import model_management
from pathlib import Path

def get_presets_in_folder(arg_folder_name):
    if not arg_folder_name:
        arg_folder_name = category_selection
    presets_in_folder = []
    if os.path.exists(arg_folder_name):
        folder_name = Path(f'.\presets\{arg_folder_name}') 
        presets_in_folder = list(folder_name.rglob('*.json'))
        if not presets_in_folder:
            print(f'Could not find presets in the {arg_folder_name} folder.')
            print()
    else:
        print(f'Could not find the {arg_folder_name} folder.')
        print()        
    return presets_in_folder  

def get_presetnames_in_folder(folder_name):
    presets_in_folder = get_presets_in_folder(folder_name)
    presetnames_in_folder = []
    for file in presets_in_folder:
        presetname, ext = os.path.splitext(file)
        presetnames_in_folder.append(presetname)
    return presetnames_in_folder

def find_preset_file(preset):
    preset_json = f'{preset}.json'
    preset_file = ''
    preset_path = Path('.\presets')
    for preset_file in preset_path.rglob(preset_json):
      if not preset_file:
        print(f'Could not find the {preset} preset')
        print()
        return {}
    return preset_file

def get_preset_paths():    # called by update_files() in modules.config
    preset_path = Path('.\presets')
    presets = list(preset_path.rglob('*.json'))
    if not [presets]:
        print('No presets found')
        presets = ['initial']
        return presets
    return presets

def get_random_preset():
    presets = get_preset_paths()
    preset_random = random.randint(0, (len(presets)-1))
    return presets[preset_random]

category_selection = 'Favorite'
def get_category_selection(arg_category_selection):
    global category_selection
    if category_selection == '':
        category_selection = 'Favorite'
    category_selection = arg_category_selection
    return category_selection

def get_preset_content(preset):
    preset_file = find_preset_file(preset)
    if preset_file:
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

def get_initial_preset_content():
    preset = args_manager.args.preset
    if (preset=='initial' or preset.lower()=='default') and (int(model_management.get_vram())<6000)\
    and (find_preset_file('4GB_Default')):
        preset='4GB_Default'
        args_manager.args.preset = preset
        print('Loading the "4GB_Default" preset, the default for low VRAM systems')
    if not find_preset_file(preset):
        if find_preset_file('Default'):
            preset = 'Default'
        else:
            print('Could not find the startup preset')
            preset = get_random_preset()
            if not preset:
                print('Could not find any presets')
                preset = 'initial'
    json_content = get_preset_content(preset)
    return json_content

def get_preset_foldernames():
    preset_folder = '.\presets'
    preset_foldernames = []
    if os.path.exists(preset_folder):
        preset_foldernames = [f.name for f in os.scandir('.\presets') if f.is_dir()]
    else:
        print(f'Could not find the folder named {folder_name}.')
        print() 
    return preset_foldernames.append('Random')

'''
def get_presets_in_folder(arg_folder_name):
    if not arg_folder_name:
        arg_folder_name = category_selection
    presets_in_folder = []
    if os.path.exists(folder_name):
        folder_name = Path(f'.\presets\{arg_folder_name}') 
        presets_in_folder = list(folder_name.rglob('*.json'))
#        presets_in_folder = [f.name for f in os.scandir(folder_name) if f.is_file(): if f.endswith(".json")]
        if not presets_in_folder:
            print(f'Could not find presets in the {arg_folder_name} folder.')
            print()
    else:
        print(f'Could not find the {arg_folder_name} folder.')
        print()        
    return presets_in_folder  

def get_preset_names():
    preset_folder = '.\presets'
    preset_names = []
    if os.path.exists(preset_folder):
        preset_names = [f.name for f in os.scandir('.\presets') if f.is_file() and f.endswith(".json")]
        if not presets_names:
            print(f'Could not find presets in the {preset_folder} subfolders.')
            print()
    else:
        print(f'Could not find the {folder_name} preset folder.')
        print()
    return preset_names
'''
  
#def update_presets():
#    global available_presets
#    available_presets = get_presets()
#    return
