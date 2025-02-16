import os
import glob
import modules.util as util
import random


def get_welcome_image():
    path_welcome = os.path.abspath(f'./enhanced/welcome_images/')
    skip_jpg = os.path.join(path_welcome, 'skip.jpg')
    if not os.path.isfile(skip_jpg):                   # if skip.jpg exists then ignore all jpgs & jpegs
        image_count = len(glob.glob1(path_welcome,'*.jpg')) + len(glob.glob1(path_welcome,'*.jpeg'))
        if image_count > 0:
            welcomes = [p for p in util.get_files_from_folder(path_welcome, ['.jpg', '.jpeg'], None, None)]
            return os.path.join(path_welcome, random.choice(welcomes))

    skip_png = os.path.join(path_welcome, 'skip.png')
    if not os.path.isfile(skip_png):                   # if skip.png exists then use the fallback, welcome.png
        image_count = len(glob.glob1(path_welcome,'*.png'))
        if image_count > 1:
            welcomes = [p for p in util.get_files_from_folder(path_welcome, '.png', None, None) if p != 'welcome.png']
            if len(welcomes) > 0:
                file_welcome = random.choice(welcomes) # a call to the dynamic startup code will follow this line
                return os.path.join(path_welcome, file_welcome)
    file_welcome = os.path.join(path_welcome, 'welcome.png')
    if not os.path.isfile(file_welcome):
        print()
        print(f'SERIOUS ERROR: PLEASE RESTORE {file_welcome}')
        print()
    return file_welcome

