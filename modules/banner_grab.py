import subprocess

def run(urls):
    """
    Runs Nikto banner grabbing on a list of URLs.
    Returns a dict with 'output' key.
    """
    output = []
    for url in urls:
        output.append(f"=== {url} ===")
        try:
            proc = subprocess.run(
                ["nikto", "-host", url, "-Tuning", "x 6"],
                capture_output=True,
                text=True,
                timeout=120
            )
            # Only print Nikto output, not errors unless there's a failure
            if proc.returncode == 0:
                output.append(proc.stdout.strip())
            else:
                output.append(f"Nikto error (code {proc.returncode}):\n{proc.stderr.strip()}")
        except Exception as e:
            output.append(f"Nikto failed: {e}")
    return {"output": "\n\n".join(output)}
