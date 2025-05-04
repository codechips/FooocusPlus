import os
import shutil
import modules.preset_resource as PR
from modules import config

def create_model_structure():
  # ensure that all the special model directories exist
  os.makedirs(config.paths_checkpoints[0] + '\Alternative', exist_ok=True)
  os.makedirs(config.paths_checkpoints[0] + '\FluxDev', exist_ok=True)
  os.makedirs(config.paths_checkpoints[0] + '\FluxSchnell', exist_ok=True)
  os.makedirs(config.paths_checkpoints[0] + '\LowVRAM', exist_ok=True)
  os.makedirs(config.paths_checkpoints[0] + '\Pony', exist_ok=True)
  os.makedirs(config.paths_checkpoints[0] + '\SD1.5', exist_ok=True)
  os.makedirs(config.paths_checkpoints[0] + '\SD3x', exist_ok=True)

  # ensure that the special LoRA directories exist
  os.makedirs(config.paths_loras[0] + '\Alternative', exist_ok=True)        
  os.makedirs(config.paths_loras[0] + '\Flux', exist_ok=True)
  os.makedirs(config.paths_loras[0] + '\Pony', exist_ok=True)
  os.makedirs(config.paths_loras[0] + '\SD1.5', exist_ok=True)
  os.makedirs(config.paths_loras[0] + '\SD3x', exist_ok=True)
  return

def create_user_structure():
  # initialize the user directory, user_dir  
  print(f'Initialized the user folder at {os.path.abspath(config.user_dir)}')
  shutil.copytree('./masters/master_batch_startups', f'{config.user_dir}/batch_startups', dirs_exist_ok = True)
  shutil.copytree('./masters/master_control_images', f'{config.user_dir}/control_images', dirs_exist_ok = True)
  shutil.copytree('./masters/master_welcome_images', f'{config.user_dir}/welcome_images', dirs_exist_ok = True)
  shutil.copytree('./masters/master_wildcards', f'{config.user_dir}/wildcards', dirs_exist_ok = True)

  # delete the contents of user_dir/master_topics to get a clean start
  # copy the contents of '.masters/master_topics' to user_dir for the user's reference only
  master_topics = f'{config.user_dir}/master_topics'
  if os.path.exists(master_topics):
    shutil.rmtree(master_topics, ignore_errors=True)
  shutil.copytree('./masters/master_topics', f'{config.user_dir}/master_topics', dirs_exist_ok = True)
  
  # ensure that './custom/OneButtonPrompt/random_prompt/userfiles' exists
  # delete the contents of 'usefiles' which is used as a temporary working folder
  # initialize 'userfiles' with the contents of '.masters/master_topics'
  working_topics = os.path.abspath('./custom/OneButtonPrompt/random_prompt/userfiles')
  os.makedirs(working_topics, exist_ok = True)
  if os.path.exists(working_topics):
    shutil.rmtree(working_topics, ignore_errors=True)
  shutil.copytree('./masters/master_topics', working_topics, dirs_exist_ok = True)

  # overwrite 'userfiles' with the contents of user_dir './user_topics'
  # this allows a user to completely customize the available topics, if desired
  user_topics = f'{config.user_dir}/user_topics'
  os.makedirs(user_topics, exist_ok = True)
  if os.path.exists(user_topics):
    shutil.copytree(user_topics, working_topics, dirs_exist_ok = True)
  print('Updated the working Random Prompt (OneButtonPrompt) topics folder:')
  print(f'  {working_topics}')

  # in a similar way, initialize the Presets structure
  master_presets = f'{config.user_dir}/master_presets'
  if os.path.exists(master_presets):
    shutil.rmtree(master_presets, ignore_errors=True)
  shutil.copytree('./masters/master_presets', master_presets, dirs_exist_ok = True)

  working_presets = os.path.abspath('./presets')
  if os.path.exists(working_presets):
    shutil.rmtree(working_presets, ignore_errors=True)
  shutil.copytree('./masters/master_presets', working_presets, dirs_exist_ok = True)

  user_presets = f'{config.user_dir}/user_presets'
  os.makedirs(user_presets, exist_ok = True)
  preset_foldernames = PR.get_preset_foldernames()
  for i in preset_foldernames:
    os.makedirs(os.path.join(user_presets, preset_foldernames[i]), exist_ok = True)
  if os.path.exists(user_presets):
    shutil.copytree(user_presets, working_presets, dirs_exist_ok = True)
  print(f'Updated the working preset folder: {working_presets}')
  return
