from version import __version__
import random
import Colors
import Sounds as sfx
from Utils import keywdify


def patch_cosmetics(settings, rom):
    log = CosmeticsLog(settings)

    # re-seed for aesthetic effects. They shouldn't be affected by the generation seed
    random.seed()

    # Set default targeting option to Hold
    if settings.default_targeting == 'hold':
        rom.write_byte(0xB71E6D, 0x01)
    else:
        rom.write_byte(0xB71E6D, 0x00)

    # patch music
    if settings.background_music == 'random':
        restore_music(rom)
        log.bgm = randomize_music(rom)
    elif settings.background_music == 'off':
        disable_music(rom)
    else:
        restore_music(rom)

    # Configurable Colors
    rgb_config = [
          (settings.color_tunic_kokiri, Colors.RGB_Setting.TUNIC_KOKIRI),
          (settings.color_tunic_goron,  Colors.RGB_Setting.TUNIC_GORON),
          (settings.color_tunic_zora,   Colors.RGB_Setting.TUNIC_ZORA),
          (settings.color_navi_idle,    Colors.RGB_Setting.NAVI_IDLE),
          (settings.color_navi_npc,     Colors.RGB_Setting.NAVI_NPC),
          (settings.color_navi_enemy,   Colors.RGB_Setting.NAVI_ENEMY),
          (settings.color_navi_prop,    Colors.RGB_Setting.NAVI_PROP),
    ]

    # Evaluate the user's selection and patch all hooks accordingly
    for selection, setting in rgb_config:
        if selection == 'default':
            for hook_list in setting.hook_lists:
                for hook in hook_list:
                    rgb_bytes = rom.original[hook:hook+3]
                    rom.write_bytes(hook, rgb_bytes)
        elif selection == 'custom':
            raise ValueError("Sorry, immediate custom colors are not handled in this version.")
        elif selection == 'completely_random':
            for hook_list in setting.hook_lists:
                rgb_bytes = [random.getrandbits(8), random.getrandbits(8), random.getrandbits(8)]
                for hook in hook_list:
                    rom.write_bytes(hook, rgb_bytes)
        elif selection in setting.random_pools:
            poolname = setting.random_pools[selection].lstrip('Random ')
            rc = random.choice(setting.origin['pools'][poolname])
            for i, hook_list in enumerate(setting.hook_lists):
                rgb_bytes = Colors.bytes_from_hexcode(str(rc[1][i]))
                for hook in hook_list:
                    rom.write_bytes(hook, rgb_bytes)
        elif selection in setting.pool_choices:
            for i, hook_list in enumerate(setting.hook_lists):
                hexcode = setting.patch_dict[keywdify(setting.pool_choices[selection])][i]
                rgb_bytes = Colors.bytes_from_hexcode(hexcode)
                for hook in hook_list:
                    rom.write_bytes(hook, rgb_bytes)
        else:
            raise ValueError("This value is unhandled as a color: ", selection)

    # Configurable Sound Effects
    sfx_config = [
          (settings.sfx_hover_boots,    sfx.SoundHooks.BOOTS_HOVER),
          (settings.sfx_menu_select,    sfx.SoundHooks.MENU_SELECT),
          (settings.sfx_menu_cursor,    sfx.SoundHooks.MENU_CURSOR),
          (settings.sfx_horse_neigh,    sfx.SoundHooks.HORSE_NEIGH),
          (settings.sfx_navi,           sfx.SoundHooks.NAVI),
          (settings.sfx_low_hp,         sfx.SoundHooks.HP_LOW),
          (settings.sfx_nightfall,      sfx.SoundHooks.NIGHTFALL),
    ]
    sound_dict = sfx.get_patch_dict()

    for selection, hook in sfx_config:
        if selection == 'default':
            for loc in hook.value.locations:
                sound_id = int.from_bytes((rom.original[loc:loc+2]), byteorder='big', signed=False)
                rom.write_int16(loc, sound_id)
        else:
            if selection == 'random-choice':
                selection = random.choice(sfx.get_hook_pool(hook)).value.keyword
            elif selection == 'random-ear-safe':
                selection = random.choice(sfx.no_painful).value.keyword
            elif selection == 'completely-random':
                selection = random.choice(sfx.standard).value.keyword
            sound_id  = sound_dict[selection]
            for loc in hook.value.locations:
                rom.write_int16(loc, sound_id)
        log.sfx[hook.value.name] = selection

    # Player Instrument
    instruments = {
           #'none':            0x00,
            'ocarina':         0x01,
            'malon':           0x02,
            'whistle':         0x03,
            'harp':            0x04,
            'grind_organ':     0x05,
            'flute':           0x06,
           #'another_ocarina': 0x07,
            }
    if settings.sfx_ocarina != 'random':
        choice = settings.sfx_ocarina
    else:
        choice = random.choice(list(instruments.keys()))
    rom.write_byte(0x00B53C7B, instruments[choice])
    log.sfx['Ocarina'] = choice

    return log


# Format: (Title, Sequence ID)
bgm_sequence_ids = [
    ('Hyrule Field', 0x02),
    ('Dodongos Cavern', 0x18),
    ('Kakariko Adult', 0x19),
    ('Battle', 0x1A),
    ('Boss Battle', 0x1B),
    ('Inside Deku Tree', 0x1C),
    ('Market', 0x1D),
    ('Title Theme', 0x1E),
    ('House', 0x1F),
    ('Jabu Jabu', 0x26),
    ('Kakariko Child', 0x27),
    ('Fairy Fountain', 0x28),
    ('Zelda Theme', 0x29),
    ('Fire Temple', 0x2A),
    ('Forest Temple', 0x2C),
    ('Castle Courtyard', 0x2D),
    ('Ganondorf Theme', 0x2E),
    ('Lon Lon Ranch', 0x2F),
    ('Goron City', 0x30),
    ('Miniboss Battle', 0x38),
    ('Temple of Time', 0x3A),
    ('Kokiri Forest', 0x3C),
    ('Lost Woods', 0x3E),
    ('Spirit Temple', 0x3F),
    ('Horse Race', 0x40),
    ('Ingo Theme', 0x42),
    ('Fairy Flying', 0x4A),
    ('Deku Tree', 0x4B),
    ('Windmill Hut', 0x4C),
    ('Shooting Gallery', 0x4E),
    ('Sheik Theme', 0x4F),
    ('Zoras Domain', 0x50),
    ('Shop', 0x55),
    ('Chamber of the Sages', 0x56),
    ('Ice Cavern', 0x58),
    ('Kaepora Gaebora', 0x5A),
    ('Shadow Temple', 0x5B),
    ('Water Temple', 0x5C),
    ('Gerudo Valley', 0x5F),
    ('Potion Shop', 0x60),
    ('Kotake and Koume', 0x61),
    ('Castle Escape', 0x62),
    ('Castle Underground', 0x63),
    ('Ganondorf Battle', 0x64),
    ('Ganon Battle', 0x65),
    ('Fire Boss', 0x6B),
    ('Mini-game', 0x6C)
]


def randomize_music(rom):
    log = {}

    # Read in all the Music data
    bgm_data = []
    for bgm in bgm_sequence_ids:
        bgm_sequence = rom.read_bytes(0xB89AE0 + (bgm[1] * 0x10), 0x10)
        bgm_instrument = rom.read_int16(0xB89910 + 0xDD + (bgm[1] * 2))
        bgm_data.append((bgm[0], bgm_sequence, bgm_instrument))

    # shuffle data
    random.shuffle(bgm_data)

    # Write Music data back in random ordering
    for bgm in bgm_sequence_ids:
        bgm_name, bgm_sequence, bgm_instrument = bgm_data.pop()
        rom.write_bytes(0xB89AE0 + (bgm[1] * 0x10), bgm_sequence)
        rom.write_int16(0xB89910 + 0xDD + (bgm[1] * 2), bgm_instrument)
        log[bgm[0]] = bgm_name

    # Write Fairy Fountain instrument to File Select (uses same track but different instrument set pointer for some reason)
    rom.write_int16(0xB89910 + 0xDD + (0x57 * 2), rom.read_int16(0xB89910 + 0xDD + (0x28 * 2)))
    return log


def disable_music(rom):
    # First track is no music
    blank_track = rom.read_bytes(0xB89AE0 + (0 * 0x10), 0x10)
    for bgm in bgm_sequence_ids:
        rom.write_bytes(0xB89AE0 + (bgm[1] * 0x10), blank_track)


def restore_music(rom):
    # Restore all music from original
    for bgm in bgm_sequence_ids:
        bgm_sequence = rom.original[0xB89AE0 + (bgm[1] * 0x10): 0xB89AE0 + (bgm[1] * 0x10) + 0x10]
        rom.write_bytes(0xB89AE0 + (bgm[1] * 0x10), bgm_sequence)
        bgm_instrument = rom.original[0xB89910 + 0xDD + (bgm[1] * 2): 0xB89910 + 0xDD + (bgm[1] * 2) + 0x02]
        rom.write_bytes(0xB89910 + 0xDD + (bgm[1] * 2), bgm_instrument)

    # restore file select instrument
    bgm_instrument = rom.original[0xB89910 + 0xDD + (0x57 * 2): 0xB89910 + 0xDD + (0x57 * 2) + 0x02]
    rom.write_bytes(0xB89910 + 0xDD + (0x57 * 2), bgm_instrument)


class CosmeticsLog(object):

    def __init__(self, settings):
        self.settings = settings
        self.tunic_colors = {}
        self.navi_colors = {}
        self.sfx = {}
        self.bgm = {}


    def to_file(self, filename):
        with open(filename, 'w') as outfile:
            outfile.write(self.cosmetics_output())


    def cosmetics_output(self):
        output = ''
        output += 'OoT Randomizer Version %s - Cosmetics Log\n' % (__version__)

        format_string = '\n{key:{width}} {value}'
        #keys = list(self.tunic_colors.keys()) + list(self.navi_colors.keys()) + list(self.sfx.keys()) + ['Default Targeting Option', 'Background Music']
        #padding = 1 + len(max(keys, key=len))
        padding = 40

        output += format_string.format(key='Default Targeting Option:', value=self.settings.default_targeting, width=padding)
        output += format_string.format(key='Background Music:', value=self.settings.background_music, width=padding)

        output += '\n\nColors:\n'
        for tunic, options in self.tunic_colors.items():
            color_option_string = '{option} (#{color})'
            output += format_string.format(key=tunic+':', value=color_option_string.format(option=options['option'], color=options['color']), width=padding)
        for navi_action, list in self.navi_colors.items():
            i = 0
            for options in list:
                color_option_string = '{option} (#{color1}, #{color2})'
                output += format_string.format(key=(navi_action+':') if i == 0 else '', value=color_option_string.format(option=options['option'], color1=options['color1'], color2=options['color2']), width=padding)
                i += 1

        output += '\n\nSFX:\n'
        for key, value in self.sfx.items():
            output += format_string.format(key=key+':', value=value, width=padding)

        if self.settings.background_music == 'random':
            #music_padding = 1 + len(max(self.bgm.keys(), key=len))
            music_padding = 40
            output += '\n\nBackground Music:\n'
            for key, value in self.bgm.items():
                output += format_string.format(key=key+':', value=value, width=music_padding)

        return output
