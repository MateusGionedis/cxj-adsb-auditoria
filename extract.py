#!/usr/bin/env python3
"""Consume a TAR stream and write only files matching requested ICAO24 identifiers."""
import argparse
import csv
import json
import os
import re
import sys
import tarfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--date', required=True)
parser.add_argument('--hexes', required=True, help='Comma separated ICAO24 hex addresses')
parser.add_argument('--output', default='results')
args = parser.parse_args()
targets = {x.strip().lower() for x in args.hexes.split(',') if re.fullmatch(r'[0-9a-fA-F]{6}', x.strip())}
if not targets:
    parser.error('No valid six-digit ICAO24 values')
out = Path(args.output) / args.date
out.mkdir(parents=True, exist_ok=True)
records = []
with tarfile.open(fileobj=sys.stdin.buffer, mode='r|') as tar:
    for item in tar:
        if not item.isfile():
            continue
        base = Path(item.name).name.lower()
        matched = [h for h in targets if h in base and (base.endswith('.json') or base.endswith('.json.gz'))]
        if not matched:
            continue
        f = tar.extractfile(item)
        if f is None:
            continue
        for h in matched:
            dest = out / (h + '__' + base)
            with dest.open('wb') as sink:
                while True:
                    chunk = f.read(1024 * 1024)
                    if not chunk:
                        break
                    sink.write(chunk)
            records.append({'date': args.date, 'icao24': h, 'archive_member': item.name, 'output': str(dest), 'bytes': dest.stat().st_size})
            print('EXTRACTED', item.name, '->', dest, flush=True)
with (out / 'manifest.json').open('w') as f:
    json.dump({'date': args.date, 'targets': sorted(targets), 'found': records, 'note': 'Missing records do not prove the aircraft did not fly.'}, f, indent=2)
print('Files extracted:', len(records))
