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
  shutil.copytree('./master_batch_startups', f'{args_manager.args.user_dir}/batch_startups')
  shutil.copytree('./master_control_images', f'{args_manager.args.user_dir}/control_images')
  shutil.copytree('./master_presets', f'{args_manager.args.user_dir}/presets')
  shutil.copytree('./master_welcome_images', f'{args_manager.args.user_dir}/welcome_images')
  shutil.copytree('./master_wildcards', f'{args_manager.args.user_dir}/wildcards')
  return
