FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

# Install system tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv whatweb nikto nmap wget unzip && \
    apt-get clean

WORKDIR /app

COPY . /app

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python requirements + sublist3r in venv
RUN pip install --no-cache-dir -r requirements.txt sublist3r

# Install httpx CLI tool (ProjectDiscovery)
RUN wget https://github.com/projectdiscovery/httpx/releases/download/v1.6.6/httpx_1.6.6_linux_amd64.zip && \
    unzip httpx_1.6.6_linux_amd64.zip && \
    mv httpx /usr/local/bin/ && \
    chmod +x /usr/local/bin/httpx && \
    rm httpx_1.6.6_linux_amd64.zip LICENSE.md README.md

ENTRYPOINT ["python3", "main.py"]
