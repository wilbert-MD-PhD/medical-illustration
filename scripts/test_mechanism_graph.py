#!/usr/bin/env python3
"""Mechanism graph input validation regression tests. MIT; see ../LICENSE-CODE."""
import importlib.util
import unittest
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'plugins/medical-illustration/skills/medical-illustration/scripts/check_mechanism_graph.py'
spec = importlib.util.spec_from_file_location('graph', path)
graph = importlib.util.module_from_spec(spec)
spec.loader.exec_module(graph)


class GraphTests(unittest.TestCase):
    def test_invalid_relation_type_reports_all_edges(self):
        for invalid in ([], {}, None, 1):
            with self.subTest(invalid=invalid):
                data = {'nodes': [], 'sources': [], 'edges': [
                    {'id': 'first', 'source': 'missing', 'target': 'missing', 'source_ids': [], 'relation': invalid},
                    {'id': 'second', 'source': 'missing', 'target': 'missing', 'source_ids': [], 'relation': 'activation'}]}
                errors = graph.check(data)
                self.assertIn('first: invalid relation', errors)
                self.assertIn('first: unknown source', errors)
                self.assertIn('second: unknown source', errors)

    def test_valid_graph_passes(self):
        data = {'nodes': [{'id':'a', 'label':'A', 'compartment':'cell'}, {'id':'b', 'label':'B', 'compartment':'cell'}],
                'sources': [{'id':'s', 'citation':'reference', 'checked_scope':'example'}],
                'edges': [{'id':'e', 'source':'a', 'target':'b', 'relation':'activation', 'evidence_status':'observed',
                           'directness':'unspecified', 'source_ids':['s'], 'line_style':'solid', 'arrowhead':'arrow'}]}
        self.assertEqual(graph.check(data), [])


if __name__ == '__main__':
    unittest.main()
