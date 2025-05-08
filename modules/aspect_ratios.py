import math

# Store the current aspect ratio selection as updated by webui & modules.meta_parser
current_AR = modules.config.default_standard_aspect_ratio

# Store the aspect ratio template for the current preset
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

def AR_split(x):
    x = x.replace("x","*") # entries in config.txt that use "x" instead of "*"
    x = x.replace("×","*") # webui aspect ratio selector uses the raised "×"
    width, height = x.replace('*', ' ').split(' ')[:2]
    return width, height

def add_ratio(x):
    a, b = AR_split(x)
    a, b = int(a), int(b)
    g = math.gcd(a, b)
    c, d = a // g, b // g
    return f'{a}×{b} <span style="color: grey;"> \U00002223 {c}:{d}</span>'

def aspect_ratio_title(default_aspect_ratio_values):
    return {template: add_ratio(ratio)
        for template, ratio in zip(aspect_ratios_templates, default_aspect_ratio_values)}

def aspect_ratio_labels(config_aspect_ratios):
    return {template: [add_ratio(x) for x in ratios]
        for template, ratios in zip(aspect_ratios_templates, config_aspect_ratios)}
