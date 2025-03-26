import os

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


def DependencyResolver(torch_ver: str = "2.5.1"):
    """
    Provides the dependent versions of a Torch build.
    Returns a dictionary with:
    - torchvision_version: str
    - torchaudio_version: str
    - xformers_version: str
    - pytorchlightning_version: str
    - lightningfabric_version: str
    """
    # set our defaults for 2.5.1
    torchvision_default = "0.20.1"
    torchaudio_default = "2.5.1"
    xformers_default = "0.0.29.post1"
    pytorchlightning_default = "2.5.1"
    lightningfabric_default = "2.5.1"
    
    ### begin assignments ###
    if torch_ver == "2.4.1":
        dependencies = dict(
            torchvision_version = "0.19.1",
            torchaudio_version = "2.4.1",
            xformers_version = "0.0.28.post1",
            pytorchlightning_version = "2.5.1", # will be compatible with slightly older versions
            lightningfabric_version = "2.5.1",
        )

    elif torch_ver == "2.2.2": # last version supporting Intel Macs
        dependencies = dict(
            torchvision_version = "0.17.2",
            torchaudio_version = "2.2.2",
            xformers_version = "0.0.27.post2", # but not MPS compatible
            pytorchlightning_version = "2.4.0", # confirm 2.5.1 compatibility when versioning policy updated
            lightningfabric_version = "2.4.0",
        )

    elif torch_ver == "1.13.1": # earliest possible supported release: rocm5.2
        dependencies = dict(
            torchvision_version = "0.14.1",
            torchaudio_version = "0.13.1",
            xformers_version = "0.0.20", # but not compatible with ROCm, rocm6.2.4 only
            pytorchlightning_version = "2.2.5",
            lightningfabric_version = "2.2.5",
        )

    else:
        # use the defaults
        dependencies = dict(
            torchvision_version = torchvision_default,
            torchaudio_version = torchaudio_default,
            xformers_version = xformers_default,
            pytorchlightning_version = pytorchlightning_default,
            lightningfabric_version = lightningfabric_default,
        )
    
    # return the result
    return dependencies
