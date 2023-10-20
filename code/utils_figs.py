import matplotlib.colors as mcolors
import numpy as np


def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values'''
    value = value.strip("#") # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values'''
    return [v/256 for v in value]


def get_continuous_cmap(hex_list, float_list=None):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list. 
        
        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.
        
        Returns
        ----------
        colour map'''
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0,1,len(rgb_list)))
        
    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = mcolors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp


ndvi_map = get_continuous_cmap(['#7B3F00','#FFFACD','#3C8703'])
bg_map = get_continuous_cmap(['#FFFFFF','#E9F6F4','#D2EDE9','#A8D5D0','#7EBCB6','#2A8B83','#166B62','#014B40'])
h2o_map = get_continuous_cmap(['#FFFFFF','#CFF3F8','#B6EBF4','#9CE3EF','#68C4D5','#34A4BB','#0D859C','#026876'])
ef_map = get_continuous_cmap(['#FFFFFF','#E7F9FC','#CFF3F8','#B6EBF4','#96DAE6','#75C8D8','#55B6CA','#34A4BB','#2195AC','#026876'])


gray = '#454545'

# turq = '#409099'
turq = '#2195AC'
sky = '#95C7CB'
salmon = '#f9ab98'
rouge = '#EF877D'
forest = '#1E6626'
# green = '#B2CE5B'
green = '#81BF24'
gold = '#F1C300'
# orange = '#FFA500'
orange = '#f8961e'
brown = '#AA7942'

maroon = '#80004D'
lav = '#A6A6ED'

c_list = [gold, turq, rouge, green]
c3_list = [green,gray,turq]
c4_list = [gray,rouge,turq,green]

co_list = [green, rouge, turq, gray, gold, sky]
    
#col_list = [sky, gold, lav, maroon, gray, rouge, forest]

col_list = [green, rouge, turq, gray, sky, gold, forest, lav, maroon]

e_list = ['#6a7b36','#e74839','#295d63','k','#62acb2','#a58500','#0d2b10','#6666e0','#34001f']

red = '#cc3928'
green1 = '#2b9348'
green2 = '#aacc00'

blue1 = '#0d557f'
blue2 = '#087ebb'
darkblue = '#11405b'

pink1 = '#ff0081'
pink2 = '#ff77bc'
purple1 = '#5a189a'
purple2 = '#e0aaff'

cal_palettes = {
    ### release 1: June 2020
    "sierra1": ["#BD973D", "#5F5C29", "#3B7D6E", "#5792CC", "#4D5B75", "#262E43"],
    "sierra2": ["#FDD989", "#8BAD57", "#516238", "#4CA2B0", "#5A8B92", "#395B5F"],
    "chaparral1": ["#DCC27A", "#B0B9BE", "#63605F", "#985E5C", "#AEBFA8", "#F19B34"],
    "chaparral2": ["#D98A63", "#D9E4DC", "#C5D2D2", "#79B38F", "#9A9B5F", "#A7C2CD"],
    "chaparral3": ["#D3E3CA", "#BED6B3", "#92A587", "#4A5438", "#2F3525"],
    "conifer": ["#CC7540", "#765043", "#A69260", "#979A6B", "#39692F"],
    "desert": ["#F6EECF", "#ECD6AB", "#B09175", "#632D1F", "#291611"],
    "wetland": ["#DED4C8", "#AD6F4F", "#AEC96F", "#2B3851", "#3F320D"],
    "oak": ["#EFC68E", "#B58755", "#7C9867", "#4F5730", "#7A5028"],
    "kelp1": ["#C70000", "#FFBF00", "#BE8333", "#54662C", "#009BB0", "#114C54"],
    "kelp2": ["#0FB2D3", "#026779", "#368000", "#3D6334", "#6D5A18"],
    "coastaldune1": ["#DCC8BA", "#DCD6C5", "#B4AA98", "#D7DCE4", "#444239"],
    "coastaldune2": ["#E2D78A", "#E4B3E2", "#90816E", "#523833", "#372E21"],
    "superbloom1": ["#B9C7E2", "#ECAB99", "#F1C100", "#5B6530", "#9484B1"],
    "superbloom2": ["#DE7424", "#F5CA37", "#AD8D26", "#496849", "#654783"],
    "superbloom3": ["#E69512", "#D3105C", "#3B4F8E", "#3A5D3D", "#4C4976", "#6C91BD"],
    "sbchannel": ["#A1CAF6", "#6592D6", "#4C6FA1", "#375377", "#1E2F46"],
    "lake": ["#CECEB9", "#7AC9B7", "#6CA184", "#3793EC", "#2A3927"],
    "fire": ["#B77B7B", "#FEEC44", "#F66C09", "#E60505", "#2C1B21"],
    "agriculture": ["#A45C44", "#5A7F3C", "#CACA91", "#2C3B26", "#88B063"],
    "bigsur": ["#E4DECE", "#ECBD95", "#9BB1BB", "#79ACBD", "#346575", "#0B4221"],
    "figmtn": ["#E29244", "#FFAA00", "#D46F10", "#4CA49E", "#69B9FA", "#59A3F8", "#4B8FF7", "#5A7ECB", "#6B6D9F"],
    "caqu": ["#E6DECC", "#F3E3C2", "#8F96A6", "#625D55", "#501F16"],
    "eschscholzia": ["#F2B705", "#F29F05", "#F28705", "#D95204", "#A62F03"],
    "arbutus": ["#DFE3CE", "#B5C861", "#8AA789", "#CB8573", "#976153"],
    "calochortus": ["#CAC8CF", "#C9B3B5", "#8F706E", "#AF6E78", "#5C3327"],
    "grassdry": ["#E1BC8D", "#845B3E", "#5B4E23", "#35301C", "#4C5454"],
    "grasswet": ["#4C4E32", "#908E6C", "#5D8FBC", "#97C2E2", "#17252A", "#B4A480"],
    "sage": ["#607860", "#304830", "#C0D8F0", "#909078", "#181818"],
    "tidepool": ["#84A6A2", "#4A5352", "#151E2F", "#D7C8C6", "#BE5A47", "#604A76"],
    "seagrass": ["#5A870A", "#BDD0A2", "#555B53", "#6A4D3B", "#BEAB91", "#8F9BAB"],
    "bigsur2": ["#20618D", "#91AAC4", "#6B6C58", "#464724", "#83932D", "#CAB89F"],
    "bixby": ["#286A81", "#045CB4", "#7F6F43", "#748B75", "#B8B196"],
    "redwood1": ["#303018", "#604830", "#609048", "#90A860", "#786048"],
    "redwood2": ["#304818", "#906030", "#486030", "#784830", "#181800"],
    "halfdome": ["#A2A098", "#5E6B7B", "#233D3F", "#85ADCC", "#426714"],
    "creek": ["#EBDAC9", "#CEAD96", "#CECFD4", "#686F60", "#455D44", "#23341E"],
    "vermillion": ["#c39ca4", "#e05959", "#ac181d", "#713d3f", "#381f21"],
    "canary": ["#FFDBA5", "#FAB455", "#F28023", "#A5683C", "#B4450E"],
    "casj": ["#336887", "#8197A4", "#A9B4BC", "#B7AA9F", "#706A6B"],
    "lupinus": ["#6C568C", "#9386A6", "#BFCDD9", "#7F8C72", "#607345"],
    "dudleya": ["#7E8C69", "#E7A655", "#E59D7F", "#E38377", "#6D4847"],
    "gayophytum": ["#AA767C", "#B7AF57", "#797014", "#C2607F", "#A65644"],
    "collinsia": ["#9E8ABC", "#A99CD9", "#808C91", "#A7907B", "#A5BA92"],
    "buow": ["#DED4CB", "#DBE38E", "#7E7576", "#A79787", "#3A2C21"]
}

lacroix_palettes = {
    'PassionFruit': ["#C70E7B", "#FC6882", "#A6E000", "#1BB6AF", "#6C6C9D", "#172869"],
    'Mango': ["#FF5300", "#9ED80B", "#43B629", "#1BB6AF", "#8F92A1", "#172869"],
    'Pure': ["#AFDFEF", "#54BCD1", "#1BB6AF", "#0099D5", "#007BC3", "#172869"],
    'Lime': ["#2CB11B", "#95C65C", "#BDDE9B", "#1BB6AF", "#0076C0", "#172869"],
    'Lemon': ["#F7AA14", "#F5D000", "#F7E690", "#1BB6AF", "#088BBE", "#172869"],
    'Orange': ["#EF7C12", "#FCA315", "#F4B95A", "#1BB6AF", "#088BBE", "#172869"],
    'Berry': ["#B25D91", "#CB87B4", "#EFC7E6", "#1BB6AF", "#088BBE", "#172869"],
    'CranRaspberry': ["#D9565C", "#F28A8A", "#EDA9AB", "#1BB6AF", "#088BBE", "#172869"],
    'Pamplemousse': ["#EA7580", "#F6A1A5", "#F8CD9C", "#1BB6AF", "#088BBE", "#172869"],
    'PeachPear': ["#FF3200", "#E9A17C", "#E9E4A6", "#1BB6AF", "#0076BB", "#172869"],
    'Coconut': ["#881C00", "#AF6125", "#F4E3C7", "#1BB6AF", "#0076BB", "#172869"],
    'Apricot': ["#D72000", "#EE6100", "#FFAD0A", "#1BB6AF", "#9093A2", "#132157"],
    'Tangerine': ["#EF562A", "#EC921D", "#F7B449", "#FFED00", "#1BB6AF", "#9093A2", "#132157"],
    'KeyLime': ["#D84D16", "#FFF800", "#8FDA04", "#009F3F", "#132157"],
    'PommeBaya': ["#C23A4B", "#FBBB48", "#EFEF46", "#31D64D", "#132157"],
    'CeriseLimon': ["#EE4244", "#F8D961", "#B6D944", "#638E6E", "#3C5541", "#132157"],
    'PinaFraise': ["#F44B4B", "#F19743", "#F1F1A8", "#92D84F", "#7473A6", "#132157"],
    'KiwiSandia': ["#D18F55", "#FF3F38", "#FF8C8D", "#AFDE62", "#3CBC38", "#4F5791", "#132157"],

}

batlow = [
    '#011959', '#FACCFA', '#828231', '#226061', '#F19D6B', '#FDB4B4', 
    '#114360', '#4D734D', '#C09036', '#175262', '#356A59', '#FCA890', 
    '#677B3E', '#0D315D', '#FCBFD6', '#A18A2B', '#DD954D', '#134B61', 
    '#0F3B5F', '#91862D', '#2B655E', '#FDBAC4', '#08255B', '#1B5962', 
    '#CF9340', '#FDAEA2', '#5A7745', '#416F53', '#B18D2F', '#F8A27E', 
    '#FBC6E8', '#747E38', '#E7985A', '#7B8034', '#537549', '#FBC9F1', 
    '#FAA587', '#6D7C3B', '#FDB7BC', '#103F60', '#3B6D56', '#FDBCCD', 
    '#FDB1AB', '#B98F32', '#99882C', '#1E5D62', '#FDAB9A', '#0E365E', 
    '#C8913B', '#8A842F', '#ED9A62', '#26635F', '#A98C2C', '#F59F74', 
    '#154F62', '#30685C', '#FCC3DF', '#195662', '#0B2B5C', '#607942', 
    '#124761', '#477150', '#D69446', '#051F5A', '#E19752', '#EF9B67',] # '#FCC4E3', '#07225B', '#447052', '#D69446', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960', '#303960',

#-------------------------------------------------------------------------------

# var_dict = {
#     'T_s' : {
#         'symbol' : r"$T_s$",
#         'label' : r"$T_s$ (°C)",
#         'unit' : r"°C",
#         'der' : 'dLE_dTs',
#         'color' : red
#     },
#     'r_aH': {
#         'symbol' : r"$r_{aH}$",
#         'label' : r"$r_{aH}$ (s m$^{-1}$)",
#         'unit' : r"s m$^{-1}$",
#         'der' : 'dLE_draH',
#         'color' : purple2
#     },
#     'T_a' : {
#         'symbol' : r"$T_a$",
#         'label' : r"$T_a$ (°C)",
#         'unit' : r"°C",
#         'der' : 'dLE_dTa',
#         'color' : blue2
#     },
#     'h_r' : {
#         'symbol' : r"$h_r$",
#         'label' : r"$h_r$ (%)",
#         'unit' : r"%",
#         'der' : 'dLE_dhr',
#         # 'tower_col' : 'RH',
#         'color' : green2
#     },
#     'SW_IN' : {
#         'symbol' : r"$R_{\mathrm{SW}}^{\downarrow}$",
#         'label' : r"$R_{\mathrm{SW}}^{\downarrow}$ (W m$^{-2}$)",
#         'unit' : r"W m$^{-2}$",
#         'der' : 'dLE_dRsw',
#         'color' : orange
#     },    
#     'LE' : {
#         'symbol' : r"$\lambda E$",
#         'label' : r"$\lambda E$ (W m$^{-2}$)",
#         'unit' : r"W m$^{-2}$"
#     },
#     'H' : {
#         'symbol' : r"$H$",
#         'label' : r"$H$ (W m$^{-2}$)",
#         'unit' : r"W m$^{-2}$",
#         'color' : None,
#     },
#     'u_star' : {
#         'symbol' : r"$u_{*}$",
#         'label' : r"$u_{*}$ (m s$^{-1}$)",
#         'unit' : r"m s$^{-1}$",
#         'tower_col' : 'ustar',
#         'color' : None,
#     },
#     'p_a' : {
#         'symbol' : r"$p_a$",
#         'label' : r"$p_a$ (kPa)",
#         'unit' : 'kPa'
#     },
#     'u' : {
#         'symbol' : r"$u$",
#         'label' : r"$u$ (m s$^{-1}$)",
#         'unit' : r"m s$^{-1}$",
#         'color' : sky,
#     },
#     'LW_IN' : {
#         'symbol' : r"$R_{\mathrm{LW}}^{\downarrow}$",
#         'label' : r"$R_{\mathrm{LW}}^{\downarrow}$ (W m$^{-2}$)",
#         'unit' : r"W m$^{-2}$",
#         'der' : 'dLE_dRsw',
#         'color' : red
#     },    
#     'SW_OUT' : {
#         'symbol' : r"$R_{\mathrm{SW}}^{\uparrow}$",
#         'label' : r"$R_{\mathrm{SW}}^{\uparrow}$ (W m$^{-2}$)",
#         'unit' : r"W m$^{-2}$",
#         'color' : gold
#     },    
#     'LW_OUT' : {
#         'symbol' : r"$R_{\mathrm{LW}}^{\uparrow}$",
#         'label' : r"$R_{\mathrm{LW}}^{\uparrow}$ (W m$^{-2}$)",
#         'unit' : r"W m$^{-2}$",
#         'color' : salmon
#     },    
#     'R_n' : {
#         'symbol' : r"$R_n$",
#         'label' : r"$R_n$ (W m$^{-2}$)",
#         'unit' : r"W m$^{-2}$",
#         'color' : maroon
#     },    
#     'dLE_dTs' : {
#         'symbol' : r"$\frac{\partial \lambda E}{\partial T_s}$",
#         'label' : r"$\frac{\partial \lambda E}{\partial T_s}$ (W m$^{-2}$ °C$^{-1}$)"
#     },
#     'dLE_draH' : {
#         'symbol' : r"$\frac{\partial \lambda E}{\partial r_{aH}}$",
#         'label' : r"$\frac{\partial \lambda E}{\partial r_{aH}}$ (W m$^{-2}$ s$^{-1}$ m)"
#     },
#     'dLE_dTa' : {
#         'symbol' : r"$\frac{\partial \lambda E}{\partial T_a}$",
#         'label' : r"$\frac{\partial \lambda E}{\partial T_a}$ (W m$^{-2}$ °C$^{-1}$)"
#     },
#     'dLE_dhr' : {
#         'symbol' : r"$\frac{\partial \lambda E}{\partial h_r}$",
#         'label' : r"$\frac{\partial \lambda E}{\partial h_r}$ (W m$^{-2}$ %$^{-1}$)"
#     },
#     'dLE_dRsw' : {
#         'symbol' : r"$\frac{\partial \lambda E}{\partial R_{\mathrm{sw}}^{\downarrow}}$",
#         'label' : r"$\frac{\partial \lambda E}{\partial R_{\mathrm{sw}}^{\downarrow}}$ (W m$^{-2}$ W$^{-1}$ m$^{2}$)"
#     }
# }

# '#3aaa00', '#4fbbaf', '#77cfd2', '#a1e3e8', '#cbf7ff'
# '#3aaa00', '#47b56f', '#52bdbe', '#6bc9cb', '#83d5d8', '#9be0e5', '#b3ecf2', '#cbf7ff'


# c_Ts = '#E4605B' #CC573D'
# c_rH = '#F4BCBF'
# c_Ta = '#3AA5C1' #'#378D9C'
# c_Ta1 = '#086D79'    # '#244B52'
# c_Ta2 = c_Ta
# c_hr = green2 #'#BECC5D'
# c_hr1 = green1 #'#839F30'
# c_hr2 = c_hr
# c_pa = '#CEDAED'
# c_pa1 = '#6788C4'
# c_ps = c_pa1
# c_pa2 = c_pa
# c_SWIN = '#FEBC11' #D6A550'
# c_u = purple1
# c_LWIN = red
# c_LWOUT = c_Ts
# c_SWOUT = gold
# c_Rn = maroon

# c_Ts = '#006e0c'

# c_Ta1, c_Ta2 = '#000e4c', '#001a66'
# c_Ta = c_Ta2

# c_SWIN = '#003176' #D6A550'
# c_rH = '#dbedf3'


# c_hr1, c_hr2 = '#158ab1', '#4ea6c4'
# c_hr = c_hr2

# c_ps, c_pa = '#b7dbe7', '#dbedf3'
# c_pa1,c_pa2 = '#b7dbe7', '#dbedf3'


# c_u = purple1
# c_LWIN = red
# c_LWOUT = c_Ts
# c_SWOUT = gold
# c_Rn = maroon 

# c_list = [
#     '#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', 
#     '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', 
#     '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', 
#     '#17becf', '#9edae5'
# ]

# sRGB hex codes
# c_Ts = '#3C6333' #8A6F24'

# # c_Ta1, c_Ta2 = '#8b9641', '#b1cb40'
# c_Ta1, c_Ta2 = '#4D9C44', '#93C93F' #8b9641', '#ABB964'
# c_Ta = c_Ta2

# c_SWIN = '#DCEED7' #D6A550'
# c_rH = '#004646'


# c_hr1, c_hr2 = '#AFDFDC', '#60B9BA'
# c_hr = c_hr2

# c_ps, c_pa = '#086d79', '#086d79'
# c_pa1,c_pa2 = '#006F7B', '#005B60'


# c_u = purple1
# c_LWIN = red
# c_LWOUT = c_Ts
# c_SWOUT = gold
# c_Rn = maroon 

sRGB = ['#3C6333', '#4D9C44', '#93C93F', '#DCEED7', '#AFDFDC', '#60B9BA', '#006F7B', '#005B60', '#004646']
adobe_RGB = ['#4B6339', '#6B9933', '#A3CA4A', '#E3FBDD', '#BDE4DF', '#80B8B9', '#2E6F7A', '#2A5B60', '#294846']
RGB = ['#2F5226', '#418D1A', '#81C52C', '#D2FCD5', '#9EE0D8', '#50ACAC', '#005D68', '#00494E', '#073735']
native = ['#456238', '#629938', '#9ECA53', '#e0fadf', '#b8e3df', '#76B7B9', '#086d79', '#12595F', '#1b4544']

#------------------------------------------------------------------------------

c_Ts,c_Ta1,c_Ta2,c_SWIN, c_hr1, c_hr2, c_pa1, c_pa2, c_rH = RGB

# c_Ts = '#456238' #8A6F24'
# c_Ta1, c_Ta2 = '#629938', '#9ECA53' #8b9641', '#ABB964'
# c_SWIN = '#e0fadf' #D6A550'
# c_hr1, c_hr2 = '#b8e3df', '#76B7B9'
# c_pa1,c_pa2 = '#086d79', '#12595F'
# c_rH = '#1b4544'

# c_Ta1, c_Ta2 = '#8b9641', '#b1cb40'
c_Ta = c_Ta2
c_hr = c_hr2

c_ps, c_pa = '#086d79', '#086d79'



c_u = purple1
c_LWIN = red
c_LWOUT = c_Ts
c_SWOUT = gold
c_Rn = maroon 



var_dict = {
    'T_s' : {
        'symbol' : r"$T_s$",
        'label' : r"$T_s$ (°C)",
        'unit' : r"°C",
        'der' : 'dLE_dTs',
        'tower_col' : 'T_s_CNR4',
        'color' : c_Ts, # darkblue,
    },
    'r_H': {
        'symbol' : r"$r_{H}$",
        'label' : r"$r_{H}$ (s m$^{-1}$)",
        'unit' : r"s m$^{-1}$",
        'der' : 'dLE_drH',
        'tower_col' : 'r_H_CNR4',
        'color' : c_rH # pink1
    },
    'T_a' : {
        'symbol' : r"$T_a$",
        'label' : r"$T_a$ (°C)",
        'unit' : r"°C",
        'der' : 'dLE_dTa',
        'der_br' : ['dLE_dTa1', 'dLE_dTa2'],
        'color' : c_Ta  # blue2,
    },
    'h_r' : {
        'symbol' : r"$h_r$",
        'label' : r"$h_r$ (%)",
        'unit' : r"%",
        'der' : 'dLE_dhr',
        'der_br' : ['dLE_dhr1', 'dLE_dhr2'],
        'color' : c_hr  # green2
    },
    'SW_IN' : {
        'symbol' : r"$R_{\mathrm{SW}}^{\downarrow}$",
        'label' : r"$R_{\mathrm{SW}}^{\downarrow}$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
        'der' : 'dLE_dRsw',
        'color' : c_SWIN    #orange
    },
    'p_a' : {
        'symbol' : r"$p_a$",
        'label' : r"$p_a$ (kPa)",
        'unit' : r"kPa",
        'der' : 'dLE_dpa',
        'der_br' : ['dLE_dpa1', 'dLE_dpa2'],
        'color' : c_pa  #pink2,
    },    
    'p_s' : {
        'symbol' : r"$p_s$",
        'label' : r"$p_s$ (kPa)",
        'unit' : r"kPa",
        'der' : 'dLE_dps',
        'color' : c_ps  #pink1,
    },    
    'T_a1' : {
        'symbol' : r"$T_{a1}$",
        'label' : r"$T_{a1}$ (°C)",
        'unit' : r"°C",
        'der' : 'dLE_dTa1',
        'color' : c_Ta1     #blue1,
    },
    'T_a2' : {
        'symbol' : r"$T_{a2}$",
        'label' : r"$T_{a2}$ (°C)",
        'unit' : r"°C",
        'der' : 'dLE_dTa2',
        'color' : c_Ta2     #blue2,
    },
    'h_r1' : {
        'symbol' : r"$h_{r1}$",
        'label' : r"$h_{r1}$ (%)",
        'unit' : r"%",
        'der' : 'dLE_dhr1',
        'color' : c_hr1     #green1
    },
    'h_r2' : {
        'symbol' : r"$h_{r2}$",
        'label' : r"$h_{r2}$ (%)",
        'unit' : r"%",
        'der' : 'dLE_dhr2',
        'color' : c_hr2     #green2
    },
    'p_a1' : {
        'symbol' : r"$p_{a1}$",
        'label' : r"$p_{a1}$ (kPa)",
        'unit' : r"kPa",
        'der' : 'dLE_dpa1',
        'color' : c_pa1     #purple1
    },   
    'p_a2' : {
        'symbol' : r"$p_{a2}$",
        'label' : r"$p_{a2}$ (kPa)",
        'unit' : r"kPa",
        'der' : 'dLE_dpa2',
        'color' : c_pa2     #purple2
    },     
    'LE' : {
        'symbol' : r"$\lambda E$",
        'label' : r"$\lambda E$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
        'color' : None,
    },
    'H' : {
        'symbol' : r"$H$",
        'label' : r"$H$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
        'color' : None,
    },
    'dLE_dTs' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial T_s}$",
        'label' : r"$\frac{\partial \lambda E}{\partial T_s}$ (W m$^{-2}$ °C$^{-1}$)"
    },
    'dLE_drH' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial r_{H}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial r_{H}}$ (W m$^{-2}$ s$^{-1}$ m)"
    },
    'dLE_dTa' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial T_a}$",
        'label' : r"$\frac{\partial \lambda E}{\partial T_a}$ (W m$^{-2}$ °C$^{-1}$)"
    },
    'dLE_dhr' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial h_r}$",
        'label' : r"$\frac{\partial \lambda E}{\partial h_r}$ (W m$^{-2}$ %$^{-1}$)"
    },
    'dLE_dRsw' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial R_{\mathrm{SW}}^{\downarrow}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial R_{\mathrm{SW}}^{\downarrow}}$ (W m$^{-2}$ W$^{-1}$ m$^{2}$)"
    },
    'dLE_dpa' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial p_a}$",
        'label' : r"$\frac{\partial \lambda E}{\partial p_a}$ (W m$^{-2}$ kPa$^{-1}$)"
    },
    'dLE_dps' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial p_s}$",
        'label' : r"$\frac{\partial \lambda E}{\partial p_s}$ (W m$^{-2}$ kPa$^{-1}$)"
    },
    'dLE_dTa1' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial T_{a1}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial T_{a1}}$ (W m$^{-2}$ °C$^{-1}$)"
    },
    'dLE_dTa2' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial T_{a2}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial T_{a2}}$ (W m$^{-2}$ °C$^{-1}$)"
    },
    'dLE_dhr1' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial h_{r1}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial h_{r1}}$ (W m$^{-2}$ %$^{-1}$)"
    },
    'dLE_dhr2' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial h_{r2}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial h_{r2}}$ (W m$^{-2}$ %$^{-1}$)"
    },
    'dLE_dpa1' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial p_{a1}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial p_{a1}}$ (W m$^{-2}$ kPa$^{-1}$)"
    },
    'dLE_dpa2' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial p_{a2}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial p_{a2}}$ (W m$^{-2}$ kPa$^{-1}$)"
    },
    'u' : {
        'symbol' : r"$u$",
        'label' : r"$u$ (m s$^{-1}$)",
        'unit' : r"m s$^{-1}$",
        'color' : c_u   #sky,
    },
    'LW_IN' : {
        'symbol' : r"$R_{\mathrm{LW}}^{\downarrow}$",
        'label' : r"$R_{\mathrm{LW}}^{\downarrow}$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
        'der' : 'dLE_dRsw',
        'color' : c_LWIN    #red
    },    
    'SW_OUT' : {
        'symbol' : r"$R_{\mathrm{SW}}^{\uparrow}$",
        'label' : r"$R_{\mathrm{SW}}^{\uparrow}$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
        'color' : c_SWOUT   #gold
    },    
    'LW_OUT' : {
        'symbol' : r"$R_{\mathrm{LW}}^{\uparrow}$",
        'label' : r"$R_{\mathrm{LW}}^{\uparrow}$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
        'color' : c_LWOUT  #salmon
    },    
    'R_n' : {
        'symbol' : r"$R_n$",
        'label' : r"$R_n$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
        'color' : c_Rn  #maroon
    },  
    'u_star' : {
        'symbol' : r"$u_{*}$",
        'label' : r"$u_{*}$ (m s$^{-1}$)",
        'unit' : r"m s$^{-1}$",
        'tower_col' : 'ustar',
        'color' : None,
    },
}
