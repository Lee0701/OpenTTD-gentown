
### Merges wikidata dictionaries
# in_files: {lang1}wiki.tsv,{lang2}wiki.tsv
# out_file: dict.json

import sys
import itertools
import json

def parse_dict(in_file):
    with open(in_file, 'r') as f:
        lines = f.read().splitlines()
    lines = [line.split('\t')[:2] for line in lines]
    result = {key: value for key, value in lines}
    return result

def merge_wikidata_dict(in_files, out_file):
    in_dicts = [parse_dict(in_file) for in_file in in_files]
    print(f'Merging {len(in_dicts)} dictionaries')
    ids = [d.keys() for d in in_dicts]
    ids = list(itertools.chain.from_iterable(ids))
    ids = list(set(ids))
    print(f'Found {len(ids)} unique ids')
    id_to_str = {}
    for id in ids:
        if id not in id_to_str:
            id_to_str[id] = []
        for d in in_dicts:
            if id in d:
                id_to_str[id].append(d[id])
    str_to_id = {}
    for id in ids:
        for r in id_to_str[id]:
            str_to_id[r] = id
    result = {}
    for id in ids:
        for str in id_to_str[id]:
            result[str] = id_to_str[id]
    with open(out_file, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def main(args):
    script = sys.argv[0]
    args = sys.argv[1:]
    if len(args) != 2:
        print(f'Usage: {script} in_files out_file', file=sys.stderr)
        sys.exit(1)
    [in_files, out_file] = args
    in_files = in_files.split(',')
    merge_wikidata_dict(in_files, out_file)

if __name__ == '__main__':
    main(sys.argv)
