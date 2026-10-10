#!/usr/bin/env python3
"""Runtime boundaries and mechanism records; host dispatch is mocked. MIT."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
SCRIPTS = Path(__file__).resolve().parents[1]/'plugins/medical-illustration/skills/medical-illustration/scripts'
sys.path.insert(0, str(SCRIPTS))
import illustrator_run as runner
from illustrator_preflight import inspect_script
from check_mechanism_graph import check

class RuntimeTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.script = self.base/'中文 job.jsx'
        self.script.write_text('var s = IllustratorSession.current;\n', encoding='utf-8')
        self.run = self.base/'运行记录'
        self.lock = self.base/'shared.lock'
    def invoke(self, extra=(), platform='darwin', dispatch=None):
        args = ['runtime', str(self.script), '--run-dir', str(self.run), *extra]
        with patch.object(runner, 'LOCK', self.lock), patch.object(sys, 'argv', args), patch.object(sys, 'platform', platform), patch.object(runner.subprocess, 'run', side_effect=dispatch) as call, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            result = runner.main()
        return result, call
    def completed(self, status):
        def dispatch(argv, **kwargs):
            self.assertEqual(argv[0], '/usr/bin/osascript')
            self.assertTrue((self.run/'wrapper.jsx').is_file())
            (self.run/'completion.txt').write_text(status, encoding='utf-8')
            return subprocess.CompletedProcess(argv, 0, 'host returned', '')
        return dispatch
    def test_check_only_without_host_or_side_effects(self):
        code, call = self.invoke(['--check-only'], platform='win32')
        self.assertEqual(code, 0);call.assert_not_called()
        self.assertFalse(self.lock.exists());self.assertFalse(self.run.exists())
    def test_unsupported_platform_does_not_dispatch(self):
        with self.assertRaises(SystemExit) as error:self.invoke(platform='linux')
        self.assertEqual(error.exception.code,2)
        self.assertFalse(self.lock.exists());self.assertFalse(self.run.exists())
    def test_managed_lettering_passes_preflight(self):
        self.script.write_text('$.evalFile(File('+json.dumps(str(SCRIPTS/'illustrator-lettering.jsx'))+'));', encoding='utf-8')
        result=inspect_script(self.script)
        self.assertFalse(result['errors']);self.assertEqual(len(result['files']),2)
    def test_nested_unsafe_code_rejected(self):
        child=self.base/'中文 dependency.jsx'
        child.write_text('app.documents.add();',encoding='utf-8')
        self.script.write_text('$.evalFile(File('+json.dumps(str(child))+'));',encoding='utf-8')
        code,call=self.invoke()
        self.assertEqual(code,65);call.assert_not_called();self.assertFalse(self.lock.exists())
    def test_comments_and_strings_do_not_create_dependencies(self):
        literal = '$.evalFile(File(' + json.dumps(str(self.base/'missing.jsx')) + '));'
        for source in ('// ' + literal, '/* ' + literal + ' */',
                       "var note = '" + literal + "';",
                       'var note = ' + json.dumps('Example: "quoted" ' + literal) + ';'):
            with self.subTest(source=source):
                self.script.write_text(source + '\nvar s = IllustratorSession.current;\n', encoding='utf-8')
                audit = inspect_script(self.script)
                self.assertEqual(audit['errors'], [])
                self.assertEqual(audit['warnings'], [])
                self.assertEqual(len(audit['files']), 1)
                code, call = self.invoke(['--check-only'], platform='win32')
                self.assertEqual(code, 0);call.assert_not_called()
                self.assertFalse(self.lock.exists());self.assertFalse(self.run.exists())
    def test_real_dependency_with_inline_comments_is_still_inspected(self):
        child = self.base/'real dependency.jsx'
        child.write_text('app.documents.add();', encoding='utf-8')
        self.script.write_text(
            '// $.evalFile(File("/unused/example.jsx"));\n'
            '$.evalFile(/* load */ File(/* path */ ' + json.dumps(str(child)) +
            ' /* end path */) /* end load */);\n', encoding='utf-8')
        audit = inspect_script(self.script)
        self.assertEqual(len(audit['files']), 2)
        self.assertEqual(audit['errors'], [{'path': str(child.resolve()), 'line': 1,
            'code': 'unmanaged-create', 'message': 'Use session.create(...).'}])
        self.assertEqual(audit['warnings'], [])
    def test_inactive_literal_cannot_hide_computed_dependency_warning(self):
        child = self.base/'unused.jsx'
        child.write_text('var unused = true;', encoding='utf-8')
        literal = '$.evalFile(File(' + json.dumps(str(child)) + '));'
        for inactive in ('// ' + literal, "var note = '" + literal + "';"):
            with self.subTest(inactive=inactive):
                self.script.write_text(inactive + '\n$.evalFile(dynamicPath);', encoding='utf-8')
                audit = inspect_script(self.script)
                self.assertEqual(audit['errors'], [])
                self.assertEqual(len(audit['files']), 1)
                self.assertEqual(len(audit['warnings']), 1)
                self.assertIn('Computed evalFile dependency', audit['warnings'][0]['message'])
    def test_real_missing_and_relative_dependencies_remain_errors(self):
        for path, error in ((str(self.base/'missing.jsx'), 'missing-dependency'),
                            ('relative.jsx', 'relative-code-path')):
            with self.subTest(path=path):
                self.script.write_text('$.evalFile(File(' + json.dumps(path) + '));', encoding='utf-8')
                self.assertEqual([e['code'] for e in inspect_script(self.script)['errors']], [error])
                code, call = self.invoke()
                self.assertEqual(code, 65);call.assert_not_called()
                self.assertFalse(self.lock.exists());self.assertFalse(self.run.exists())
    def test_wrapper_preserves_placeholder_words_and_escaped_paths(self):
        for word in ('LIBRARY', 'RECOVERY', 'SCRIPT', 'COMPLETION', 'PROGRESS',
                     'LIBRARY-RECOVERY-SCRIPT-COMPLETION-PROGRESS'):
            with self.subTest(word=word):
                folder = self.base/(word + " 中文 ' {paths} $-é")
                folder.mkdir()
                library = folder/'illustrator_session.jsx'
                library.write_text('// mocked session library', encoding='utf-8')
                self.script = folder/'job.jsx'
                self.script.write_text('var s = IllustratorSession.current;', encoding='utf-8')
                self.run = folder/'run'
                self.lock = folder/'isolated.lock'
                def dispatch(argv, **kwargs):
                    wrapper = (self.run/'wrapper.jsx').read_text(encoding='utf-8')
                    for path in (library, self.script, self.run/'recovery',
                                 self.run/'progress.txt', self.run/'completion.txt'):
                        self.assertIn(json.dumps(str(path.resolve()), ensure_ascii=True), wrapper)
                    return self.completed('OK\n')(argv, **kwargs)
                with patch.object(runner, '__file__', str(folder/'illustrator_run.py')):
                    code, call = self.invoke(dispatch=dispatch)
                self.assertEqual(code, 0);call.assert_called_once()
                self.assertFalse(self.lock.exists())
    def test_occupied_lock_is_preserved(self):
        self.lock.mkdir();(self.lock/'owner.json').write_text('other owner')
        code,call=self.invoke()
        self.assertEqual(code,75);call.assert_not_called()
        self.assertEqual((self.lock/'owner.json').read_text(encoding='utf-8'),'other owner')
    def test_success_releases_lock(self):
        code,_=self.invoke(dispatch=self.completed('OK\n'))
        self.assertEqual(code,0);self.assertFalse(self.lock.exists())
    def test_confirmed_script_error_releases_lock(self):
        code,_=self.invoke(dispatch=self.completed('ERROR\nscript failed'))
        self.assertEqual(code,1);self.assertFalse(self.lock.exists())
    def test_timeout_retains_uncertain_lock(self):
        code,_=self.invoke(dispatch=subprocess.TimeoutExpired('host',1))
        self.assertEqual(code,2)
        self.assertEqual(json.loads((self.lock/'owner.json').read_text(encoding='utf-8'))['state'],'uncertain')
    def test_completion_without_host_success_retains_lock(self):
        def dispatch(argv,**kwargs):
            (self.run/'completion.txt').write_text('OK\n')
            return subprocess.CompletedProcess(argv,1,'','unconfirmed host error')
        code,_=self.invoke(dispatch=dispatch)
        self.assertEqual(code,2);self.assertTrue(self.lock.exists())
    def test_existing_run_directory_not_overwritten(self):
        self.run.mkdir();marker=self.run/'keep';marker.write_text('keep')
        with self.assertRaises(FileExistsError):self.invoke()
        self.assertEqual(marker.read_text(),'keep');self.assertFalse(self.lock.exists())

class MechanismTests(unittest.TestCase):
    def setUp(self):
        self.data={'nodes':[{'id':'a','label':'A','compartment':'test'},{'id':'b','label':'B','compartment':'test'}],
                   'sources':[{'id':'s','citation':'Synthetic test fixture, not literature','checked_scope':'Schema only'}],
                   'edges':[{'id':'e','source':'a','target':'b','source_ids':['s'],'relation':'activation','evidence_status':'observed','directness':'unspecified','line_style':'solid','arrowhead':'arrow'}]}
    def test_relations(self):
        for relation,head in [('activation','arrow'),('inhibition','bar'),('association','none'),('transport','arrow'),('process','arrow'),('localization','none')]:
            with self.subTest(relation=relation):
                self.data['edges'][0].update(relation=relation,arrowhead=head)
                self.assertEqual(check(self.data),[])
    def test_missing_reference_and_node_rejected(self):
        for field,value in [('source_ids',[]),('source_ids',['missing']),('target','missing')]:
            with self.subTest(field=field,value=value):
                data=copy.deepcopy(self.data);data['edges'][0][field]=value
                self.assertTrue(check(data))
    def test_hypothesis_needs_dashed_line(self):
        self.data['edges'][0]['evidence_status']='hypothesis'
        self.assertTrue(check(self.data))
        self.data['edges'][0]['line_style']='dashed'
        self.assertEqual(check(self.data),[])
    def test_duplicate_id_rejected(self):
        self.data['nodes'].append(self.data['nodes'][0].copy())
        self.assertTrue(check(self.data))

class CropTests(unittest.TestCase):
    def test_pixel_exact_crop_and_input_protection(self):
        from PIL import Image
        from illustrator_assets import crop_asset
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);source=base/'source.png'
            im=Image.new('RGB',(100,100))
            im.putdata([(x,y,(x+y)%256) for y in range(100) for x in range(100)])
            im.save(source,icc_profile=b'audit-test-profile')
            before=source.read_bytes()
            row=crop_asset(source,[100,100],[20,30,40,25],base/'crops')
            with Image.open(row['path']) as crop:
                self.assertEqual(crop.tobytes(),im.crop(row['pixel_box']).tobytes())
                self.assertEqual(crop.info['icc_profile'],b'audit-test-profile')
            self.assertEqual(source.read_bytes(),before)
            self.assertEqual(crop_asset(source,[100,100],[20,30,40,25],base/'crops')['crop_sha256'],row['crop_sha256'])
            Path(row['path']).write_bytes(b'user file')
            with self.assertRaises(OSError):crop_asset(source,[100,100],[20,30,40,25],base/'crops')
            self.assertEqual(Path(row['path']).read_bytes(),b'user file')

if __name__=='__main__':unittest.main(verbosity=2)
