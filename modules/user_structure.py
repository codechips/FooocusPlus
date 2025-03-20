import os
import shutil
import args_manager
from modules import config

def create_model_structure():
  # ensure that all the special model directories exist
  os.makedirs(config.paths_checkpoints[0] + '\Alternative', exist_ok=True)
  os.makedirs(config.paths_checkpoints[0] + '\Flux', exist_ok=True)
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
  print(f'Initialized the user folder at {os.path.abspath(args_manager.args.user_dir)}')
  shutil.copytree('./master_batch_startups', f'{args_manager.args.user_dir}/batch_startups', dirs_exist_ok = True)
  shutil.copytree('./master_control_images', f'{args_manager.args.user_dir}/control_images', dirs_exist_ok = True)
  shutil.copytree('./master_welcome_images', f'{args_manager.args.user_dir}/welcome_images', dirs_exist_ok = True)
  shutil.copytree('./master_wildcards', f'{args_manager.args.user_dir}/wildcards', dirs_exist_ok = True)

  # delete the contents of user_dir/master_presets to get a clean start
  # copy the contents of './master_presets' to user_dir for the user's reference only
  master_presets = f'{args_manager.args.user_dir}/master_presets'
  if os.path.exists(master_presets):
    shutil.rmtree(master_presets, ignore_errors=True)
  shutil.copytree('./master_presets', master_presets', dirs_exist_ok = True)

  # ensure that './presets' exists
  # delete the contents of './presets' which is used as a temporary working folder
  # initialize './presets' with the contents of './master_presets'
  working_presets = './presets'
  if os.path.exists(working_presets):
    shutil.rmtree(working_presets, ignore_errors=True)
  shutil.copytree('./master_presets', working_presets, dirs_exist_ok = True)

  # overwrite './presets' with the contents of user_dir './user_presets'
  # this allows a user to completely customize the master presets, if desired
  user_presets = f'{args_manager.args.user_dir}/user_presets'
  os.makedirs(user_presets, exist_ok = True)
  if os.path.exists(user_presets):
    shutil.copytree(user_presets, working_presets, dirs_exist_ok = True)
  print(f'Updated the working preset folder: {working_presets}')

  # in a similar way, initialize the Random Prompt (One Button Prompt) structure
  master_topics = f'{args_manager.args.user_dir}/master_topics'
  if os.path.exists(master_topics):
    shutil.rmtree(master_topics, ignore_errors=True)
  shutil.copytree('./master_topics', f'{args_manager.args.user_dir}/master_topics', dirs_exist_ok = True)
  
  working_topics = './custom/OneButtonPrompt/random_prompt/userfiles'
  os.makedirs(working_topics, exist_ok = True)
  if os.path.exists(working_topics):
    shutil.rmtree(working_topics, ignore_errors=True)
  shutil.copytree('./master_topics', working_topics, dirs_exist_ok = True)

  user_topics = f'{args_manager.args.user_dir}/user_topics'
  os.makedirs(user_topics, exist_ok = True)
  if os.path.exists(user_topics):
    shutil.copytree(user_topics, working_topics, dirs_exist_ok = True)
  print(f'Updated the working Random Prompt topics folder: {os.path.abspath(working_presets)}')
  return
