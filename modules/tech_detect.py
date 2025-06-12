import subprocess

def run(urls):
    """
    Runs WhatWeb on a list of URLs and returns a dict with 'output' key.
    Each URL is scanned separately.
    """
    output = []
    for url in urls:
        output.append(f"{url} :")
        try:
            proc = subprocess.run(
                ["whatweb", "--no-errors", "--color=never", url],
                capture_output=True,
                text=True,
                timeout=30
            )
            if proc.returncode == 0:
                # Only print WhatWeb output, not errors unless there's a failure
                output.append(proc.stdout.strip())
            else:
                output.append(f"WhatWeb error (code {proc.returncode}):\n{proc.stderr.strip()}")
        except Exception as e:
            output.append(f"WhatWeb failed: {e}")
        output.append("")  # Blank line for readability
    return {"output": "\n".join(output)}
