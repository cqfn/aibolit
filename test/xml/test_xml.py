# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

def test_xml_report_with_nested_results(self):
    """Test that XML report handles nested results structure correctly"""
    mock_input_with_nested = [
        {
            'filename': 'test.java',
            'results': [
                [{'pattern_code': 'P1', 'importance': 5}],
                [{'pattern_code': 'P2', 'importance': 3}]
            ]
        }
    ]
    
    mock_cmd = self.__create_mock_cmd()
    result = create_xml_tree(mock_input_with_nested, cmd=mock_cmd, exit_code=0)
    self.assertIn('P1', result)
    self.assertIn('P2', result)

def test_xml_report_with_flat_results(self):
    """Test that XML report still works with flat results structure"""
    mock_input_flat = [
        {
            'filename': 'test.java', 
            'results': [
                {'pattern_code': 'P1', 'importance': 5},
                {'pattern_code': 'P2', 'importance': 3}
            ]
        }
    ]
    mock_cmd = self.__create_mock_cmd()
    result = create_xml_tree(mock_input_flat, cmd=mock_cmd, exit_code=0)
    self.assertIn('P1', result)
    self.assertIn('P2', result)
