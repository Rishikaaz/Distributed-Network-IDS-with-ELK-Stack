# 🛡️ Real-Time Host-Based IDS  & SIEM Integration

A robust security architecture that transforms a Windows workstation into an Intelligent Intrusion Detection Sensor, shipping live security events to a centralized Kali Linux ELK (SIEM) stack for instant analysis.

## 🚀 Overview
This project implements a multi-platform security monitoring solution. A Python-based IDS sensor on a Windows host sniffs network traffic, identifies malicious patterns (like port scans), and transmits enriched JSON alerts over a TCP socket to an ELK stack on Kali Linux. 

I have made the project walkthrough video for better understanding purpose-> https://drive.google.com/file/d/1zRa8HpNQHjkqvb1CAWbWRlVmyXzf2k8W/view?usp=sharing

### Key Features
* **Real-Time Packet Inspection:** Uses Scapy to analyze L3/L4 headers.
* **Intelligent Alerting:** Automatically tags traffic hitting sensitive ports (80, 445, 22) with security context.
* **Centralized Logging:** Persistent TCP streaming to Logstash.
* **Elastic Search & Visualization:** Full query capabilities via Kibana.

## 🛠️ Technology Stack
- **Languages:** Python 3.x
- **Libraries:** Scapy, Socket, JSON
- **SIEM:** Elasticsearch, Logstash, Kibana (ELK)
- **Environment:** Windows (Sensor), Kali Linux (SIEM)
- **Tools:** Nmap (Attack Simulation)

## Repository Structure
├── ids.py                 
├── docker-compose.yml   
├── logstash/
│   └── pipeline/
│       └── logstash.conf  
├── docs/
│   └── architecture.png  
└── README.md


## 🏗️ Architecture
![Architecture Diagram](/architecture.png)

1. **Attack:** Kali Linux initiates an Nmap scan.
2. **Detection:** Windows script intercepts the packet and applies an `alert` tag.
3. **Transport:** Data is shipped via TCP Port 5000 to Logstash.
4. **Visualization:** Alerts are indexed and visualized in Kibana.

## 🚦 Usage

## Configure Logstash

Ensure your Logstash pipeline is listening on TCP 5000 with `json_lines` codec.

## Start all core services
`sudo systemctl start elasticsearch kibana logstash`

## Verify Logstash is listening on Port 5000
`sudo tail -f /var/log/logstash/logstash-plain.log`

## Run Sensor
Open Command Prompt as Administrator and execute:
`python ids.py`

## Simulate Attack from Kali
Trigger the detection logic using Nmap:
`nmap -sT -p 80,445 [Windows_IP]`

## Analyze 
Open Kibana and filter by `alert : *`.

Navigate to http://localhost:5601.

Create a Data View for windows-ids-logs*.

Filter by alert : * in the Discover tab to view security events.


---
