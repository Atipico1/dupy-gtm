"""Local run folders and immutable stage records; never executes a workflow/API."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STAGES = ('01-performance', '02-references', '03-planning', '04-plan-review',
          '05-production', '06-content-review', '07-publishing', '08-improvement', 'maintenance')
STATUSES = ('completed', 'needs_revision', 'blocked', 'failed', 'unknown', 'cancelled')

def stamp():
    return datetime.now(ZoneInfo('Asia/Seoul'))

def write_new(path, value):
    """Publish a complete JSON file atomically without replacing existing records."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name('.' + uuid.uuid4().hex + '.tmp')
    try:
        temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
        os.link(temp, path)
    finally:
        temp.unlink(missing_ok=True)

def start(root, request, stages, scope, source_runs):
    selected = list(dict.fromkeys(stages))
    if not selected or set(selected) - set(STAGES):
        raise ValueError('Unknown or empty stage selection')
    root.mkdir(parents=True, exist_ok=True)
    now = stamp()
    run_id = now.strftime('%Y%m%dT%H%M%S%f') + '+0900-' + uuid.uuid4().hex[:8]
    run = root / run_id
    run.mkdir(exist_ok=False)
    snapshots = []
    for relative in ('workflow/config.json', '.agents/skills/dupy-gtm-loop/SKILL.md'):
        path = ROOT / relative
        content = path.read_text()
        snapshots.append({'path': relative, 'sha256': hashlib.sha256(content.encode()).hexdigest(),
                          'content': content})
    manifest = {'schema_version': 1, 'run_id': run_id, 'started_at': now.isoformat(),
                'timezone': 'Asia/Seoul', 'request': request, 'selected_stages': selected,
                'scope': scope, 'source_runs': source_runs, 'snapshots': snapshots,
                'activation': None, 'execution_note': 'Record creation is not generation/publishing authorization.'}
    write_new(run / 'run.json', manifest)
    (run / 'artifacts').mkdir()
    return run

def record(run, stage, data):
    manifest = json.loads((run / 'run.json').read_text())
    if stage not in manifest['selected_stages']:
        raise ValueError('Stage is outside the requested run scope')
    for key in ('inputs', 'observations', 'revisions', 'outputs', 'checks'):
        if not isinstance(data.get(key), list):
            raise ValueError(f'{key} must be an array (empty allowed)')
    for key in ('decision_summary', 'conclusion'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f'{key} must be a nonempty summary')
    if data.get('status') not in STATUSES:
        raise ValueError('Invalid status')
    if data['status'] in ('blocked', 'failed', 'unknown') and not data.get('error'):
        raise ValueError('Non-success must state the blocking/error condition')
    reserved = {'schema_version', 'run_id', 'stage', 'record_id', 'recorded_at'}
    if reserved.intersection(data):
        raise ValueError('Record identity is managed by the recorder')
    now = stamp()
    rid = now.strftime('%H%M%S%f') + '-' + uuid.uuid4().hex[:8]
    path = run / 'stages' / stage / (rid + '.json')
    write_new(path, {'schema_version': 1, 'run_id': manifest['run_id'], 'stage': stage,
                     'record_id': rid, 'recorded_at': now.isoformat(), **data})
    return path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    p = subs.add_parser('start')
    p.add_argument('--request', required=True)
    p.add_argument('--stages', nargs='+', choices=STAGES, required=True)
    p.add_argument('--scope', required=True, help='e.g. analysis only, audio only, or full workflow')
    p.add_argument('--source-run', action='append', default=[])
    p.add_argument('--root', type=Path, default=ROOT / 'runs')
    p = subs.add_parser('record')
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--stage', choices=STAGES, required=True)
    p.add_argument('--input', type=Path, required=True, help='Stage JSON, without secrets or hidden reasoning')
    args = parser.parse_args()
    if args.command == 'start':
        print(start(args.root.resolve(), args.request, args.stages, args.scope, args.source_run))
    else:
        print(record(args.run.resolve(), args.stage, json.loads(args.input.read_text())))

if __name__ == '__main__':
    main()
