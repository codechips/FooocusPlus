import math
from common import CURRENT_ASPECT
from modules.flags import aspect_ratios_templates, default_aspect_ratio, available_aspect_ratios

print(f'CURRENT_ASPECT in AR: {CURRENT_ASPECT}')

def add_ratio(x):
    print(f'x: {x}')
    a, b = x.replace('*', ' ').split(' ')[:2]
    a, b = int(a), int(b)
    g = math.gcd(a, b)
    c, d = a // g, b // g
    if (a, b) == (576, 1344):
        c, d = 9, 21
    elif (a, b) == (1344, 576):
        c, d = 21, 9
    elif (a, b) == (768, 1280):
        c, d = 9, 15
    elif (a, b) == (1280, 768):
        c, d = 15, 9
    return f'{a}×{b} <span style="color: grey;"> \U00002223 {c}:{d}</span>'
    
default_aspect_ratios = {
    template: add_ratio(ratio)
    for template, ratio in zip(aspect_ratios_templates, default_aspect_ratio)
}

available_aspect_ratios_list = {
    template: [add_ratio(x) for x in ratios]
    for template, ratios in zip(aspect_ratios_templates, available_aspect_ratios)
}

def reset_aspect_ratios(aspect_ratios):
#    global aspect_ratios_selection
    if len(aspect_ratios.split(','))>1:
        template = aspect_ratios.split(',')[1]
        aspect_ratios = aspect_ratios.split(',')[0]
        if template=='SD1':
            print()
        elif template=='PixArt':
            print()
        elif template=='Spare':
            print()    
        else:        # SDXL template
             print()
    else:
        print()
    return results
     
