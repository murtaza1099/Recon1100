import argparse
import os
import datetime

from utils.logger import setup_logging, log
from utils.reports import save_combined_report

from modules import whois_lookup, dns_enum, subdomain_enum, port_scan, http_probe, tech_detect, banner_grab

def make_report_folder(domain, timestamp):
    folder_name = f"reports/{domain}_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def main():
    parser = argparse.ArgumentParser(description="Recon1100: Recon Suite (final version, combined report)")
    parser.add_argument("domain", help="Target domain (e.g., facebook.com)")
    parser.add_argument("--whois", action="store_true", help="Enable WHOIS lookup")
    parser.add_argument("--dns", action="store_true", help="Enable DNS enumeration")
    parser.add_argument("--subdomains", action="store_true", help="Enable Subdomain enumeration")
    parser.add_argument("--httpx", action="store_true", help="Enable HTTP probing (httpx)")
    parser.add_argument("--ports", action="store_true", help="Enable Port scanning (top/common ports)")
    parser.add_argument("--banner", action="store_true", help="Enable Banner grabbing (Nikto)")
    parser.add_argument("--tech", action="store_true", help="Enable Technology detection (WhatWeb)")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase output verbosity")
    args = parser.parse_args()

    setup_logging(args.verbose)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = make_report_folder(args.domain, timestamp)
    combined_report = []

    # WHOIS
    if args.whois:
        log("INFO", "Running WHOIS lookup")
        res = whois_lookup.run(args.domain)
        combined_report.append("=== WHOIS ===\n" + res.get('output', 'No output'))

    # DNS
    if args.dns:
        log("INFO", "Running DNS enumeration")
        res = dns_enum.run(args.domain)
        combined_report.append("=== DNS Enumeration ===\n" + res.get('output', 'No output'))

    # Subdomain Enumeration
    subdomains = []
    if args.subdomains:
        log("INFO", "Running Subdomain enumeration")
        res = subdomain_enum.run(args.domain)
        subdomains = subdomain_enum.parse_subdomains(res.get("output", ""), args.domain)
        combined_report.append("=== Subdomains ===\n" + ("\n".join(subdomains) if subdomains else res.get("output", "No output")))

    # HTTPX Probing
    httpx_targets = subdomains if subdomains else [args.domain]
    if args.httpx:
        log("INFO", "Running HTTPX probing")
        res = http_probe.run(args.domain, httpx_targets)
        combined_report.append("=== HTTPX Probing ===\n" + res.get('output', 'No output'))

    # Port Scanning
    open_ports = []
    if args.ports:
        log("INFO", "Running port scanning")
        res = port_scan.run(args.domain)
        open_ports = res.get("open_ports", [])
        combined_report.append("=== Port Scanning ===\n" + res.get('output', 'No output'))

    # Banner Grabbing (Nikto or custom)
    if args.banner:
        log("INFO", "Running banner grabbing")
        nikto_targets = []
        if open_ports:
            for port in open_ports:
                if port in [80, 443, 8080, 8000, 8443]:
                    scheme = "https" if port in [443, 8443] else "http"
                    nikto_targets.append(f"{scheme}://{args.domain}:{port}")
        if not nikto_targets:
            nikto_targets = [f"http://{args.domain}:80"]
        res = banner_grab.run(nikto_targets)
        combined_report.append("=== Banner Grabbing (Nikto) ===\n" + res.get('output', 'No output'))

    # Technology Detection (WhatWeb)
    if args.tech:
        log("INFO", "Running technology detection")
        urls = []
        httpx_txt_path = os.path.join(report_dir, "httpx.txt")
        if os.path.exists(httpx_txt_path):
            with open(httpx_txt_path) as f:
                urls = http_probe.extract_urls(f.read())
        if not urls:
            urls = [f"https://{args.domain}"]
        res = tech_detect.run(urls)
        combined_report.append("=== Technology Detection (WhatWeb) ===\n" + res.get('output', 'No output'))

    # Save combined report
    save_combined_report(report_dir, "combined_report.txt", combined_report)
    log("INFO", f"Scan complete! Combined report: {os.path.join(report_dir, 'combined_report.txt')}")

if __name__ == "__main__":
    main()
