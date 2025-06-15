import os
import shutil
from pathlib import Path


def copy_dirs(arg_source, arg_dest): # dirs including files
    source_path = Path(arg_source)
    dest_path = Path(arg_dest)
    shutil.copytree(source_path, dest_path, dirs_exist_ok = True)
    return

def copy_dir_structure(arg_source, arg_dest): # dirs without files
    source_path = Path(arg_source)
    dest_path = Path(arg_dest)
    for item in source_path.glob("**/*"):
        if item.is_dir():
            new_dir = dest_path / item.relative_to(source_path)
            new_dir.mkdir(parents = True, exist_ok = True)

def empty_dir(arg_dir):
    result = True
    empty_path = Path(arg_dir)
    try:
        for item in empty_path.iterdir():
            if item.is_file():
                item.unlink(missing_ok=True)
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
    except Exception as e:
        print(f'Could not to delete {empty_path}. Reason: {e}')
        result = False
    return result

def find_dir_path(search_dir, find_dir):
    search_path = Path(search_dir)
    str_find_dir = str(find_dir)
    for dir_path in search_path.rglob(str_find_dir):
        return dir_path
    return ''

def find_file_path(search_dir, filename):
    search_path = Path(search_dir)
    str_filename = str(filename)
    for file_path in search_path.rglob(str_filename):
        return file_path
    return ''

def make_dir(arg_dir):
    make_path = Path(arg_dir)
    if not make_path.is_dir():
        try:
            make_path.mkdir(parents = True, exist_ok = True)
        except Exception as e:
            print(f'The {make_path} directory could not be created because: {error}')
    return

def remove_empty_dir(arg_dir):
    remove_empty_path = Path(arg_dir)
    if remove_empty_path.is_dir() and not any(remove_empty_path.iterdir()):
        remove_empty_path.rmdir()
    return

def remove_dirs(arg_dir):
    remove_path = Path(arg_dir)
    if remove_path.is_dir():
        shutil.rmtree(remove_path, ignore_errors=True)
    return

def remove_file(arg_file):
    remove_file_path = Path(arg_file)
    remove_file_path.unlink(missing_ok=True)
    return

def remove_obsolete_flux_folder(arg_parent_str):
    # remove obsolete Flux folder if empty
    checkpoint_path = Path(arg_parent_str)
    old_flux_path = Path(checkpoint_path/'Flux')
    old_flux_file = Path(old_flux_path/'put_flux_base_models_here')
    remove_file(old_flux_file)
    remove_empty_dir(old_flux_path)


def cleanup_structure(directml=False, python_embedded_path=''):
    # cleanup an error condition from version 1.0.0
    remove_dirs('python_embedded')

    # if python_embedded, remove directml if not required, 1.0.3
    if python_embedded_path.is_dir() and not directml:
        site_packages = Path(python_embedded_path/'Lib/site-packages')
        remove_path = find_dir_path(site_packages, 'torch_directml-0.2.5.dev240914.dist-info')
        if remove_path:
            print('Removing obsolete torch_directml files')
            remove_dirs(remove_path)
            remove_dirs(Path(site_packages/'torch_directml'))
            remove_file(Path(site_packages/'torch_directml_native.cp310-win_amd64.pyd'))

    # remove UserDir from repo, an error from 1.0.3
    remove_dirs('UserDir')


def create_model_structure(paths_checkpoints, paths_loras):

    # remove obsolete Flux folders if empty, effective 1.0.1
    remove_obsolete_flux_folder(paths_checkpoints[0])
    if len(paths_checkpoints) > 1:
        remove_obsolete_flux_folder(paths_checkpoints[1])

    # ensure that all the special model directories exist
    # and this will initialize shared model storage outside of UserDir
    checkpoint0_path = Path(paths_checkpoints[0])
    make_dir(checkpoint0_path/'Alternative')
    make_dir(checkpoint0_path/'FluxDev')
    make_dir(checkpoint0_path/'FluxSchnell')
    make_dir(checkpoint0_path/'LowVRAM')
    make_dir(checkpoint0_path/'Pony')
    make_dir(checkpoint0_path/'SD1.5')
    make_dir(checkpoint0_path/'SD3x')

    # ensure that the special LoRA directories exist
    loras0_path = Path(paths_loras[0])
    make_dir(loras0_path/'Alternative')
    make_dir(loras0_path/'Flux')
    make_dir(loras0_path/'Pony')
    make_dir(loras0_path/'SD1.5')
    make_dir(loras0_path/'SD3x')

    return


def create_user_structure(user_dir):

    # initialize the user directory, user_dir
    user_dir_path = Path(user_dir)
    print(f'Initialized the user folder at {user_dir_path}')
    copy_dirs('masters/master_batch_startups', user_dir_path/'batch_startups')
    copy_dirs('masters/master_control_images', user_dir_path/'control_images')
    copy_dirs('masters/master_welcome_images', user_dir_path/'welcome_images')
    copy_dirs('masters/master_wildcards', user_dir_path/'wildcards')

    # delete the contents of user_dir/master_topics to get a clean start
    # copy the contents of '.masters/master_topics' to user_dir for the user's reference only
    master_topics_path = Path('masters/master_topics')
    ref_master_topics_path = Path(user_dir_path/'master_topics')
    remove_dirs(ref_master_topics_path)
    copy_dirs(master_topics_path, ref_master_topics_path)

    # delete './custom/OneButtonPrompt/random_prompt/userfiles'
    # which is used as a temporary working folder
    # initialize 'userfiles' with the contents of '.masters/master_topics'
    working_topics_path = Path('custom/OneButtonPrompt/random_prompt/userfiles')
    remove_dirs(working_topics_path)
    copy_dirs(master_topics_path, working_topics_path)

    # overwrite 'userfiles' with the contents of user_dir './user_topics'
    # this allows a user to completely customize the available topics, if desired
    user_topics_path = Path(user_dir_path/'user_topics')
    make_dir(user_topics_path)
    copy_dirs(user_topics_path, working_topics_path)
    print('Updated the working Random Prompt (OneButtonPrompt) topics folder:')
    print(f'  {working_topics_path.resolve()}')


    # in a similar way, initialize the Presets structure
    master_presets_path = Path('masters/master_presets')
    ref_master_presets_path = Path(user_dir_path/'master_presets')
    remove_dirs(ref_master_presets_path)
    copy_dirs(master_presets_path, ref_master_presets_path)

    working_presets_path = Path('presets')
    remove_dirs(working_presets_path)
    copy_dirs(master_presets_path, working_presets_path)

    user_presets_path = Path(user_dir_path/'user_presets')
    make_dir(user_presets_path)
    copy_dir_structure(master_presets_path, user_presets_path)
    copy_dirs(user_presets_path, working_presets_path)
    print(f'Updated the working preset folder: {working_presets_path.resolve()}')


    # and finally, initialize the Styles structure
    master_styles_path = Path('masters/master_styles')
    ref_master_styles_path = Path(user_dir_path/'master_styles')
    remove_dirs(ref_master_styles_path)
    copy_dirs(master_styles_path, ref_master_styles_path)

    working_styles_path = Path('sdxl_styles')
    remove_dirs(working_styles_path)
    copy_dirs(master_styles_path, working_styles_path)

    user_styles_path = Path(user_dir_path/'user_styles')
    make_dir(user_styles_path)
    copy_dirs(user_styles_path, working_styles_path)
    print(f'Updated the working styles folder: {working_styles_path.resolve()}')

    return
