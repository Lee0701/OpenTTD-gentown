
### Filters out unneeded data from merged dictionary
# in_file: merged.json
# out_file: merged_filtered.json

import sys
import json

def filter_dict(in_file, out_file):
    with open(in_file, 'r') as in_f, open(out_file, 'w') as out_f:
        result = {}
        merged_dict = json.load(in_f)
        for key, values in merged_dict.items():
            if len(values) == 1:
                continue
            for value in values:
                if len([c for c in value if ord(c) in range(0x4e00, 0x9fff + 1)]) >= len(value) // 2:
                    if key not in result:
                        result[key] = []
                    result[key].append(value)
        json.dump(result, out_f, ensure_ascii=False, indent=2)

def main(args):
    script = sys.argv[0]
    args = sys.argv[1:]
    if len(args) != 2:
        print(f'Usage: {script} in_file out_file', file=sys.stderr)
        sys.exit(1)
    [in_file, out_file] = args
    filter_dict(in_file, out_file)

if __name__ == '__main__':
    main(sys.argv)
