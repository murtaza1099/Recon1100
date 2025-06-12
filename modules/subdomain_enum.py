import subprocess
import re

def run(domain):
    try:
        cmd = ["sublist3r", "-d", domain, "-o", "-"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode != 0:
            return {"status": "error", "output": f"Sublist3r error: {proc.stderr.strip()}"}
        return {"status": "success", "output": proc.stdout.strip()}
    except subprocess.TimeoutExpired:
        return {"status": "error", "output": "Sublist3r timed out"}
    except Exception as e:
        return {"status": "error", "output": f"Subdomain enumeration failed: {str(e)}"}

def parse_subdomains(raw_output, domain):
    """
    Extracts subdomains from sublist3r output (from stdout).
    """
    subdomains = []
    for line in raw_output.splitlines():
        line = line.strip()
        if re.match(rf"^([\w\-\_]+\.)+{re.escape(domain)}$", line, re.IGNORECASE):
            subdomains.append(line)
    return list(sorted(set(subdomains)))
