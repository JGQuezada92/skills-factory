#!/usr/bin/env python3
"""
Unit tests for generate_skills.py
"""

import unittest
import tempfile
import yaml
from pathlib import Path
import sys
import os

# Add parent directory to path to import generate_skills
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_skills import SkillsGenerator, ConfigValidator


class TestConfigValidator(unittest.TestCase):
    
    def test_valid_config_passes(self):
        """Valid configuration should pass"""
        config = {
            'business': {
                'description': 'Test business description with enough words to pass validation check',
                'industry': 'Test Industry',
                'team_size': '10-50',
                'primary_workflows': ['Workflow 1', 'Workflow 2']
            },
            'skills': {
                'count': 3,
                'overlap_strategy': 'overlapping',
                'use_cases': [
                    {
                        'name': 'Test Skill',
                        'description': 'Test description with enough words to pass',
                        'requires_python': False,
                        'sample_data_type': 'csv'
                    }
                ]
            },
            'output': {
                'output_directory': './generated_skills'
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_missing_required_section_fails(self):
        """Missing required section should fail"""
        config = {
            'skills': {
                'count': 3
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Should mention missing 'business' section
        error_messages = ' '.join(errors)
        self.assertIn('business', error_messages.lower())
    
    def test_missing_required_key_fails(self):
        """Missing required key should fail"""
        config = {
            'business': {
                'industry': 'Test'
                # Missing 'description'
            },
            'skills': {
                'count': 3,
                'overlap_strategy': 'overlapping',
                'use_cases': []
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Should mention missing 'description' key
        error_messages = ' '.join(errors)
        self.assertIn('description', error_messages.lower())
    
    def test_invalid_overlap_strategy_fails(self):
        """Invalid overlap_strategy should fail"""
        config = {
            'business': {
                'description': 'Test description',
                'industry': 'Test'
            },
            'skills': {
                'count': 3,
                'overlap_strategy': 'invalid_strategy',  # Invalid
                'use_cases': []
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        self.assertFalse(is_valid)
        
        # Should have error about invalid strategy
        error_messages = ' '.join(errors)
        self.assertIn('overlap_strategy', error_messages.lower())
    
    def test_count_out_of_range_fails(self):
        """Count outside 1-20 should fail"""
        config = {
            'business': {
                'description': 'Test',
                'industry': 'Test'
            },
            'skills': {
                'count': 50,  # Too high
                'overlap_strategy': 'overlapping',
                'use_cases': []
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        self.assertFalse(is_valid)
        
        # Should have error about count
        error_messages = ' '.join(errors)
        self.assertIn('count', error_messages.lower())
    
    def test_invalid_sample_data_type_fails(self):
        """Invalid sample_data_type should fail"""
        config = {
            'business': {
                'description': 'Test description',
                'industry': 'Test'
            },
            'skills': {
                'count': 3,
                'overlap_strategy': 'overlapping',
                'use_cases': [
                    {
                        'name': 'Test',
                        'description': 'Test',
                        'sample_data_type': 'invalid_type'  # Invalid
                    }
                ]
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        self.assertFalse(is_valid)
        
        # Should have error about sample_data_type
        error_messages = ' '.join(errors)
        self.assertIn('sample_data_type', error_messages.lower())
    
    def test_duplicate_use_case_names_fails(self):
        """Duplicate use case names should fail"""
        config = {
            'business': {
                'description': 'Test description with enough words here',
                'industry': 'Test'
            },
            'skills': {
                'count': 2,
                'overlap_strategy': 'overlapping',
                'use_cases': [
                    {'name': 'Duplicate', 'description': 'First'},
                    {'name': 'Duplicate', 'description': 'Second'}  # Duplicate name
                ]
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        self.assertFalse(is_valid)
        
        # Should have error about duplicates
        error_messages = ' '.join(errors)
        self.assertIn('duplicate', error_messages.lower())
    
    def test_short_description_warning(self):
        """Short business description should warn"""
        config = {
            'business': {
                'description': 'Short',  # Too short
                'industry': 'Test'
            },
            'skills': {
                'count': 3,
                'overlap_strategy': 'overlapping',
                'use_cases': [
                    {'name': 'Test', 'description': 'Test description with enough content'}
                ]
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        # Should be valid but with warnings
        self.assertTrue(is_valid)
        self.assertGreater(len(warnings), 0)
        
        # Should mention short description
        warning_messages = ' '.join(warnings)
        self.assertIn('short', warning_messages.lower())
    
    def test_placeholder_detection(self):
        """Should detect placeholder text"""
        config = {
            'business': {
                'description': '[YOUR BUSINESS DESCRIPTION]',  # Placeholder
                'industry': 'Test'
            },
            'skills': {
                'count': 3,
                'overlap_strategy': 'overlapping',
                'use_cases': []
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        # Should have warning about placeholder
        self.assertGreater(len(warnings), 0)
        warning_messages = ' '.join(warnings)
        self.assertIn('placeholder', warning_messages.lower())
    
    def test_count_type_validation(self):
        """Count must be an integer"""
        config = {
            'business': {
                'description': 'Test',
                'industry': 'Test'
            },
            'skills': {
                'count': "3",  # String instead of int
                'overlap_strategy': 'overlapping',
                'use_cases': []
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        self.assertFalse(is_valid)
        
        # Should have error about type
        error_messages = ' '.join(errors)
        self.assertIn('integer', error_messages.lower())
    
    def test_use_cases_must_be_list(self):
        """use_cases must be a list"""
        config = {
            'business': {
                'description': 'Test',
                'industry': 'Test'
            },
            'skills': {
                'count': 3,
                'overlap_strategy': 'overlapping',
                'use_cases': "not a list"  # Wrong type
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        self.assertFalse(is_valid)
        
        # Should have error about list type
        error_messages = ' '.join(errors)
        self.assertIn('list', error_messages.lower())
    
    def test_use_case_missing_name(self):
        """Use case must have a name"""
        config = {
            'business': {
                'description': 'Test description',
                'industry': 'Test'
            },
            'skills': {
                'count': 3,
                'overlap_strategy': 'overlapping',
                'use_cases': [
                    {'description': 'Missing name'}  # No 'name' key
                ]
            }
        }
        validator = ConfigValidator(config)
        is_valid, errors, warnings = validator.validate()
        
        self.assertFalse(is_valid)
        
        # Should have error about missing name
        error_messages = ' '.join(errors)
        self.assertIn('name', error_messages.lower())


class TestSkillsGenerator(unittest.TestCase):
    
    def setUp(self):
        """Create temporary test directory"""
        self.test_dir = tempfile.mkdtemp()
        
        # Create a minimal valid config file
        self.config_path = Path(self.test_dir) / "test_config.yaml"
        config = {
            'business': {
                'description': 'Test business providing testing services to ensure quality',
                'industry': 'Software Testing',
                'team_size': '10-50',
                'primary_workflows': ['Testing', 'Validation']
            },
            'skills': {
                'count': 2,
                'overlap_strategy': 'overlapping',
                'use_cases': [
                    {
                        'name': 'Test Skill One',
                        'description': 'First test skill for validation purposes with detailed description',
                        'requires_python': False,
                        'sample_data_type': 'csv'
                    }
                ]
            },
            'output': {
                'output_directory': str(Path(self.test_dir) / 'output')
            }
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f)
        
        # Create a minimal template file
        self.template_path = Path(self.test_dir) / "test_template.md"
        self.template_path.write_text("""# Test Template

Business: {{BUSINESS_DESCRIPTION}}
Industry: {{INDUSTRY}}
Count: {{SKILL_COUNT}}
Strategy: {{OVERLAP_STRATEGY}}

{{USE_CASES_SECTION}}
""")
    
    def tearDown(self):
        """Clean up test directory"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_load_config(self):
        """Should load configuration file"""
        generator = SkillsGenerator(str(self.config_path))
        generator.load_config()
        
        self.assertIsNotNone(generator.config)
        self.assertIn('business', generator.config)
        self.assertIn('skills', generator.config)
    
    def test_validate_config(self):
        """Should validate configuration"""
        generator = SkillsGenerator(str(self.config_path))
        generator.load_config()
        
        # Mock input for warnings
        import io
        sys.stdin = io.StringIO('y\n')
        
        is_valid = generator.validate_config()
        
        # Restore stdin
        sys.stdin = sys.__stdin__
        
        self.assertTrue(is_valid)
    
    def test_format_list(self):
        """Should format lists correctly"""
        generator = SkillsGenerator(str(self.config_path))
        
        items = ['Item 1', 'Item 2', 'Item 3']
        formatted = generator.format_list(items)
        
        self.assertIn('- Item 1', formatted)
        self.assertIn('- Item 2', formatted)
        self.assertIn('- Item 3', formatted)
    
    def test_format_empty_list(self):
        """Should handle empty lists"""
        generator = SkillsGenerator(str(self.config_path))
        
        formatted = generator.format_list([])
        
        self.assertIn('None', formatted)
    
    def test_slugify(self):
        """Should convert text to slug format"""
        self.assertEqual(
            SkillsGenerator._slugify('My Test Skill'),
            'my-test-skill'
        )
        self.assertEqual(
            SkillsGenerator._slugify('Multiple   Spaces'),
            'multiple-spaces'
        )
        self.assertEqual(
            SkillsGenerator._slugify('Under_Score_Text'),
            'under-score-text'
        )
    
    def test_generate_use_cases_section(self):
        """Should generate use cases section"""
        generator = SkillsGenerator(str(self.config_path))
        generator.load_config()
        
        section = generator.generate_use_cases_section()
        
        self.assertIn('Test Skill One', section)
        self.assertIn('Use Case 1', section)
    
    def test_generate_overlap_guidance(self):
        """Should generate overlap guidance"""
        generator = SkillsGenerator(str(self.config_path))
        generator.load_config()
        
        guidance = generator.generate_overlap_guidance()
        
        self.assertIn('overlapping', guidance.lower())
    
    def test_populate_template(self):
        """Should populate template with values"""
        generator = SkillsGenerator(str(self.config_path))
        generator.template_path = str(self.template_path)
        generator.load_config()
        
        template = self.template_path.read_text()
        populated = generator.populate_template(template)
        
        # Should replace variables
        self.assertNotIn('{{BUSINESS_DESCRIPTION}}', populated)
        self.assertNotIn('{{INDUSTRY}}', populated)
        self.assertIn('Software Testing', populated)
        self.assertIn('2', populated)  # Count
    
    def test_missing_config_file(self):
        """Should handle missing config file"""
        generator = SkillsGenerator("nonexistent.yaml")
        
        with self.assertRaises(SystemExit):
            generator.load_config()
    
    def test_invalid_yaml(self):
        """Should handle invalid YAML"""
        invalid_yaml_path = Path(self.test_dir) / "invalid.yaml"
        invalid_yaml_path.write_text("invalid: yaml: content:")
        
        generator = SkillsGenerator(str(invalid_yaml_path))
        
        with self.assertRaises(SystemExit):
            generator.load_config()


if __name__ == '__main__':
    unittest.main()

