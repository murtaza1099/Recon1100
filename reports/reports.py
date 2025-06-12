import os

def save_report(report_dir, filename, content):
    """
    Save the given content to a file in the report directory.
    """
    if not os.path.exists(report_dir):
        os.makedirs(report_dir, exist_ok=True)
    path = os.path.join(report_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def save_summary(report_dir, summary_lines):
    """
    Save a summary of the scan in summary.txt in the report directory.
    """
    path = os.path.join(report_dir, "summary.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("Recon1100 Summary\n")
        f.write("="*30 + "\n")
        for line in summary_lines:
            f.write(f"{line}\n")
