
### Generates final town data result with coordinates and population, etc.
# cities_file: allCountries.txt
# dict_file: merged.json
# out_file: result.csv

import sys
import math
import json

from config import *

with open('input/hanja_bias.txt', 'r') as f:
    hanja_bias = set(f.read())

def cvt_population(population):
    population = float(population)
    if population <= 0:
        return 0
    return round(math.sqrt(population) * 2)

def get_cjk_score(str):
    ideograph_len = len([c for c in str if ord(c) in range(0x4e00, 0x9fff + 1)])
    hangul_len = len([c for c in str if ord(c) in range(0xac00, 0xd7a3 + 1)])
    hiragana_len = len([c for c in str if ord(c) in range(0x3041, 0x3096 + 1)])
    katakana_len = len([c for c in str if ord(c) in range(0x30a1, 0x30f6 + 1)])

    ideograph_score = ideograph_len / len(str)
    hangul_score = hangul_len / len(str) / 2
    kana_score = (hiragana_len + katakana_len) / len(str) / 3
    bias_score = len([c for c in str if c in hanja_bias]) / len(str) / 2

    return ideograph_score + kana_score + hangul_score + bias_score

def decide_name(name, asciiName, alternateNames, merged_dict):
    cands = []
    cands.append(name)
    if name in merged_dict:
        cands.extend(merged_dict[name])
    if asciiName in merged_dict:
        cands.extend(merged_dict[asciiName])
    for n in alternateNames.split(','):
        if n in merged_dict:
            cands.extend(merged_dict[n])
    cands = list(set(cands))
    cands = sorted(cands, key=lambda s: get_cjk_score(s), reverse=True)
    return cands[0]

def gen_result(in_file, dict_file, out_file):
    with open(in_file, 'r') as in_f, open(dict_file, 'r') as dict_f, open(out_file, 'w') as out_f:
        out_f.write(f'{NORTH},{EAST},{SOUTH},{WEST}\n')
        merged_dict = json.load(dict_f)
        lines = 0
        result = []
        for line in in_f:
            line = line.strip()
            [_, name, asciiName, alternateNames, latitude, longitude, _, _, _, _, _, _, _, _, population] = line.split('\t')[:15]
            latitude = float(latitude)
            longitude = float(longitude)
            if latitude > NORTH or latitude < SOUTH or longitude < WEST or longitude > EAST:
                continue
            population = int(population)
            size = 'S'
            city = '0'
            if population >= THRES_M:
                size = 'M'
            if population >= THRES_L:
                size = 'L'
            if population >= THRES_CITY:
                city = '1'
            name = decide_name(name, asciiName, alternateNames, merged_dict)
            population = cvt_population(population)
            if population == 0:
                continue
            result.append([name, population, city, latitude, longitude])
        
        # Remove duplicates
        names = list(set([e[0] for e in result]))
        result = sorted(result, key=lambda e: e[1])
        result = {e[0]: e[1:] for e in result}
        result = [[name] + result[name] for name in names]
        result = sorted(result, key=lambda e: e[1], reverse=True)

        for [name, population, city, latitude, longitude] in result:
            out_f.write(f'{name}\t{population}\t{city}\t{latitude}\t{longitude}\n')
            lines += 1
            if lines % 10000 == 0:
                print(f'Wrote {lines} lines')

def main(args):
    script = sys.argv[0]
    args = sys.argv[1:]
    if len(args) != 3:
        print(f'Usage: {script} in_file dict_file out_file', file=sys.stderr)
        sys.exit(1)
    [in_file, dict_file, out_file] = args
    gen_result(in_file, dict_file, out_file)

if __name__ == '__main__':
    main(sys.argv)
