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
  create_model_structure()
  # initialize the user directory, user_dir
  shutil.copytree('./master_batch_startups', (os.path.join(args_manager.args.user_dir, '/batch_startups')), dirs_exist_ok = True)
  shutil.copytree('./master_control_images', (os.path.join(args_manager.args.user_dir, '/control_images')), dirs_exist_ok = True)
  shutil.copytree('./master_presets', (os.path.join(args_manager.args.user_dir, '/presets')), dirs_exist_ok = True)
  shutil.copytree('./master_welcome_images', (os.path.join(args_manager.args.user_dir, '/welcome_images')), dirs_exist_ok = True)
  shutil.copytree('./master_wildcards', (os.path.join(args_manager.args.user_dir, '/wildcards')), dirs_exist_ok = True)
  return
