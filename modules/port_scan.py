import subprocess
import re

# Top/common ports (can be expanded as needed)
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080, 8000, 8443]

def run(domain):
    try:
        ports_str = ",".join(str(p) for p in COMMON_PORTS)
        cmd = ["nmap", "-sV", "-p", ports_str, "--open", domain]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if proc.returncode != 0:
            return {"status": "error", "output": f"nmap error: {proc.stderr.strip()}", "open_ports": []}
        output = proc.stdout.strip()
        open_ports = []
        # Example line: 80/tcp  open  http
        for line in output.splitlines():
            m = re.match(r"^(\d+)/tcp\s+open", line)
            if m:
                open_ports.append(int(m.group(1)))
        return {"status": "success", "output": output, "open_ports": open_ports}
    except subprocess.TimeoutExpired:
        return {"status": "error", "output": "nmap timed out", "open_ports": []}
    except Exception as e:
        return {"status": "error", "output": f"Port scan failed: {str(e)}", "open_ports": []}
