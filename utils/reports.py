import os

def save_combined_report(report_dir, filename, sections):
    """
    Save all recon sections into both a single text report and an HTML report file.
    """
    if not os.path.exists(report_dir):
        os.makedirs(report_dir, exist_ok=True)

    # Save as plain text
    txt_path = os.path.join(report_dir, filename)
    with open(txt_path, "w", encoding="utf-8") as f:
        for section in sections:
            f.write(section.strip() + "\n\n")

    # Save as HTML
    html_path = os.path.join(report_dir, filename.replace('.txt', '.html'))
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(
            "<html><head><meta charset='UTF-8'><title>Recon1100 Report</title></head>"
            "<body style='font-family:monospace;'>\n"
            "<h1>Recon1100 Combined Report</h1>\n"
        )
        for section in sections:
            title = section.split('\n', 1)[0]
            content = section.split('\n', 1)[1] if '\n' in section else ''
            f.write(f"<h2>{title}</h2>\n")
            f.write("<pre style='background:#f4f4f4;padding:1em;border-radius:4px;'>\n")
            f.write(content)
            f.write("\n</pre>\n")
        f.write("</body></html>")
