import gradio as gr
import math

# Store the current aspect ratio selection as updated by webui & modules.meta_parser
# the initial value is set to default_standard_aspect_ratio by modules.config
current_AR = '1024*1024'

# Store the aspect ratio template for the current preset or Shortlist selector
AR_template = 'Standard'

aspect_ratios_templates = ['Standard', 'Shortlist', 'SD1.5', 'PixArt']
available_aspect_ratios = [
    ['704*1408', '704*1344', '756*1344', '768*1344', '768*1280',
     '832*1248', '832*1216', '832*1152', '864*1152', '896*1152',
     '896*1088', '960*1088', '960*1024', '1024*1024', '1280*1280',
     '1024*960', '1088*960', '1088*896', '1152*896', '1152*864',
     '1152*832', '1216*832', '1248*832', '1280*768', '1344*768',
     '1344*756', '1344*704', '1408*704', '1472*704', '1536*640',
     '1600*640', '1664*576', '1728*576', '2048*512'],

    ['756*1344', '768*1344', '768*1280', '832*1248', '864*1152',
    '896*1152', '1024*1024', '1152*896', '1152*864', '1248*832',
    '1280*768', '1344*768', '1344*756', '1408*704', '1536*640'],

    ['192*448', '288*512', '384*640', '320*512', '384*576',
     '512*768', '384*512', '576*768', '512*640', '512*512',
     '768*768', '640*512', '512*384', '768*576', '576*384',
     '768*512', '512*320', '640*384', '512*288', '448*192'],

    ['704*1408', '704*1344', '756*1344', '768*1344', '1152*2048',
     '2160*3840', '768*1280', '832*1248', '1280*1920', '832*1216',
     '832*1152', '864*1152', '1536*2048', '896*1152', '1536*1920',
     '896*1088', '960*1088', '960*1024', '1024*1024', '1280*1280',
     '2880*2880', '1024*960', '1088*960', '1088*896', '1920*1536',
     '1152*896', '1152*864', '2048*1536', '1152*832', '1216*832',
     '1248*832', '1920*1280', '1280*768', '1344*768', '1344*756',
     '2048*1152', '3840*2160', '1344*704', '1408*704', '1472*704',
     '1792*768', '1536*640', '1600*640', '1664*576', '1728*576',
     '2048*512'],
]

def do_the_split(x):
    x = x.replace("x","*") # entries in config.txt that use "x" instead of "*"
    x = x.replace("×","*") # webui aspect ratio selector uses the raised "×"
    width, height = x.replace('*', ' ').split(' ')[:2]
    return width, height

def AR_split(x):
    width, height = do_the_split(x)
    if (width == '') or (height == ''):
        print()
        print(f'Adjusting aspect ratio value to {current_AR}')
        width, height = do_the_split(current_AR)
    return width, height

def add_template_ratio(x):    # used to initialize the AR Accordion 
    a, b = AR_split(x)
    a, b = int(a), int(b)
    g = math.gcd(a, b)
    c, d = a // g, b // g
    return f'{AR_template} Aspect Ratio: {a}×{b} \U00002223 {c}:{d}'

def aspect_ratio_title(default_aspect_ratio_values):
    return {template: add_template_ratio(ratio)
        for template, ratio in zip(aspect_ratios_templates, default_aspect_ratio_values)}

def add_ratio(x):
    a, b = AR_split(x)
    a, b = int(a), int(b)
    g = math.gcd(a, b)
    c, d = a // g, b // g
    return f'{a}×{b} \U00002223 {c}:{d}'

def aspect_ratio_labels(config_aspect_ratios):
    return {template: [add_ratio(x) for x in ratios]
        for template, ratios in zip(aspect_ratios_templates, config_aspect_ratios)}

def save_current_aspect(x):
    global current_AR
    if x != '':
        print()
        print(f'save_current_aspect x: {x}')
        print(f'save_current_aspect AR_template {AR_template}')
        current_AR = f'{x.split(",")[0]}'
    return x, gr.update(label=AR_template)

def overwrite_aspect_ratios(width, height):
    if width>0 and height>0:
        current_AR = f'{x.split(",")[0]}'
        return AR.add_ratio(f'{width}*{height}')
    return gr.update()

def reset_aspect_ratios(arg_AR):
    global AR_template, current_AR
    print()
    print(f'reset_aspect_rations arg_AR: {arg_AR}')
    if len(arg_AR.split(','))>1:
        template = arg_AR.split(',')[1]
        AR_template = template
    elif not AR_template:
        # fallback if template & AR_template are undefined
        results = [gr.update()] * 4
        return results
    aspect_ratios = arg_AR.split(',')[0]
    if aspect_ratios:
        current_AR = aspect_ratios    
    if AR_template=='Shortlist':
        results = [gr.update(visible=False), gr.update(value=aspect_ratios, visible=True)] + [gr.update(visible=False)] * 2
    elif AR_template=='SD1.5':
        results = [gr.update(visible=False)] * 2 + [gr.update(value=aspect_ratios, visible=True), gr.update(visible=False)]
    elif AR_template=='PixArt':
        results = [gr.update(visible=False)] * 3 + [gr.update(value=aspect_ratios, visible=True)]
    else:        # Standard template           
       results = [gr.update(value=aspect_ratios, visible=True)] + [gr.update(visible=False)] * 3
    return results

def save_AR_template():
    return gr.update(label=AR_template)
