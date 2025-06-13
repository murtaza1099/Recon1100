# Recon1100

A powerful automated reconnaissance tool for security assessments, built with Python and Docker. Recon1100 performs domain enumeration tasks like WHOIS lookup, DNS enumeration, subdomain discovery, HTTP probing, port scanning, banner grabbing, and technology detection.

## Features

- WHOIS Lookup
- DNS Enumeration
- Subdomain Enumeration (with Sublist3r)
- HTTP Probing (with httpx)
- Port Scanning (with nmap)
- Banner Grabbing (with Nikto)
- Technology Detection (with whatweb)
- Easy Dockerized usage
- Saves combined reports to your local machine

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/murtaza1099/Recon1100.git
cd Recon1100
```

### 2. Build the Docker image:

```bash
sudo docker build -t recon1100 .
```

## Usage

### Run the tool (with output saved to your host):

```bash
sudo docker run --rm -v "$(pwd)/reports:/app/reports" recon1100 <domain> [options]
```

#### Example:

```bash
sudo docker run --rm -v "$(pwd)/reports:/app/reports" recon1100 example.com --whois --dns --subdomains --httpx --ports --banner --tech -v
```

### Output

After the scan, your combined report will be saved in the `reports/` directory on your host machine.  
Example:  
```
./reports/example.com_2025-06-12_20-11-51/combined_report.txt
```

## Command-Line Options

| Option       | Description                              |
|--------------|------------------------------------------|
| --whois      | Run WHOIS lookup                         |
| --dns        | Run DNS enumeration                      |
| --subdomains | Run subdomain enumeration                |
| --httpx      | Probe HTTP services                      |
| --ports      | Scan ports                               |
| --banner     | Banner grabbing                          |
| --tech       | Technology detection                     |
| -v           | Verbose output                           |

*You can combine any options as needed.*

## Requirements

- Docker

*All other dependencies are handled inside the container.*

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

## Contact

- **Author:** Murtaza Hasnat  
- **GitHub:** [murtaza1099](https://github.com/murtaza1099)
