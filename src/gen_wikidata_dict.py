
### Generates WikiData dictionary
# in_file: wikidatawiki-{date}-wb_items_per_site.sql
# site_id: {lang}wiki
# out_file: {lang}wiki.tsv

import sys
import re

head = 'INSERT INTO `wb_items_per_site` VALUES '
record_pat = re.compile(r"\(\d+?,\d+?,'[^']+?','[^']+?'\)[,;]")
field_pat = re.compile(r"(\d+|'.+?')")

def strip_quotes(str):
    if str.startswith("'") and str.endswith("'"):
        return str[1:-1]
    else:
        return str

def gen_wikidata_dict(in_file, site_id, out_file):
    record_count = 0
    with open(in_file, 'r') as in_f, open(out_file, 'w') as out_f:
        for line in in_f:
            line = line.strip()
            if not line.startswith(head):
                continue
            records = record_pat.findall(line)
            if not records:
                continue
            for record in records:
                record = field_pat.findall(record)
                [_, qid, sid, page] = record[:4]
                qid, sid, page = int(qid), strip_quotes(sid), strip_quotes(page)
                if sid != site_id:
                    continue
                out_f.write(f'{qid}\t{page}\n')
                record_count += 1
                if record_count % 10000 == 0:
                    print(f'Processed {record_count} records', file=sys.stderr)

def main(args):
    script = sys.argv[0]
    args = sys.argv[1:]
    if len(args) != 3:
        print(f'Usage: {script} in_file site_id out_file', file=sys.stderr)
        sys.exit(1)
    [in_file, site_id, out_file] = args
    gen_wikidata_dict(in_file, site_id, out_file)

if __name__ == '__main__':
    main(sys.argv)
