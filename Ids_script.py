import socket
import json
from scapy.all import sniff, IP, TCP, UDP, conf

LOGSTASH_IP = '127.0.0.1' 
LOGSTASH_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((LOGSTASH_IP, LOGSTASH_PORT))
    print(f"Connected to Logstash at {LOGSTASH_IP}:{LOGSTASH_PORT}")
except Exception as e:
    print(f"Connection failed: {e}. Check if Logstash and Port Forwarding are active.")

def send_to_elk(data):
    global sock
    try:
        message = json.dumps(data) + "\n"
        sock.sendall(message.encode('utf-8'))
    except (socket.error, BrokenPipeError):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((LOGSTASH_IP, LOGSTASH_PORT))
            sock.sendall((json.dumps(data) + "\n").encode('utf-8'))
        except:
            pass

def monitor_packet(pkt):
    if pkt.haslayer(IP):
        log_entry = {
            "src_ip": pkt[IP].src,
            "dst_ip": pkt[IP].dst,
            "proto": int(pkt[IP].proto),
            "length": len(pkt),
            "hostname": "Windows-Host-Sensor"
        }
        
        if pkt.haslayer(TCP):
            log_entry["dport"] = int(pkt[TCP].dport)
            log_entry["sport"] = int(pkt[TCP].sport)
            
            if pkt[TCP].dport == 445: 
                print(f"!!! ALERT: SMB Scan detected from {pkt[IP].src} !!!") 
                log_entry["alert"] = "Potential Ransomware/SMB Scan"
            elif pkt[TCP].dport == 22:
                print(f"!!! ALERT: SSH Scan detected from {pkt[IP].src} !!!")
                log_entry["alert"] = "SSH Scan Detected"
        
        elif pkt.haslayer(UDP):
            log_entry["dport"] = int(pkt[UDP].dport)
            log_entry["sport"] = int(pkt[UDP].sport)

        send_to_elk(log_entry)

try:
    my_iface = conf.ifaces.dev_from_index(22)
    print(f"Monitoring on: {my_iface.description}")
    print("Sending live data to Kali ELK... Press Ctrl+C to stop.")
    
    sniff(iface=my_iface, filter="ip", prn=monitor_packet, store=0)
    
except Exception as e:
    print(f"Error starting sniffer: {e}")
    print("Try running the script as Administrator.")