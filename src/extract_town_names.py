
### Extracts all town names from GeoNames data
# in_file: AllCountries.txt
# out_file: town_names.txt

import sys

def extract_town_names(in_file, out_file):
    result = set()
    with open(in_file, 'r') as in_f:
        for line in in_f:
            line = line.strip()
            if not line:
                continue
            [name, ascii_name, alternate_names] = line.split('\t')[1:4]
            name, ascii_name = name.strip(), ascii_name.strip()
            alternate_names = alternate_names.split(',')
            result.add(name)
            result.add(ascii_name)
            for n in alternate_names:
                result.add(n.strip())
    result = list(sorted(list(result)))
    with open(out_file, 'w') as out_f:
        for name in result:
            if name == '':
                continue
            out_f.write(f'{name}\n')

def main(args):
    script = sys.argv[0]
    args = sys.argv[1:]
    if len(args) != 2:
        print(f'Usage: {script} in_file out_file', file=sys.stderr)
        sys.exit(1)
    [in_file, out_file] = args
    extract_town_names(in_file, out_file)

if __name__ == '__main__':
    main(sys.argv)
