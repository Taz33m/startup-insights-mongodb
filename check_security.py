#!/usr/bin/env python3
"""
Security verification script.
Run this before committing code to ensure no sensitive data is exposed.
"""
import os
import re
import sys


def check_gitignore():
    """Verify .gitignore exists and contains critical entries."""
    print("🔍 Checking .gitignore...")
    
    if not os.path.exists('.gitignore'):
        print("❌ .gitignore file not found!")
        return False
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    critical_entries = ['.env', 'venv/', '*.log', '*.key', '*.pem']
    missing = []
    
    for entry in critical_entries:
        if entry not in content:
            missing.append(entry)
    
    if missing:
        print(f"⚠️  Missing critical entries in .gitignore: {missing}")
        return False
    
    print("✅ .gitignore properly configured")
    return True


def check_env_file():
    """Verify .env file is not tracked by git."""
    print("\n🔍 Checking .env file...")
    
    if not os.path.exists('.env'):
        print("ℹ️  .env file not found (this is OK if not set up yet)")
        return True
    
    # Check if .env is in git
    result = os.system('git ls-files .env 2>/dev/null')
    if result == 0:
        print("❌ CRITICAL: .env file is tracked by git!")
        print("   Run: git rm --cached .env")
        return False
    
    print("✅ .env file is not tracked by git")
    return True


def check_for_secrets_in_code():
    """Scan Python files for potential hardcoded secrets."""
    print("\n🔍 Scanning for hardcoded secrets...")
    
    patterns = [
        (r'mongodb\+srv://[^<][^"\']+', 'MongoDB connection string'),
        (r'password\s*=\s*["\'][^"\']{8,}["\']', 'Hardcoded password'),
        (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', 'API key'),
        (r'secret\s*=\s*["\'][^"\']+["\']', 'Secret key'),
    ]
    
    issues_found = []
    
    for root, dirs, files in os.walk('.'):
        # Skip virtual environment and git directories
        dirs[:] = [d for d in dirs if d not in ['venv', '.git', '__pycache__', '.ipynb_checkpoints']]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern, description in patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            # Skip if it's a comment or example
                            line_start = content.rfind('\n', 0, match.start()) + 1
                            line = content[line_start:content.find('\n', match.start())]
                            
                            if not line.strip().startswith('#'):
                                issues_found.append({
                                    'file': filepath,
                                    'description': description,
                                    'line': line.strip()[:80]
                                })
                
                except Exception as e:
                    print(f"⚠️  Could not scan {filepath}: {e}")
    
    if issues_found:
        print(f"⚠️  Found {len(issues_found)} potential security issues:")
        for issue in issues_found:
            print(f"   {issue['file']}: {issue['description']}")
            print(f"      {issue['line']}")
        return False
    
    print("✅ No hardcoded secrets detected")
    return True


def check_env_example():
    """Verify .env.example doesn't contain real credentials."""
    print("\n🔍 Checking .env.example...")
    
    if not os.path.exists('.env.example'):
        print("⚠️  .env.example not found")
        return False
    
    with open('.env.example', 'r') as f:
        content = f.read()
    
    # Check for placeholder patterns
    if '<username>' in content and '<password>' in content:
        print("✅ .env.example uses placeholders")
        return True
    
    # Check for potential real credentials
    if re.search(r'mongodb\+srv://[^<][^@]+@', content):
        print("⚠️  .env.example may contain real credentials!")
        return False
    
    print("✅ .env.example looks safe")
    return True


def check_git_status():
    """Check if any sensitive files are staged for commit."""
    print("\n🔍 Checking git status...")
    
    if not os.path.exists('.git'):
        print("ℹ️  Not a git repository")
        return True
    
    # Get staged files
    import subprocess
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True
        )
        
        staged_files = result.stdout.strip().split('\n')
        
        sensitive_patterns = ['.env', 'credentials', 'secrets', '.pem', '.key']
        sensitive_staged = []
        
        for file in staged_files:
            if file:
                for pattern in sensitive_patterns:
                    if pattern in file.lower():
                        sensitive_staged.append(file)
        
        if sensitive_staged:
            print(f"❌ Sensitive files staged for commit: {sensitive_staged}")
            print("   Run: git reset HEAD <file> to unstage")
            return False
        
        print("✅ No sensitive files staged")
        return True
    
    except Exception as e:
        print(f"⚠️  Could not check git status: {e}")
        return True


def main():
    """Run all security checks."""
    print("="*60)
    print("🔒 SECURITY VERIFICATION")
    print("="*60)
    
    checks = [
        check_gitignore(),
        check_env_file(),
        check_env_example(),
        check_for_secrets_in_code(),
        check_git_status()
    ]
    
    print("\n" + "="*60)
    
    if all(checks):
        print("✅ All security checks passed!")
        print("\n💡 Tips:")
        print("   - Review changes before committing: git diff")
        print("   - Never commit .env files")
        print("   - Use environment variables for secrets")
        print("   - Rotate credentials if accidentally exposed")
        return 0
    else:
        print("❌ Some security checks failed!")
        print("\n⚠️  Please fix the issues above before committing.")
        print("\n📖 See SECURITY.md for detailed guidelines")
        return 1


if __name__ == "__main__":
    sys.exit(main())
