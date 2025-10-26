#!/usr/bin/env python3
"""
Unit tests for package_skill.py
"""

import unittest
import tempfile
import shutil
import zipfile
import json
from pathlib import Path
from package_skill import SkillPackager


class TestSkillPackager(unittest.TestCase):
    
    def setUp(self):
        """Create temporary skill folder for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.skill_path = Path(self.test_dir) / "test-skill"
        self.skill_path.mkdir()
        
        # Create minimal valid SKILL.md
        skill_md_content = """---
name: test-skill
description: Test skill for unit testing the packaging system to ensure all components work correctly.
license: MIT
---

# Test Skill

## Overview

Test skill overview goes here.

## When to Use

Use for testing the packaging system.

## How to Use

Run tests to validate functionality.
"""
        (self.skill_path / "SKILL.md").write_text(skill_md_content, encoding='utf-8')
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_basic_packaging(self):
        """Should create valid zip file"""
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        self.assertIsNotNone(zip_path)
        self.assertTrue(Path(zip_path).exists())
        
        # Verify zip contains SKILL.md
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            self.assertIn("SKILL.md", names)
    
    def test_excludes_testing_guide(self):
        """TESTING_GUIDE folder should not be in package"""
        # Create TESTING_GUIDE folder
        testing_guide_dir = self.skill_path / "TESTING_GUIDE"
        testing_guide_dir.mkdir()
        (testing_guide_dir / "test.md").write_text("Test data")
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Verify TESTING_GUIDE is not in zip
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            testing_guide_files = [n for n in names if 'TESTING_GUIDE' in n]
            self.assertEqual(len(testing_guide_files), 0)
    
    def test_includes_scripts_folder(self):
        """scripts/ folder should be included with structure"""
        # Create scripts folder
        scripts_dir = self.skill_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "test_script.py").write_text("print('test')")
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Verify scripts are in zip
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            self.assertIn("scripts/test_script.py", names)
    
    def test_manifest_generated(self):
        """manifest.json should be included"""
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Verify manifest.json is in zip
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            self.assertIn("manifest.json", names)
            
            # Read and parse manifest
            manifest_content = zf.read("manifest.json")
            manifest = json.loads(manifest_content)
            
            # Check manifest structure
            self.assertIn("name", manifest)
            self.assertIn("version", manifest)
            self.assertIn("created", manifest)
            self.assertIn("files", manifest)
            self.assertEqual(manifest["name"], "test-skill")
    
    def test_excludes_zip_files(self):
        """Existing .zip files should not be included"""
        # Create a dummy zip file
        (self.skill_path / "old.zip").write_text("dummy")
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Verify old.zip is not in package
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            zip_files = [n for n in names if n.endswith('.zip')]
            self.assertEqual(len(zip_files), 0)
    
    def test_excludes_pycache(self):
        """__pycache__ should not be included"""
        # Create __pycache__ folder
        scripts_dir = self.skill_path / "scripts"
        scripts_dir.mkdir()
        pycache_dir = scripts_dir / "__pycache__"
        pycache_dir.mkdir()
        (pycache_dir / "test.pyc").write_text("compiled")
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Verify __pycache__ is not in zip
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            pycache_files = [n for n in names if '__pycache__' in n or n.endswith('.pyc')]
            self.assertEqual(len(pycache_files), 0)
    
    def test_includes_references_folder(self):
        """references/ folder should be included"""
        # Create references folder
        refs_dir = self.skill_path / "references"
        refs_dir.mkdir()
        (refs_dir / "schema.md").write_text("# Schema documentation")
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Verify references are in zip
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            self.assertIn("references/schema.md", names)
    
    def test_includes_assets_folder(self):
        """assets/ folder should be included"""
        # Create assets folder
        assets_dir = self.skill_path / "assets"
        assets_dir.mkdir()
        (assets_dir / "template.txt").write_text("Template content")
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Verify assets are in zip
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            self.assertIn("assets/template.txt", names)
    
    def test_includes_license_file(self):
        """LICENSE.txt should be included if present"""
        (self.skill_path / "LICENSE.txt").write_text("MIT License...")
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Verify LICENSE.txt is in zip
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            self.assertIn("LICENSE.txt", names)
    
    def test_checksum_calculation(self):
        """Should calculate checksums for files"""
        packager = SkillPackager(str(self.skill_path), validate=False)
        
        # Test checksum calculation
        checksum = packager._calculate_checksum(self.skill_path / "SKILL.md")
        
        # Should be a hex string
        self.assertIsInstance(checksum, str)
        self.assertEqual(len(checksum), 64)  # SHA256 is 64 hex characters
    
    def test_format_size(self):
        """Should format file sizes correctly"""
        packager = SkillPackager(str(self.skill_path), validate=False)
        
        self.assertIn("B", packager._format_size(100))
        self.assertIn("KB", packager._format_size(2048))
        self.assertIn("MB", packager._format_size(2 * 1024 * 1024))
    
    def test_package_without_validation(self):
        """Should package without validation when validate=False"""
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        self.assertIsNotNone(zip_path)
        self.assertTrue(Path(zip_path).exists())
    
    def test_missing_skill_md_fails(self):
        """Should fail if SKILL.md is missing"""
        # Remove SKILL.md
        (self.skill_path / "SKILL.md").unlink()
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        
        with self.assertRaises(ValueError):
            packager.package()
    
    def test_custom_output_path(self):
        """Should create package at custom path"""
        output_path = Path(self.test_dir) / "custom" / "my-skill.zip"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package(str(output_path))
        
        self.assertEqual(str(output_path), zip_path)
        self.assertTrue(output_path.exists())
    
    def test_nested_directory_structure(self):
        """Should preserve nested directory structure"""
        # Create nested structure
        scripts_dir = self.skill_path / "scripts" / "utils"
        scripts_dir.mkdir(parents=True)
        (scripts_dir / "helper.py").write_text("def help(): pass")
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Verify nested structure is preserved
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            self.assertIn("scripts/utils/helper.py", names)
    
    def test_excludes_hidden_files(self):
        """Should exclude hidden files"""
        (self.skill_path / ".gitignore").write_text("*.pyc")
        (self.skill_path / ".hidden").write_text("hidden content")
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Verify hidden files are not in zip
        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            hidden_files = [n for n in names if n.startswith('.')]
            self.assertEqual(len(hidden_files), 0)
    
    def test_manifest_includes_file_metadata(self):
        """Manifest should include file metadata"""
        # Create some files
        scripts_dir = self.skill_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "script.py").write_text("print('hello')")
        
        packager = SkillPackager(str(self.skill_path), validate=False)
        zip_path = packager.package()
        
        # Read manifest
        with zipfile.ZipFile(zip_path, 'r') as zf:
            manifest_content = zf.read("manifest.json")
            manifest = json.loads(manifest_content)
            
            # Check SKILL.md metadata
            self.assertIn("SKILL.md", manifest["files"])
            self.assertIn("checksum", manifest["files"]["SKILL.md"])
            self.assertIn("size", manifest["files"]["SKILL.md"])
            
            # Check scripts metadata
            if "scripts" in manifest["files"]:
                self.assertIsInstance(manifest["files"]["scripts"], dict)


class TestPackageMultipleSkills(unittest.TestCase):
    """Test batch packaging functionality"""
    
    def setUp(self):
        """Create temporary directory with multiple skills"""
        self.test_dir = tempfile.mkdtemp()
        
        # Create two skills
        for i in range(1, 3):
            skill_path = Path(self.test_dir) / f"skill-{i}"
            skill_path.mkdir()
            
            skill_md = f"""---
name: skill-{i}
description: Test skill {i} for batch packaging tests.
license: MIT
---

# Skill {i}

Content for skill {i}.
"""
            (skill_path / "SKILL.md").write_text(skill_md)
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_dir)
    
    def test_batch_packaging(self):
        """Should package multiple skills"""
        from package_skill import package_multiple_skills
        
        packaged = package_multiple_skills(self.test_dir)
        
        # Should have packaged 2 skills
        self.assertEqual(len(packaged), 2)
        
        # All should exist
        for zip_path in packaged:
            self.assertTrue(Path(zip_path).exists())


if __name__ == '__main__':
    unittest.main()

