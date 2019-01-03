# COLORS.PY
from enum import Enum
from collections import OrderedDict
import re

import CustomPools
from Utils import keywdify


RE_HEXCODE      = re.compile(r'^#[0-9A-Za-z]+$')
MSG_COLORFORMAT = "Colors must take the form #nnn or #nnnnnn. Instead found '{}'."
def bytes_from_hexcode(hexcode: str):
    matches = RE_HEXCODE.match(hexcode)
    if matches is None:
        raise ValueError(MSG_COLORFORMAT.format(hexcode))

    hc = hexcode.lstrip('#')
    if len(hc) == 3:
        hc = ''.join([''.join((i, i)) for i in hc])

    if len(hc) == 6:
        return tuple(int(hc[i:i+2], 16) for i in range(6) if i%2 == 0)
    else:
        raise ValueError(MSG_COLORFORMAT.format(hexcode))


class RGB_Setting(Enum):
                  # keyword,              label,          origin,            hook list(s)
    TUNIC_KOKIRI = ('color_tunic_kokiri', 'Kokiri Tunic', 'colors_single',   [[0xB6DA38]])
    TUNIC_GORON  = ('color_tunic_goron',  'Goron Tunic',  'colors_single',   [[0xB6DA3B]])
    TUNIC_ZORA   = ('color_tunic_zora',   'Zora Tunic',   'colors_single',   [[0xB6DA3E]])
    NAVI_IDLE    = ('color_navi_idle',    'Navi Idle',    'colors_double',   [
        [0xB5E184],
        [0xB5E188],
        ])
    NAVI_NPC     = ('color_navi_npc',     'Navi NPC',     'colors_double',   [
        [0xB5E194],
        [0xB5E198],
        ])
    NAVI_ENEMY   = ('color_navi_enemy',   'Navi Enemy',   'colors_double',   [
        [0xB5E19C, 0xB5E1BC],
        [0xB5E1A0, 0xB5E1C0],
        ])
    NAVI_PROP    = ('color_navi_prop',    'Navi Prop',    'colors_double',   [
        [0xB5E174, 0xB5E17C, 0xB5E18C, 0xB5E1A4, 0xB5E1AC, 0xB5E1B4, 0xB5E1C4, 0xB5E1CC, 0xB5E1D4],
        [0xB5E178, 0xB5E180, 0xB5E190, 0xB5E1A8, 0xB5E1B0, 0xB5E1B8, 0xB5E1C8, 0xB5E1D0, 0xB5E1D8],
    ])
    def __init__(self, keyword, label, origin, hook_lists):
        self.keyword      = keyword
        self.label        = label
        self.origin       = CustomPools.pool_configs[origin]
        self.hook_lists   = hook_lists
        self.pools        = {keywdify(p): p for p in self.origin['settings'][keyword]}
        pool0             = list(self.pools.values())[0]
        self.random_pools = {'random_' + p: ('Random ' + self.pools[p]) for p in list(self.pools.keys())}
        self.pool_choices = {keywdify(choice[0]): choice[0] for choice in self.origin['pools'][pool0]}
        self.patch_dict   = {keywdify(choice[0]): choice[1] for choice in self.origin['pools'][pool0]}
        self.choices      = {
                'default':            'Default',
                # I don't want to bother with custom right now
                #'custom':             'Custom Color',
                'completely_random':  'Completely Random',
                **self.random_pools,
                **self.pool_choices,
                }


if __name__ == '__main__':
    pass
