#!/usr/bin/env bash
set -euo pipefail
mode=${1:---dry-run}
[[ "$mode" == --dry-run || "$mode" == --apply ]] || { echo 'Usage: ./correct-transcripts.sh [--dry-run|--apply]' >&2; exit 2; }
cd "$(dirname "$0")"
python3 - "$mode" <<'PY'
from pathlib import Path
import sys,re,difflib
mode=sys.argv[1]
base=Path('.')
for stem in ('Abstraction_as_Reduction','Abstraction_Is_Just_Energy_Minimization'):
    dicts=[base/'corrections/shared.tsv',base/f'corrections/{stem}.tsv']
    rules=[]
    for d in dicts:
        if not d.exists(): continue
        for n,line in enumerate(d.read_text(encoding='utf-8').splitlines(),1):
            if not line.strip() or line.lstrip().startswith('#'): continue
            fields=line.split('\t')
            if len(fields)!=2 or not all(fields): raise ValueError(f'{d}:{n}: expected wrong<TAB>right')
            rules.append(tuple(fields))
    for suffix in ('.txt','.vtt','.srt','.tsv'):
        path=base/(stem+suffix)
        if not path.exists(): continue
        raw=path.read_bytes()
        encoding='utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8'
        original=raw.decode(encoding)
        edited=original
        for wrong,right in sorted(rules,key=lambda r:-len(r[0])):
            pattern=re.compile(r'(?<!\w)'+re.escape(wrong)+r'(?!\w)',re.I)
            edited=pattern.sub(lambda m: right,edited)
        if edited==original:
            print('UNCHANGED',path); continue
        print('CHANGED',path)
        if mode=='--dry-run':
            sys.stdout.writelines(difflib.unified_diff(original.splitlines(True),edited.splitlines(True),fromfile=str(path),tofile=str(path)+' corrected'))
        else:
            backup=path.with_name(path.name+'.bak')
            if not backup.exists(): backup.write_bytes(raw)
            path.write_bytes((b'\xef\xbb\xbf' if encoding=='utf-8-sig' else b'')+edited.encode('utf-8'))
            print('BACKUP',backup)
PY
