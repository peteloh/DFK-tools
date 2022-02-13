
import json

FAIL_ON_NOT_FOUND = False

ALPHABET = '123456789abcdefghijkmnopqrstuvwx'

rarity = {
    0: "common",
    1: "uncommon",
    2: "rare",
    3: "legendary",
    4: "mythic",
}

_class = {
    0: "warrior",
    1: "knight",
    2: "thief",
    3: "archer",
    4: "priest",
    5: "wizard",
    6: "monk",
    7: "pirate",
    16: "paladin",
    17: "darkKnight",
    18: "summoner",
    19: "ninja",
    24: "dragoon",
    25: "sage",
    28: "dreadKnight"
}

visual_traits = {
    0: 'gender',
    1: 'headAppendage',
    2: 'backAppendage',
    3: 'background',
    4: 'hairStyle',
    5: 'hairColor',
    6: 'visualUnknown1',
    7: 'eyeColor',
    8: 'skinColor',
    9: 'appendageColor',
    10: 'backAppendageColor',
    11: 'visualUnknown2'
}

stat_traits = {
    0: 'class',
    1: 'subClass',
    2: 'profession',
    3: 'passive1',
    4: 'passive2',
    5: 'active1',
    6: 'active2',
    7: 'statBoost1',
    8: 'statBoost2',
    9: 'statsUnknown1',
    10: 'element',
    11: 'statsUnknown2'
}

professions = {
    0: 'mining',
    2: 'gardening',
    4: 'fishing',
    6: 'foraging',
}

stats = {
    0: 'STR',
    2: 'AGI',
    4: 'INT',
    6: 'WIS',
    8: 'LCK',
    10: 'VIT',
    12: 'END',
    14: 'DEX'
}

elements = {
    0: 'fire',
    2: 'water',
    4: 'earth',
    6: 'wind',
    8: 'lightning',
    10: 'ice',
    12: 'light',
    14: 'dark',
}


def parse_rarity(id):
    value = rarity.get(id, None)
    if FAIL_ON_NOT_FOUND and value is None:
        raise Exception("Rarity not found")
    return value


def parse_class(id):
    value = _class.get(id, None)
    if FAIL_ON_NOT_FOUND and value is None:
        raise Exception("Class not found")
    return value


def parse_profession(id):
    value = professions.get(id, None)
    if FAIL_ON_NOT_FOUND and value is None:
        raise Exception("Profession not found")
    return value


def parse_stat(id):
    value = stats.get(id, None)
    if FAIL_ON_NOT_FOUND and value is None:
        raise Exception("Stat not found")
    return value


def parse_element(id):
    value = elements.get(id, None)
    if FAIL_ON_NOT_FOUND and value is None:
        raise Exception("Element not found")
    return value


def genes2traits(genes):
    traits = []

    stat_raw_kai = "".join(__genesToKai(genes).split(' '))
    for ki in range(0, len(stat_raw_kai)):
        kai = stat_raw_kai[ki]
        value_num = __kai2dec(kai)
        traits.append(value_num)

    assert len(traits) == 48
    arranged_traits = [[], [], [], []]
    for i in range(0, 12):
        index = i << 2
        for j in range(0, len(arranged_traits)):
            arranged_traits[j].append(traits[index + j])

    arranged_traits.reverse()
    return arranged_traits


def parse_stat_genes(genes):
    traits = genes2traits(genes)
    stats = parse_stat_trait(traits[0])
    r1 = parse_stat_trait(traits[1])
    r2 = parse_stat_trait(traits[2])
    r3 = parse_stat_trait(traits[3])

    stats['r1'] = r1
    stats['r2'] = r2
    stats['r3'] = r3
    stats['raw'] = genes

    return stats


def parse_stat_trait(trait):

    if len(trait) != 12:
        raise Exception("Traits must be an array of 12")

    stats = {}
    for i in range(0, 12):
        stat_trait = stat_traits.get(i, None)
        stats[stat_trait] = trait[i]

    stats['class'] = parse_class(stats['class'])
    stats['subClass'] = parse_class(stats['subClass'])

    stats['profession'] = parse_profession(stats['profession'])

    stats['passive1'] = parse_class(stats['passive1'])
    stats['passive2'] = parse_class(stats['passive2'])
    stats['active1'] = parse_class(stats['active1'])
    stats['active2'] = parse_class(stats['active2'])

    stats['statBoost1'] = parse_stat(stats['statBoost1'])
    stats['statBoost2'] = parse_stat(stats['statBoost2'])
    stats['statsUnknown1'] = stats.get(stats['statsUnknown1'], None)  # parse_stat(stat_genes['statsUnknown1'])
    stats['statsUnknown2'] = stats.get(stats['statsUnknown2'], None)  # parse_stat(stat_genes['statsUnknown2'])

    stats['element'] = parse_element(stats['element'])

    return stats


def parse_visual_genes(genes):
    visual_genes = {}
    visual_genes['raw'] = genes

    visual_raw_kai = "".join(__genesToKai(visual_genes['raw']).split(' '))

    for ki in range(0, len(visual_raw_kai)):
        stat_trait = visual_traits.get(int(ki / 4), None)
        kai = visual_raw_kai[ki]
        value_num = __kai2dec(kai)
        visual_genes[stat_trait] = value_num

    visual_genes['gender'] = 'male' if visual_genes['gender'] == 1 else 'female'
    return visual_genes


def __genesToKai(genes):
    BASE = len(ALPHABET)

    buf = ''
    while genes >= BASE:
        mod = int(genes % BASE)
        buf = ALPHABET[int(mod)] + buf
        genes = (genes - mod) // BASE

    # Add the last 4 (finally).
    buf = ALPHABET[int(genes)] + buf

    # Pad with leading 1s.
    buf = buf.rjust(48, '1')

    return ' '.join(buf[i:i + 4] for i in range(0, len(buf), 4))


def __kai2dec(kai):
    return ALPHABET.index(kai)


def parse_names(names_raw_string):
    names_raw_string = names_raw_string\
        .replace("\\xf3", "ó") \
        .replace("\\xf2", "ò") \
        .replace("\\xe9", "é") \
        .replace("\\xe1", "á") \
        .replace("\\xc9", "É") \
        .replace("\\xed", "í") \
        .replace("\\xfa", "ú") \
        .replace("\\xec", "ì")

    if "\\x" in names_raw_string:
        raise Exception("Unhandled unicode found")

    return json.loads(names_raw_string)

def human_readable_auction(auction):
    human_readable = {}
    human_readable['seller'] = auction[0]
    human_readable['id'] = auction[1]
    human_readable['startingPrice'] = auction[2]
    human_readable['endingPrice'] = auction[3]
    human_readable['duration'] = auction[4]
    human_readable['startedAt'] = auction[5]
    human_readable['winner'] = auction[6]
    human_readable['open'] = auction[7]

    return human_readable


# Personal Utils
def long_stat(stat):
    long_stat = {
        "AGI": "agility",
        "STR": "strength",
        "END": "endurance",
        "LCK": "luck",
        "DEX": "dexterity",
        "WIS": "wisdom",
        "INT": "intelligence",
        "VIT": "vitality"
    }
    return long_stat[stat]

def ideal_professsion_stats(profession):
    ideal_professsion_stats = {
        "mining": ["STR", "END"],
        "gardening": ["WIS", "VIT"],
        "foraging": ["INT", "DEX"],
        "fishing": ["AGI", "LCK"]
    }
    return ideal_professsion_stats[profession]

def ideal_class_profession(mainClass):
    ideal_class_profession = {
        "warrior": "mining",
        "knight": "mining",
        "archer": "foraging",
        "thief": "fishing",
        "pirate": "mining",
        "monk": "mining",
        "wizard": "gardening",
        "priest": "gardening",
        "paladin": "mining",
        "darkknight": "mining",
        "ninja": "fishing",
        "summoner": "gardening",
        "dragoon": "mining",
        "sage": "gardening",
        "dreadknight": "mining"
    }
    return ideal_class_profession[mainClass]