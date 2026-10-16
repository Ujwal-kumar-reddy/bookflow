"""
Secrets and Git Hygiene Scanner for BookFlow Capstone
Scans all tracked files and the entire commit history for credentials and sensitive data.
"""
import subprocess
import re
import sys

def main():
    print("=" * 60)
    print("BOOKFLOW PRE-PUSH SECRETS & HYGIENE AUDIT")
    print("=" * 60)

    # 1. Tracked Files Check
    print("\n[1] Checking tracked files against sensitive patterns...")
    res = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, encoding='utf-8', errors='replace')
    tracked = res.stdout.splitlines()

    sensitive_patterns = [
        r'\.env$', r'\.tfstate$', r'\.tfvars$', r'id_rsa', r'\.pem$', r'\.key$', r'kubeconfig'
    ]

    flagged_files = []
    for f in tracked:
        for pat in sensitive_patterns:
            if re.search(pat, f, re.IGNORECASE) and not f.endswith('.example') and not f.endswith('.md'):
                flagged_files.append((f, pat))

    if flagged_files:
        print("  FAILED: Sensitive files found tracked in Git!")
        for f, pat in flagged_files:
            print(f"    - {f} (matched {pat})")
        sys.exit(1)
    else:
        print(f"  PASSED: 0 sensitive files tracked (out of {len(tracked)} total files).")

    # 2. Commit History Diffs Scan
    print("\n[2] Scanning full git log commit diffs for secret patterns...")
    res = subprocess.run(['git', 'log', '-p'], capture_output=True, text=True, encoding='utf-8', errors='replace')
    diff_text = res.stdout

    secret_regexes = [
        (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
        (r'-----BEGIN (?:RSA|OPENSSH|EC|DSA|PGP) PRIVATE KEY-----', 'Private Key'),
        (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token'),
        (r'xox[baprs]-[0-9a-zA-Z]{10,48}', 'Slack Token'),
        (r'aws_secret_access_key\s*=\s*["\']?[A-Za-z0-9/+=]{20,}', 'AWS Secret Access Key')
    ]

    found_secrets = []
    for pat, desc in secret_regexes:
        matches = re.findall(pat, diff_text)
        if matches:
            found_secrets.append((desc, len(matches)))

    if found_secrets:
        print("  FAILED: Secrets found in commit history!")
        for desc, count in found_secrets:
            print(f"    - {desc}: {count} occurrences")
        sys.exit(1)
    else:
        print(f"  PASSED: 0 secret patterns detected ({len(diff_text)} bytes of git history scanned).")

    print("\n" + "=" * 60)
    print("ALL AUDITS PASSED: REPOSITORY IS CLEAN AND READY FOR REMOTE")
    print("=" * 60)

if __name__ == "__main__":
    main()
