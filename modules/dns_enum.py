import dns.resolver

def run(domain):
    """
    Performs DNS enumeration for common record types and returns a dict with 'output' key.
    """
    output = []
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for r in answers:
                output.append(f"{rtype}: {r.to_text()}")
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            output.append(f"{rtype}: No record")
        except Exception as e:
            output.append(f"{rtype}: Error: {e}")
    return {"output": "\n".join(output)}
