# 🛡️ Real-Time Host-Based IDS  & SIEM Integration

A robust security architecture that transforms a Windows workstation into an Intelligent Intrusion Detection Sensor, shipping live security events to a centralized ELK (SIEM) stack for instant analysis. This repository offers two deployment models: Docker Containers or a Native Kali Linux Installation.

## 🚀 Overview
This project implements a multi-platform security monitoring solution. A Python-based IDS sensor on a Windows host sniffs network traffic, identifies malicious patterns (like port scans), and transmits enriched JSON alerts over a TCP socket to an ELK stack. 

I have made the project walkthrough video for better understanding purpose-> https://drive.google.com/file/d/1zRa8HpNQHjkqvb1CAWbWRlVmyXzf2k8W/view?usp=sharing

### Key Features
* **Real-Time Packet Inspection:** Uses Scapy to analyze L3/L4 headers.
* **Intelligent Alerting:** Automatically tags traffic hitting sensitive ports (80, 445, 22) with security context.
* **Centralized Logging:** Persistent TCP streaming to Logstash.
* **Elastic Search & Visualization:** Full query capabilities via Kibana.

## 🛠️ Technology Stack
- **Languages:** Python 3.x
- **Libraries:** Scapy, Socket, JSON
- **SIEM Options:** Docker Desktop Core OR Native Kali Linux Services(Elasticsearch, Logstash, Kibana (ELK)).
- **Environment:** Windows (Sensor Node / Docker Host), Kali Linux (Alternative SIEM Node)
- **Tools:** Nmap (Attack Simulation)

## Repository Structure

```text
├── ids-script.py
├── docker-compose.yml
├── architecture.png
├── README.md
├── logstash/
│   └── pipeline/
│       └── logstash.conf
└── kali-native-configs/
    ├── logstash.conf
    └── SIEM Configuration.md
```

## 🏗️ Architecture
![Architecture Diagram](/architecture.png)

1. **Attack:** Kali Linux initiates an Nmap scan.
2. **Detection:** Windows script intercepts the packet and applies an `alert` tag.
3. **Transport:** Data is shipped via TCP Port 5000 to Logstash.
4. **Visualization:** Alerts are indexed and visualized in Kibana.


## 🚦 Deployment Option A: Docker Containers (Recommended)

This method allows you to run the entire SIEM platform locally on your machine alongside the sensor via Docker without needing a separate virtual machine.

### 1. Launch the Environment
Run the following command in your root project folder to download and spin up the ELK containers in the background:
```
docker-compose up -d
```

### 2. Run the Sensor (Windows)
Ensure LOGSTASH_IP = "127.0.0.1" in your ids-script.py, open Command Prompt as Administrator, and run:

```python ids-script.py```

### 3. Attack Simulation & Kibana Analysis
Scan: Run ```nmap -sT -p 80,445 127.0.0.1``` from a secondary terminal.

Visualize: Navigate to ```http://localhost:5601``` to access Kibana, create a Data View for windows-ids-logs*, and monitor the Discover tab.

## 🚦 Deployment Option B: Native Kali Linux Stack

If you prefer deploying the SIEM platform natively inside a dedicated Kali Linux virtual machine, use the configuration variants stored in the kali-native-configs/ folder.

### 1. Configure the Pipeline
Ensure your Logstash pipeline is listening on TCP port 5000 with the json_lines codec by dropping the backup configuration file into your Kali Linux configurations directory:

```sudo cp kali-native-configs/logstash.conf /etc/logstash/conf.d/windows_ids.conf```
### 2. Service Initialization
Run the following commands on your Kali machine to open network rules and start up the native ELK services:

# Allow ingestion traffic through the firewall
```sudo ufw allow 5000/tcp```

# Start core services
```sudo systemctl start elasticsearch kibana logstash```

# Verify the Logstash engine has successfully initialized the listener
```sudo tail -f /var/log/logstash/logstash-plain.log```

### 3. Run Sensor
Open Command Prompt as Administrator and execute:
`python ids.py`

### 4. Simulate Attack from Kali
Trigger the detection logic using Nmap:
`nmap -sT -p 80,445 [Windows_IP]`


### 5. Analyze 
Open Kibana and filter by `alert : *`.

Navigate to http://localhost:5601.

Create a Data View for windows-ids-logs*.

Filter by alert : * in the Discover tab to view security events.


---
