import math
from modules.meta_parser import ar_template
from modules.flags import aspect_ratios_templates, available_aspect_ratios


default_aspect_ratio = ['1024*1024', '768*768', '3840*2160']
ar_index = aspect_ratios_templates.index(ar_template)

def add_ratio(x):
    print(f'x: {x}')
    a, b = x.replace('*', ' ').split(' ')[:2]
    a, b = int(a), int(b)
    g = math.gcd(a, b)
    c, d = a // g, b // g
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
     
