import gradio as gr
import math
import args_manager

# These variables are set to their actual values by config.txt
default_standard_AR = '1024*1024'
default_shortlist_AR = '1024*1024'
default_sd1_5_AR = '768*768'
default_pixart_AR = '3840*2160'

# Store the current aspect ratio selection as updated by webui & modules.meta_parser
current_AR = default_standard_AR

# Store the aspect ratio template for the current preset
AR_template = 'Standard'

# Store the status of the Shortlist control
# the initial value is set to "enable_shortlist_aspect_ratios" by modules.config
AR_shortlist = False

# for use by toggle_shortlist()
# this value is updated by PR.set_preset_selection()
current_preset = args_manager.args.preset

# used to ensure template update to SD1.5 in meta_parser.get_resolution()
# this value is updated by PR.find_preset_file()
preset_file = 'presets\Favorite\Default.json'

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

default_aspect_ratio_values = [default_standard_AR, default_shortlist_AR,\
    default_sd1_5_AR, default_pixart_AR]

def assign_default_by_template(template):
    ar_index = aspect_ratios_templates.index(template)
    return default_aspect_ratio_values[ar_index]

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

def add_ratio(x):
    a, b = AR_split(x)
    a, b = int(a), int(b)
    g = math.gcd(a, b)
    c, d = a // g, b // g
    return f'{a}×{b} \U00002223 {c}:{d}'

def aspect_ratio_labels(config_aspect_ratios):
    return {template: [add_ratio(x) for x in ratios]
        for template, ratios in zip(aspect_ratios_templates, config_aspect_ratios)}

def add_template_ratio(x):    # only used to initialize the AR Accordion 
    a, b = AR_split(x)
    a, b = int(a), int(b)
    g = math.gcd(a, b)
    c, d = a // g, b // g
    return f'{AR_template} Aspect Ratio: {a}×{b} \U00002223 {c}:{d}'

def aspect_ratio_title(default_aspect_ratio_values):
    return {template: add_ratio(ratio)
        for template, ratio in zip(aspect_ratios_templates, default_aspect_ratio_values)}
aspect_ratio_title = aspect_ratio_title(default_aspect_ratio_values)

def save_current_aspect(x):
    global AR_template, current_AR
    if x != '':
        current_AR = f'{x.split(",")[0]}'
        x = current_AR
    print(f'{AR_template} Aspect Ratio: {current_AR}')
    return gr.update(), gr.update(label=AR_template)

def overwrite_aspect_ratios(width, height):
    if width>0 and height>0:
        current_AR = f'{x.split(",")[0]}'
        return AR.add_ratio(f'{width}*{height}')
    return gr.update()

def reset_aspect_ratios(arg_AR):
    global AR_shortlist, AR_template, current_AR, preset_file, task_method
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
    if (AR_shortlist == True) and (AR_template == 'Standard'):
        AR_template = 'Shortlist'
    elif (AR_shortlist == False) and (AR_template == 'Shortlist'):
        AR_template = 'Standard'
    if AR_template == 'Shortlist':
        results = [gr.update(visible=False), gr.update(value=aspect_ratios, visible=True)] + [gr.update(visible=False)] * 2
    elif AR_template=='SD1.5':
        results = [gr.update(visible=False)] * 2 + [gr.update(value=aspect_ratios, visible=True), gr.update(visible=False)]
    elif AR_template=='PixArt':
        results = [gr.update(visible=False)] * 3 + [gr.update(value=aspect_ratios, visible=True)]
    else:        # Standard template
        results = [gr.update(value=aspect_ratios, visible=True)] + [gr.update(visible=False)] * 3
    print(f'Selected the {AR_template} template with the Aspect Ratio: {current_AR}')
    return results

# a preset change is required to enable a reliable switch between Standard & Shortlist templates
# switch to either the Default preset or Cheyenne when changing presets
def reset_preset():
    global current_preset
    working_preset = current_preset
    if current_preset == 'Default':
        working_preset = 'Cheyenne'
    else:
        working_preset = 'Default'
    return working_preset

def toggle_shortlist(arg_shortlist):
    global AR_shortlist, AR_template, current_AR, shortlist_default, current_preset
    AR_shortlist = arg_shortlist
    working_preset = current_preset
    if AR_template == 'Standard' and AR_shortlist:
        AR_template = 'Shortlist'
        # this ensures that Shortlist does not start with an invalid value:
        current_AR = default_shortlist_AR
        print()
        print('Switching to the Shortlist template requires a preset change:')
        working_preset = reset_preset()
    elif AR_template == 'Shortlist' and not AR_shortlist:
        AR_template = 'Standard'
        print()
        print('Switching to the Standard template requires a preset change:')
        working_preset = reset_preset()
    return gr.update(), gr.update(value=current_AR),\
        gr.update(value=working_preset)

def save_AR_template(x):
    global AR_template
#    x = AR_template
    if (AR_template == 'Standard') or (AR_template == 'Shortlist'):
        return gr.update(), gr.update(label=AR_template), gr.update(visible=True)
    else:
        return gr.update(), gr.update(label=AR_template), gr.update(visible=False)
