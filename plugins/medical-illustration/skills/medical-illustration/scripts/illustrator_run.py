#!/usr/bin/env python3
# MIT License; see ../LICENSE-CODE.
"""Serialize local Illustrator jobs. Never quits Illustrator or clears uncertain locks."""
from __future__ import annotations
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
import subprocess
import time
import uuid
from illustrator_preflight import inspect_script

# macOS uses the same lock as other installed copies and the local host adapter.
LOCK = Path('/private/tmp' if sys.platform == 'darwin' else tempfile.gettempdir()) / f'codex-illustrator-{getattr(os, "getuid", lambda: 0)()}.lock'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('script', type=Path, nargs='?')
    p.add_argument('--run-dir', type=Path, help='New, permanent run directory for wrapper, logs and recovery')
    p.add_argument('--timeout', type=int, default=600)
    p.add_argument('--status', action='store_true')
    p.add_argument('--check-only', action='store_true', help='Inspect JSX and literal dependencies; do not call Illustrator')
    a = p.parse_args()
    if sys.platform != 'darwin' and not a.check_only:
        p.error('Automatic dispatch/status requires macOS and Adobe Illustrator; --check-only works without the host. Use the documented SVG/vector workflow elsewhere.')
    if a.status:
        print((LOCK / 'owner.json').read_text(encoding='utf-8') if (LOCK / 'owner.json').exists() else ('LOCKED (owner pending)' if LOCK.exists() else 'IDLE'))
        return 0
    if not a.script or (not a.run_dir and not a.check_only) or a.timeout < 1:
        p.error('script, --run-dir and a positive timeout are required')
    try:
        script = a.script.expanduser().resolve(strict=True)
        audit = inspect_script(script)
    except (OSError, ValueError) as exc:
        p.error(str(exc))
    if a.check_only or audit['errors']:
        print(json.dumps(audit, ensure_ascii=False, indent=2))
        return 65 if audit['errors'] else 0
    library = Path(__file__).resolve().with_name('illustrator_session.jsx')
    if not library.is_file(): p.error('Missing sibling illustrator_session.jsx')
    run_dir = a.run_dir.expanduser().resolve()
    # One lock path for every project. A timeout may leave an AppleEvent executing.
    try: LOCK.mkdir(mode=0o700)
    except FileExistsError:
        print(f'BUSY_OR_UNCERTAIN: inspect {LOCK}; do not retry or remove a live lock.')
        return 75
    token = uuid.uuid4().hex
    owner = {'token':token, 'pid':os.getpid(), 'script':str(script), 'run_dir':str(run_dir), 'started':time.time(), 'state':'preparing'}
    dispatched = False
    settled = False
    try:
        (LOCK / 'owner.json').write_text(json.dumps(owner, ensure_ascii=False, indent=2), encoding='utf-8')
        run_dir.mkdir(parents=True, exist_ok=False)
        (run_dir / 'recovery').mkdir()
        (run_dir / 'preflight.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
        complete = run_dir / 'completion.txt'
        progress = run_dir / 'progress.txt'
        wrapper = run_dir / 'wrapper.jsx'
        q = lambda s: json.dumps(str(s), ensure_ascii=True)
        wrapper.write_text('''#target illustrator
(function () {
    var state = 'OK', message = '';
    function progress(note) { var p=File(PROGRESS); if(p.open('w')) {p.write(note);p.close();} }
    try {
        progress('loading session');
        $.evalFile(File(LIBRARY));
        IllustratorSession.run({recoveryDir: RECOVERY, progressPath: PROGRESS}, function (session) {
            progress('executing script');
            $.evalFile(File(SCRIPT));
            progress('script returned; cleaning up');
        });
    } catch (e) { state = 'ERROR'; message = String(e) + ' line ' + e.line; }
    finally {
        var f = File(COMPLETION); f.encoding = 'UTF-8';
        if (!f.open('w')) throw Error('Cannot write completion record.');
        f.write(state + '\\n' + message); f.close();
    }
    return state + '\\n' + message;
}());
'''.replace('LIBRARY', q(library)).replace('RECOVERY', q(run_dir / 'recovery')).replace('SCRIPT', q(script)).replace('COMPLETION', q(complete)).replace('PROGRESS', q(progress)), encoding='utf-8')
        apple = run_dir / 'dispatch.applescript'
        apple.write_text('''on run argv
    with timeout of %d seconds
        tell application id "com.adobe.illustrator"
            do javascript ((POSIX file (item 1 of argv)) as alias) show debugger never
        end tell
    end timeout
end run
''' % a.timeout, encoding='utf-8')
        owner['state'] = 'dispatched'
        (LOCK / 'owner.json').write_text(json.dumps(owner, ensure_ascii=False, indent=2), encoding='utf-8')
        dispatched = True
        result = subprocess.run(['/usr/bin/osascript', str(apple), str(wrapper)], capture_output=True, text=True, timeout=a.timeout + 10)
        (run_dir / 'dispatch.stdout.txt').write_text(result.stdout, encoding='utf-8')
        (run_dir / 'dispatch.stderr.txt').write_text(result.stderr, encoding='utf-8')
        # Completion means the host reached its finally block, not just a file appeared.
        if result.returncode == 0 and complete.is_file():
            status = complete.read_text(encoding='utf-8')
            settled = status.startswith(('OK\n', 'ERROR\n'))
            print(status)
            return 0 if status.startswith('OK\n') else 1
        print(f'UNCONFIRMED: see {run_dir}; lock retained at {LOCK}')
        return 2
    except subprocess.TimeoutExpired:
        print(f'TIMEOUT: Illustrator may still be executing. Lock retained: {LOCK}')
        return 2
    finally:
        if settled or not dispatched:
            (LOCK / 'owner.json').unlink(missing_ok=True)
            LOCK.rmdir()
        else:
            owner['state'] = 'uncertain'
            (LOCK / 'owner.json').write_text(json.dumps(owner, ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    raise SystemExit(main())
