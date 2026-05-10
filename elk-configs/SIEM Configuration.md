```markdown
🛠️ Logstash Configuration & Setup Guide
---

1. Pipeline Configuration File

Command:
sudo nano /etc/logstash/conf.d/windows_ids.conf

```

**Configuration Content:**

```conf
📥 Input: Listen for TCP traffic on Port 5000
input {
  tcp {
    port => 5000
    codec => json_lines
  }
}

⚙️ Filter: Add metadata to incoming logs
filter {
  mutate {
    add_tag => [ "windows_ids_sensor" ]
  }
}

📤 Output: Ship logs to Elasticsearch and Terminal
output {
  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "windows-ids-logs"
  }
  
  # Useful for debugging; prints raw JSON to the Kali terminal
  stdout { 
    codec => rubydebug 
  }
}

```

---

## 2. Firewall Configuration

Ensure that your Kali Linux VM allows incoming traffic from your Windows machine on the specific Logstash port.

**Command:**

```bash
sudo ufw allow 5000/tcp

```

---

## 3. Service Management

Apply the changes by reloading the system daemon and restarting the Logstash service.

**Commands:**

```bash
# Reload system configurations
sudo systemctl daemon-reload

# Restart the service to apply the new .conf file
sudo systemctl restart logstash

# (Optional) Enable Logstash to start automatically on boot
sudo systemctl enable logstash

```

---

## 4. Verification & Troubleshooting

Logstash uses a Java Virtual Machine (JVM) and may take **30–60 seconds** to fully initialize the listener.

**Check service status:**

```bash
sudo systemctl status logstash

```

**Monitor real-time logs for errors:**

```bash
sudo tail -f /var/log/logstash/logstash-plain.log

```

> **Note:** Look for the message: `Successfully started TCP input listener on port 5000`.

---

## 5. Data Flow Validation

Once the service is active:

1. Start the `ids.py` script on your Windows Host.
2. Run an Nmap scan from Kali: `nmap -p 80 [Windows_IP]`.
3. Observe the Logstash terminal output (if running in foreground) or check **Kibana Discover** to see the indexed events.

```


```
