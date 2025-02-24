import os
import sys
from pathlib import Path

branch = ''
commit_id = ''
fooocusplus_ver = ''
simplesdxl_ver = ''

def get_library_ver():
    current_library = Path('../python_embedded/embedded_version/library_version.py')
    print(f'current_library {current_library}')
    if os.path.exists(current_library):
        embedded_version = os.path.abspath('../python_embedded/embedded_version')
        print(f'embedded_version {embedded_version}')
        sys.path.append(embedded_version)
        from embedded_version import library_version
        return (library_version.version)
    else:
        return 0.96

def get_required_library():
    if not os.path.exists('enhanced/required_library.py'):
        return True
    if get_library_ver() >= enhanced.required_library.version:
        return True
    else:
        return False

def get_fooocusplus_ver():
    global fooocusplus_ver, commit_id
    if not fooocusplus_ver:
        fooocusplus_log = os.path.abspath(f'./fooocusplus_log.md')
        if os.path.exists(fooocusplus_log):
            with open(fooocusplus_log, "r", encoding="utf-8") as log_file:
                line = log_file.readline().strip()
                while line:
                    if line.startswith("# "):
                        break
                    line = log_file.readline().strip()                
        else:
            line = '0.9.0'
        fooocusplus_ver = line.strip('# ')
        if commit_id:
            fooocusplus_ver += f'.{commit_id}'
    return fooocusplus_ver

def get_simplesdxl_ver():
    global simplesdxl_ver, commit_id
    if not simplesdxl_ver:
        simplesdxl_log = os.path.abspath(f'./simplesdxl_log.md')
        line = ''
        if os.path.exists(simplesdxl_log):
            with open(simplesdxl_log, "r", encoding="utf-8") as log_file:
                line = log_file.readline().strip()
                while line:
                    if line.startswith("# "):
                        break
                    line = log_file.readline().strip()
        else:
            line = '# 2024-09-16'
        date = line.split(' ')[1].split('-')
        simplesdxl_ver = f'{date[0]}{date[1]}{date[2]}'
    return simplesdxl_ver

def get_branch():
    global branch, commit_id
    if not branch:
        import pygit2
        pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)
        repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))
        branch = repo.head.shorthand
        if branch=="main":
            branch = "FooocusPlus"
        commit_id = f'{repo.head.target}'[:7]
    return branch

