import os
import json
import random
import gradio as gr
import args_manager
from ldm_patched.modules import model_management
from pathlib import Path

current_preset = args_manager.args.preset

def find_preset_file(preset):
    if os.path.splitext(preset)[1] == 'json':
        preset_json = preset
    else:
        preset_json = f'{preset}.json'
    preset_file = ''
    preset_path = Path('.\presets')
    for preset_file in preset_path.rglob(preset_json):
      if not preset_file:
        print(f'Could not find the {preset} preset')
        print()
        return {}
    return preset_file

def find_preset_folder(preset):
    preset_file = find_preset_file(preset)
    preset_folder = os.path.dirname(preset_file)
    return preset_folder

category_selection = find_preset_folder(current_preset)

def get_preset_paths():              # called by update_files() in modules.config
    preset_path = Path('.\presets')  # also used to check if preset files exist
    presets = list(preset_path.rglob('*.json'))
    if not [presets]:
        print('No presets found')
        presets = ['initial']
        return presets
    return presets

def get_random_preset_and_category():
    presets = get_preset_paths()
    random_index = random.randint(0, (len(presets)-1))
    file_path = presets[random_index]
    random_category = os.path.basename(os.path.dirname(file_path))
    file_path = Path(file_path)
    random_preset = file_path.stem
    print()
    print(f'Selected the {random_preset} preset at random')
    print(f'{random_preset} is in the {random_category} category')
    return random_category, random_preset

def get_presets_in_folder(arg_folder_name):
    if not arg_folder_name:
        arg_folder_name = category_selection
    if arg_folder_name == '.\presets':
        arg_folder_name = ''
    presets_in_folder = []
    if os.path.basename(os.path.dirname(arg_folder_name)) == 'presets':
        folder_name = Path(arg_folder_name)
    else:
        folder_name = Path(f'.\presets\{arg_folder_name}')
    if os.path.exists(folder_name):
        presets_in_folder = list(folder_name.rglob('*.json'))
        if not presets_in_folder:
            print(f'Could not find presets in the {arg_folder_name} folder.')
            print()
    else:
        print(f'Could not find the {arg_folder_name} folder.')
        print()        
    return presets_in_folder  

def get_presetnames_in_folder(folder_name):
    presetnames_in_folder = []
    if folder_name == 'All':
        folder_name = '.\presets'
    presets_in_folder = get_presets_in_folder(folder_name)
    if presets_in_folder:
        for preset_file in presets_in_folder:
            presetname = Path(preset_file)
            presetnames_in_folder.append(presetname.stem)
        if folder_name == '.\presets': # if we are listing files in all folders
            temp_set = set(presetnames_in_folder)    # then remove duplicates
            presetnames_in_folder = sorted(temp_set) # now convert back to a list
    return presetnames_in_folder

def get_all_presetnames():
    return get_presetnames_in_folder('.\presets')

def set_category_selection(arg_category_selection):
    global category_selection
    if arg_category_selection == '':
        category_selection = 'Favorite'
    category_selection = arg_category_selection
    if category_selection == 'Random':
        category_selection, preset_value = get_random_preset_and_category()
        preset_choices = get_presetnames_in_folder(category_selection)
    else:
        preset_choices = get_presetnames_in_folder(category_selection)
        if current_preset in preset_choices:
            preset_value = current_preset
        else:
            preset_value = preset_choices[0]
    return gr.update(value=category_selection),\
        gr.update(choices=preset_choices, value=preset_value),\
        gr.update(value=preset_value)

def set_preset_selection(arg_preset_selection):
    global current_preset
    if arg_preset_selection == '':
        if current_preset == '':
            current_preset = args_manager.args.preset
        print(f'Using the {current_preset} preset...')
    elif current_preset == arg_preset_selection:
        print()
        print(f'Continuing with the {current_preset} preset...')
    else:
        print(f'Changed the preset from {current_preset} to {arg_preset_selection}')
        current_preset = arg_preset_selection  # updated the current preset tracker
    preset_names = get_all_presetnames()
    preset_index = preset_names.index(current_preset)
    return gr.update(value=current_preset),\
        gr.update(value = preset_names[preset_index]),\
        gr.update(value=current_preset)

def get_preset_content(preset):
    preset_file = find_preset_file(preset)
    if preset_file:
        try:
          with open(preset_file, "r", encoding="utf-8") as json_file:
              json_content = json.load(json_file)
              print(f'Loaded the {preset} preset content from {preset_file}')
              return json_content
        except Exception as e:
            print(f'Could not load the {preset} preset content from {preset_file}')
            print(e)
        print()
    return {}

def get_initial_preset_content():
    global current_preset, category_selection
    json_content = ''
    preset = args_manager.args.preset
    if (preset=='initial' or preset.lower()=='default')\
    and (int(model_management.get_vram())<6000)\
    and (find_preset_file('4GB_Default')):
        preset='4GB_Default'
        print('Loading the "4GB_Default" preset, the default for low VRAM systems')
    if not find_preset_file(preset):
        if find_preset_file('Default'):
            preset = 'Default'
        else:
            print('Could not find the startup preset')
            category_selection = 'Random'
            if not preset:
                print('Could not find any presets')
                current_preset = 'initial'
    if category_selection != 'Random' and current_preset != 'initial':
        args_manager.args.preset = preset
        current_preset = preset
        category_selection = find_preset_folder(preset)
    if current_preset != 'initial':
        set_category_selection(category_selection)
        json_content = get_preset_content(current_preset)
    return json_content

def get_preset_foldernames():
    preset_folder = '.\presets'
    preset_foldernames = []
    if os.path.exists(preset_folder):
        preset_foldernames = [f.name for f in os.scandir(preset_folder) if f.is_dir()]
        if not preset_foldernames:
            print(f'Could not find any preset subfolders in {preset_folder}')
            print()
            return preset_foldernames
    else:
        print(f'Could not find the {preset_folder} folder')
        print()
    return preset_foldernames

def get_preset_categories():
    preset_categories = get_preset_foldernames()
    if preset_categories:
        preset_categories.append('All')    
        preset_categories.append('Random')
        preset_categories.sort()
    return preset_categories

def preset_count():
    return len(get_preset_paths())

def favorite_count():
    preset_favorites = get_presets_in_folder('Favorite')
    return len(preset_favorites)

'''
if not args_manager.args.disable_preset_selection:
    def preset_selection_change(preset, is_generating, inpaint_mode):
        print()
        if PR.current_preset == preset:
            print(f'Continuing with the {preset} preset...')
        else:
            print(f'Changed the preset from {PR.current_preset} to {preset}')
            PR.current_preset = preset    # updated the current preset tracker
        preset_content = PR.get_preset_content(preset) if preset != 'initial' else {}
        preset_prepared = modules.meta_parser.parse_meta_from_preset(preset_content)

        default_model = preset_prepared.get('base_model')
        previous_default_models = preset_prepared.get('previous_default_models', [])
        checkpoint_downloads = preset_prepared.get('checkpoint_downloads', {})
        embeddings_downloads = preset_prepared.get('embeddings_downloads', {})
        lora_downloads = preset_prepared.get('lora_downloads', {})
        vae_downloads = preset_prepared.get('vae_downloads', {})

        preset_prepared['base_model'], preset_prepared['checkpoint_downloads'] = UIS.download_models(
            default_model, previous_default_models, checkpoint_downloads, embeddings_downloads, lora_downloads,
            vae_downloads)

        if 'prompt' in preset_prepared and preset_prepared.get('prompt') == '':
            preset_prepared.update({'prompt': common.POSITIVE})
            prompt = common.POSITIVE

        if 'negative_prompt' in preset_prepared and preset_prepared.get('negative_prompt') == '':
            preset_prepared.update({'negative_prompt': common.NEGATIVE})
            negative_prompt = common.NEGATIVE
        
        return modules.meta_parser.load_parameter_button_click(json.dumps(preset_prepared), is_generating, inpaint_mode)


preset_selection.change(preset_selection_change, inputs=[preset_selection, state_is_generating, inpaint_mode],\
            outputs=[preset_textbox, load_data_outputs], queue=False, show_progress=True) \
        .then(fn=style_sorter.sort_styles, inputs=style_selections, outputs=style_selections, queue=False, show_progress=False) \
        .then(lambda: None, _js='()=>{refresh_style_localization();}') \
        .then(inpaint_engine_state_change, inputs=[inpaint_engine_state] + enhance_inpaint_mode_ctrls,\
            outputs=enhance_inpaint_engine_ctrls, queue=False, show_progress=False)
'''
