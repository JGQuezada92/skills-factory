#!/usr/bin/env python3
"""
Claude Skills Packager
Packages skills into .zip files ready for Claude import

Usage:
    python package_skill.py <skill_folder>
    python package_skill.py <skill_folder> --output custom.zip
    python package_skill.py --batch ./generated_skills
"""

import os
import json
import zipfile
import hashlib
import fnmatch
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Import validator
try:
    from validate_skill import SkillValidator, Severity
    HAS_VALIDATOR = True
except ImportError:
    HAS_VALIDATOR = False
    print("Warning: validate_skill module not found. Skipping validation.")


class SkillPackager:
    """Packages Claude Skills for import"""
    
    # Files and directories to exclude from package
    EXCLUDED_PATTERNS = [
        'TESTING_GUIDE',
        'TESTING_GUIDE/*',
        'TESTING_GUIDE/**/*',
        '*.zip',
        '.*',
        '.git',
        '.git/*',
        '.git/**/*',
        '.gitignore',
        '.DS_Store',
        'Thumbs.db',
        '__pycache__',
        '__pycache__/*',
        '__pycache__/**/*',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        'test_*.py',
        '*_test.py',
        'tests',
        'tests/*',
        'tests/**/*',
        '*.backup',
        '*.bak',
        '*.tmp',
        '*~',
    ]
    
    def __init__(self, skill_path: str, validate: bool = True, force: bool = False):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.should_validate = validate and HAS_VALIDATOR
        self.force = force
        self.packager_version = "1.0"
    
    def package(self, output_path: Optional[str] = None) -> str:
        """
        Package the skill into a .zip file
        Returns: Path to created .zip file
        """
        try:
            # Validate skill_path exists and is directory
            if not self.skill_path.exists():
                raise ValueError(f"Skill path does not exist: {self.skill_path}")
            
            if not self.skill_path.is_dir():
                raise ValueError(f"Skill path is not a directory: {self.skill_path}")
            
            # Check SKILL.md exists
            skill_md = self.skill_path / "SKILL.md"
            if not skill_md.exists():
                raise ValueError(f"SKILL.md not found in {self.skill_path}")
            
            # If should_validate: run SkillValidator
            if self.should_validate:
                print(f"Validating skill '{self.skill_name}'...")
                validator = SkillValidator(str(self.skill_path))
                is_valid, issues = validator.validate()
                
                errors = [i for i in issues if i.severity == Severity.ERROR]
                warnings = [i for i in issues if i.severity == Severity.WARNING]
                
                if errors:
                    if not self.force:
                        print(f"\n✗ Validation failed with {len(errors)} error(s):")
                        for i, error in enumerate(errors[:5], 1):  # Show first 5
                            print(f"  {i}. {error.message}")
                        if len(errors) > 5:
                            print(f"  ... and {len(errors) - 5} more")
                        print(f"\nCannot package skill with validation errors.")
                        print(f"Run: python validate_skill.py {self.skill_path}")
                        print(f"Or use --force to package anyway (not recommended)")
                        raise ValueError("Skill validation failed")
                    else:
                        print(f"⚠ Warning: Packaging with {len(errors)} validation error(s) (--force enabled)")
                
                if warnings and not self.force:
                    print(f"\n⚠ Validation found {len(warnings)} warning(s):")
                    for i, warning in enumerate(warnings[:3], 1):
                        print(f"  {i}. {warning.message}")
                    if len(warnings) > 3:
                        print(f"  ... and {len(warnings) - 3} more")
                    
                    response = input("\nContinue packaging? (y/n): ")
                    if response.lower() != 'y':
                        print("Packaging cancelled.")
                        return None
                
                if not errors:
                    print("✓ Validation passed")
            
            # Determine output_path
            if output_path is None:
                output_path = self.skill_path / f"{self.skill_name}.zip"
            else:
                output_path = Path(output_path)
            
            # Check if output file exists
            if output_path.exists():
                print(f"\n⚠ Output file already exists: {output_path}")
                response = input("Overwrite? (y/n): ")
                if response.lower() != 'y':
                    print("Packaging cancelled.")
                    return None
                output_path.unlink()
            
            # Create the zip file
            print(f"Packaging skill '{self.skill_name}'...")
            file_count = self._create_zip(output_path)
            
            # Get file size
            file_size = output_path.stat().st_size
            size_str = self._format_size(file_size)
            
            # Print success message
            print(f"\n{'='*70}")
            print(f"✓ SUCCESS! Skill packaged successfully")
            print(f"{'='*70}")
            print(f"\nSkill: {self.skill_name}")
            print(f"Output: {output_path}")
            print(f"Size: {size_str}")
            print(f"Files: {file_count}")
            print(f"\nReady to import into Claude!")
            print(f"{'='*70}\n")
            
            return str(output_path)
            
        except Exception as e:
            print(f"\n✗ Error packaging skill: {str(e)}")
            raise
    
    def _create_zip(self, output_path: Path) -> int:
        """
        Create the zip file with proper structure
        Returns: Number of files included
        """
        file_count = 0
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add SKILL.md at root (required)
            skill_md = self.skill_path / "SKILL.md"
            if skill_md.exists():
                zf.write(skill_md, "SKILL.md")
                file_count += 1
            
            # Add optional directories with structure
            for dir_name in ['scripts', 'references', 'assets']:
                dir_path = self.skill_path / dir_name
                if dir_path.exists() and dir_path.is_dir():
                    for file_path in dir_path.rglob('*'):
                        if file_path.is_file() and self._should_include(file_path):
                            arcname = file_path.relative_to(self.skill_path)
                            zf.write(file_path, arcname)
                            file_count += 1
            
            # Add LICENSE.txt if exists
            for license_file in ['LICENSE.txt', 'LICENSE']:
                license_path = self.skill_path / license_file
                if license_path.exists():
                    zf.write(license_path, license_file)
                    file_count += 1
                    break
            
            # Generate and add manifest.json
            manifest = self._create_manifest()
            zf.writestr("manifest.json", json.dumps(manifest, indent=2))
            file_count += 1
        
        return file_count
    
    def _should_include(self, file_path: Path) -> bool:
        """Check if file should be included in package"""
        # Get relative path from skill_path
        try:
            rel_path = file_path.relative_to(self.skill_path)
        except ValueError:
            return False
        
        # Convert to string with forward slashes
        rel_path_str = str(rel_path).replace('\\', '/')
        
        # Check against EXCLUDED_PATTERNS
        for pattern in self.EXCLUDED_PATTERNS:
            # Ensure pattern works with full path matching
            full_pattern = pattern if pattern.startswith('**/') else f'**/{pattern}'
            if fnmatch.fnmatch(rel_path_str, pattern) or fnmatch.fnmatch(rel_path_str, full_pattern):
                return False
            
            # Also check just the filename
            if fnmatch.fnmatch(file_path.name, pattern):
                return False
        
        return True
    
    def _create_manifest(self) -> dict:
        """Create manifest.json with skill metadata"""
        manifest = {
            "name": self.skill_name,
            "version": "1.0",
            "created": datetime.utcnow().isoformat() + "Z",
            "packager_version": self.packager_version,
            "files": {}
        }
        
        # Try to extract description from SKILL.md frontmatter
        try:
            skill_md_path = self.skill_path / "SKILL.md"
            if skill_md_path.exists():
                content = skill_md_path.read_text(encoding='utf-8')
                if content.startswith('---\n'):
                    import yaml
                    parts = content.split('---\n', 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        if frontmatter:
                            if 'description' in frontmatter:
                                manifest['description'] = frontmatter['description']
                            if 'name' in frontmatter:
                                manifest['skill_name'] = frontmatter['name']
        except Exception:
            pass  # Continue without description
        
        # Add file listing with checksums
        manifest['files']['SKILL.md'] = {
            'checksum': self._calculate_checksum(self.skill_path / "SKILL.md"),
            'size': (self.skill_path / "SKILL.md").stat().st_size
        }
        
        # Add scripts/ files
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists():
            manifest['files']['scripts'] = {}
            for script_file in scripts_dir.rglob('*.py'):
                if self._should_include(script_file):
                    rel_path = script_file.relative_to(self.skill_path)
                    manifest['files']['scripts'][str(rel_path)] = {
                        'checksum': self._calculate_checksum(script_file),
                        'size': script_file.stat().st_size
                    }
        
        # Add references/ files
        references_dir = self.skill_path / "references"
        if references_dir.exists():
            manifest['files']['references'] = {}
            for ref_file in references_dir.rglob('*'):
                if ref_file.is_file() and self._should_include(ref_file):
                    rel_path = ref_file.relative_to(self.skill_path)
                    manifest['files']['references'][str(rel_path)] = {
                        'checksum': self._calculate_checksum(ref_file),
                        'size': ref_file.stat().st_size
                    }
        
        # Add assets/ files
        assets_dir = self.skill_path / "assets"
        if assets_dir.exists():
            manifest['files']['assets'] = {}
            for asset_file in assets_dir.rglob('*'):
                if asset_file.is_file() and self._should_include(asset_file):
                    rel_path = asset_file.relative_to(self.skill_path)
                    # Don't include checksum for large binary files
                    file_size = asset_file.stat().st_size
                    file_info = {'size': file_size}
                    if file_size < 10 * 1024 * 1024:  # Only checksum files < 10MB
                        file_info['checksum'] = self._calculate_checksum(asset_file)
                    manifest['files']['assets'][str(rel_path)] = file_info
        
        return manifest
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum for a file"""
        sha256_hash = hashlib.sha256()
        
        try:
            with open(file_path, "rb") as f:
                # Read file in 4096-byte chunks
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            return sha256_hash.hexdigest()
        except Exception:
            return "error"
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"


def package_multiple_skills(skills_dir: str, pattern: str = "*") -> List[str]:
    """Package all skills in a directory"""
    skills_dir = Path(skills_dir)
    
    if not skills_dir.exists():
        print(f"✗ Directory not found: {skills_dir}")
        return []
    
    # Find all skill folders (containing SKILL.md)
    skill_folders = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            if fnmatch.fnmatch(item.name, pattern):
                skill_folders.append(item)
    
    if not skill_folders:
        print(f"No skills found in {skills_dir}")
        return []
    
    print(f"Found {len(skill_folders)} skill(s) to package\n")
    
    packaged_skills = []
    failed_skills = []
    
    for skill_folder in skill_folders:
        try:
            print(f"\n{'='*70}")
            packager = SkillPackager(str(skill_folder), validate=True, force=False)
            zip_path = packager.package()
            if zip_path:
                packaged_skills.append(zip_path)
        except Exception as e:
            failed_skills.append((skill_folder.name, str(e)))
            print(f"✗ Failed to package {skill_folder.name}: {str(e)}")
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"BATCH PACKAGING SUMMARY")
    print(f"{'='*70}")
    print(f"Total skills: {len(skill_folders)}")
    print(f"Successfully packaged: {len(packaged_skills)}")
    print(f"Failed: {len(failed_skills)}")
    
    if failed_skills:
        print(f"\nFailed skills:")
        for name, error in failed_skills:
            print(f"  - {name}: {error}")
    
    print(f"{'='*70}\n")
    
    return packaged_skills


def package_skill_cli():
    """Command-line interface for skill packaging"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Package Claude Skills for import',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python package_skill.py ./my-skill
  python package_skill.py ./my-skill --output ./dist/my-skill.zip
  python package_skill.py ./my-skill --no-validate
  python package_skill.py ./my-skill --force
  python package_skill.py --batch ./generated_skills
        """
    )
    parser.add_argument('skill_path', nargs='?', help='Path to skill folder')
    parser.add_argument('-o', '--output', help='Output .zip file path')
    parser.add_argument('--no-validate', action='store_true',
                       help='Skip validation before packaging')
    parser.add_argument('--force', action='store_true',
                       help='Package even if validation warnings exist')
    parser.add_argument('--batch', help='Package all skills in directory')
    
    args = parser.parse_args()
    
    try:
        # Handle --batch mode
        if args.batch:
            packaged = package_multiple_skills(args.batch)
            sys.exit(0 if packaged else 1)
        
        # Handle single skill mode
        if not args.skill_path:
            parser.print_help()
            sys.exit(1)
        
        # Create packager with appropriate flags
        packager = SkillPackager(
            args.skill_path,
            validate=not args.no_validate,
            force=args.force
        )
        
        # Call package()
        zip_path = packager.package(args.output)
        
        if zip_path:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nPackaging cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    package_skill_cli()

