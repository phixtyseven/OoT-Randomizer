# CUSTOMPOOLS.PY
from collections import OrderedDict
import Utils


# Fake class
def PoolConfig(pools: list, settings: list):
    return {
            'pools':    OrderedDict(pools),
            'settings': OrderedDict(settings),
        }


backups = {}
backups['colors_single'] = PoolConfig(
        pools = {
            'Tunics': [
                ["Kokiri Green",  ['#1E691B']],
                ["Goron Red",     ['#641400']],
                ["Zora Blue",     ['#003C64']],
                ["Black",         ['#303030']],
                ["White",         ['#F0F0FF']],
                ["Azure Blue",    ['#139ED8']],
                ["Vivid Cyan",    ['#13E9D8']],
                ["Light Red",     ['#F87C6D']],
                ["Fuchsia",       ['#FF00FF']],
                ["Purple",        ['#953080']],
                ["Majora Purple", ['#50529A']],
                ["Twitch Purple", ['#6441A5']],
                ["Purple Heart",  ['#8A2BE2']],
                ["Persian Rose",  ['#FF1493']],
                ["Dirty Yellow",  ['#E0D860']],
                ["Blush Pink",    ['#F86CF8']],
                ["Hot Pink",      ['#FF69B4']],
                ["Rose Pink",     ['#FF90B3']],
                ["Orange",        ['#E07940']],
                ["Gray",          ['#A0A0B0']],
                ["Gold",          ['#D8B060']],
                ["Silver",        ['#D0F0FF']],
                ["Beige",         ['#C0A0A0']],
                ["Teal",          ['#30D0B0']],
                ["Blood Red",     ['#830303']],
                ["Blood Orange",  ['#FE4B03']],
                ["Royal Blue",    ['#400090']],
                ["Sonic Blue",    ['#5090E0']],
                ["NES Green",     ['#00D000']],
                ["Dark Green",    ['#002518']],
                ["Lumen",         ['#508CF0']],
                ],
            },
        settings = [
            ['color_tunic_kokiri', ['Tunics']],
            ['color_tunic_goron',  ['Tunics']],
            ['color_tunic_zora',   ['Tunics']],
            ]
        )
backups['colors_double'] = PoolConfig(
        pools = {
            'Navi': [                 # inner,    outer
                ["Gold",              ['#FECC3C', '#FEC007']],
                ["White",             ['#FFFFFF', '#0000FF']],
                ["Green",             ['#00FF00', '#00FF00']],
                ["Light Blue",        ['#9696FF', '#9696FF']],
                ["Yellow",            ['#FFFF00', '#C89B00']],
                ["Red",               ['#FF0000', '#FF0000']],
                ["Magenta",           ['#FF00FF', '#C8009B']],
                ["Black",             ['#000000', '#000000']],
                ["Tatl",              ['#FFFFFF', '#C89800']],
                ["Tael",              ['#49146C', '#FF0000']],
                ["Fi",                ['#2C9EC4', '#2C1983']],
                ["Ciela",             ['#E6DE83', '#C6BE5B']],
                ["Epona",             ['#D14902', '#551F08']],
                ["Ezlo",              ['#629C5F', '#3F5D37']],
                ["King of Red Lions", ['#A83317', '#DED7C5']],
                ["Linebeck",          ['#032660', '#EFFFFF']],
                ["Loftwing",          ['#D62E31', '#FDE6CC']],
                ["Midna",             ['#192426', '#D28330']],
                ["Phantom Zelda",     ['#977A6C', '#6F4667']],
                ],
            },
        settings = [
            ['color_navi_idle',  ['Navi']],
            ['color_navi_npc',   ['Navi']],
            ['color_navi_enemy', ['Navi']],
            ['color_navi_prop',  ['Navi']],
            ]
        )
    

def load_pc_file(filename):
    extended = filename + '.yml'
    pc_file = Utils.object_from_yaml(Utils.data_path(extended))
    return PoolConfig(pc_file['pools'], pc_file['settings'])


def update_pool_configs():
    for fn in ('colors_single', 'colors_double'):
        pool_configs[fn] = load_pc_file(fn)


pool_configs = backups
update_pool_configs()
