import os
import platform
import sys
import args_manager
import torchruntime
from torchruntime.platform_detection import get_torch_platform

win32_root = os.path.dirname(os.path.dirname(__file__))
python_embedded_path = os.path.join(win32_root, 'python_embedded')

is_win32_standalone_build = os.path.exists(python_embedded_path) and os.path.isdir(python_embedded_path)

win32_cmd = '''
@echo off
.\python_embedded\python.exe -s FooocusPlus\{cmds} %*
pause
'''

def build_launcher():
    if not is_win32_standalone_build:
        return

    branches = {"FooocusPlus": "entry_with_update.py", "FooocusPlus_dev": "entry_with_update.py --dev",\
        "FooocusPlus_without_update": "launch.py", "FooocusPlus_commit": "launch_with_commit.py 56e5200"}

    for (name, cmd) in branches.items():
        win32_cmd_preset = win32_cmd.replace('{cmds}', f'{cmd}')
        bat_path = os.path.join(win32_root, f'run_{name}.bat')
        if not os.path.exists(bat_path) or name=='FooocusPlus_commit':
            with open(bat_path, "w", encoding="utf-8") as f:
                f.write(win32_cmd_preset)
    return


def dependency_resolver():
    """
    Provides the dependent versions of a Torch build.
    Returns a dictionary with:
    - torchvision_ver: str
    - torchaudio_ver: str
    - xformers_ver: str
    - pytorchlightning_version: str
    - lightningfabric_version: str
    """
    # set our defaults for 2.5.1
    torch_default = "2.5.1"
    torchvision_default = "0.20.1"
    torchaudio_default = "2.5.1"
    xformers_default = "0.0.29.post1"
    pytorchlightning_default = "2.5.1"
    lightningfabric_default = "2.5.1"
    torchruntime_platform = get_torch_platform()

    # Logic: Windows (win32)
    if (sys.platform == "win32") and (torchruntime_platform == "nightly/cu128"):
        torch_ver = "special"

    elif sys.platform == "linux":
        if torchruntime_platform == "nightly/cu128":
            torch_ver = "special"
        elif torchruntime_platform == "rocm5.7":
            torch_ver = "2.3.1"
        elif torchruntime_platform == "rocm5.2":
            torch_ver = "1.13.1"

    elif sys.platform == "darwin": # OSX
        if platform.machine == "amd64":
            torch_ver = "2.2.2"
            args_manager.directml = True # switch on AMD support
        else:
            torch_ver = "2.5.1" # Apple Silicon

    ### begin assignments ###
    if torch_ver == "2.4.1":
        dependencies = dict(
            torch_ver,
            torchvision_ver = "0.19.1",
            torchaudio_ver = "2.4.1",
            xformers_ver = "0.0.28.post1",
            pytorchlightning_version = "2.5.1", # will be compatible with slightly older versions
            lightningfabric_version = "2.5.1",
        )
    
    elif torch_ver == "2.3.1": # for Linux rocm5.7
        dependencies = dict(
            torch_ver,
            torchvision_ver = "0.18.1",
            torchaudio_ver = "2.3.1",
            xformers_ver = "0.0.27",
            pytorchlightning_version = "2.4.0",
            lightningfabric_version = "2.4.0",
        )        
    
    elif torch_ver == "2.2.2": # last version supporting Intel Macs
        dependencies = dict(
            torch_ver,
            torchvision_ver = "0.17.2",
            torchaudio_ver = "2.2.2",
            xformers_ver = "0.0.27.post2", # but not MPS compatible
            pytorchlightning_version = "2.4.0", # confirm 2.5.1 compatibility when versioning policy updated
            lightningfabric_version = "2.4.0",
        )

    elif torch_ver == "1.13.1": # earliest possible supported release: rocm5.2
        dependencies = dict(
            torch_ver,
            torchvision_ver = "0.14.1",
            torchaudio_ver = "0.13.1",
            xformers_ver = "0.0.20", # but not compatible with ROCm, rocm6.2.4 only
            pytorchlightning_version = "2.2.5",
            lightningfabric_version = "2.2.5",
        )

    elif torch_ver == "special": # version not specified (launch will clear the string)
        dependencies = dict(
            torch_ver,
            torchvision_ver = "",
            torchaudio_ver = "",
            xformers_ver = "",
            pytorchlightning_version = "",
            lightningfabric_version = "",
        )
    
    else:
        # use the defaults
        dependencies = dict(
            torch_ver = torch_default,
            torchvision_ver = torchvision_default,
            torchaudio_ver = torchaudio_default,
            xformers_ver = xformers_default,
            pytorchlightning_version = pytorchlightning_default,
            lightningfabric_version = lightningfabric_default,
        )
    
    # return the result
    return dependencies

def delete_packages():
    return

def read_torch_base():    
    try:
        torch_base_path = os.path.abspath(f'{args_manager.user_dir}/torch_base.txt')
        torch_base = open(torch_base_path, 'r')
        torch_base_ver = torch_base_ver.readline().strip()
        divider = '= '
        scratch = torch_base_ver.split(divider, 1)
        torch_base_ver = scratch[1] if len(scratch) > 1 else ''
        torch_base.close()
    except:
        torch_base_ver = ''
    return torch_base_ver

def write_torch_base(torch_base_ver):
    torch_base_path = os.path.abspath(f'{args_manager.user_dir}/torch_base.txt')
    torch_base = open(torch_base_path, "w")
    torch_base.write(f"Torch base version = '{torch_base_ver}'")
    torch_base.close()
    return

