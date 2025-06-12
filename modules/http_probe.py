import subprocess
import tempfile
import os

def run(domain, targets):
    try:
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            for line in targets:
                f.write(line.strip()+"\n")
            f.flush()
            temp_input_path = f.name
        cmd = ["httpx", "-l", temp_input_path, "-status-code", "-title", "-follow-redirects", "-tech-detect", "-json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        os.unlink(temp_input_path)
        if proc.returncode != 0:
            return {"status": "error", "output": f"httpx error: {proc.stderr.strip()}"}
        lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
        return {"status": "success", "output": "\n".join(lines)}
    except Exception as e:
        return {"status": "error", "output": f"httpx failed: {str(e)}"}

def extract_urls(httpx_output):
    # Extract URLs from httpx JSONL output
    import json
    urls = []
    for line in httpx_output.splitlines():
        try:
            data = json.loads(line)
            if "url" in data:
                urls.append(data["url"])
        except Exception:
            continue
    return urls
