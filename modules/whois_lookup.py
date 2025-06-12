import whois

def run(domain):
    try:
        w = whois.whois(domain)
        # Some fields might be lists or None, convert all to string for output
        output = ""
        for key, value in w.items():
            if value is None:
                continue
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value if v)
            output += f"{key}: {value}\n"
        return {"status": "success", "output": output}
    except Exception as e:
        return {"status": "error", "output": f"WHOIS lookup failed: {str(e)}"}

