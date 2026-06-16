# HealthSync

A Docker-based penetration testing lab simulating a realistic healthcare platform breach. Chain multiple vulnerabilities — from web application exploitation to internal network pivoting — to capture both flags.

## Story

HealthSync is a digital healthcare management platform connecting 47 hospitals and serving over 850,000 patients. Three weeks after launch, patient records began appearing on dark-web forums. The system administrator, a contractor named **Magnus Vinter**, has been unreachable since the breach.

As an incident response specialist, your task is to trace the attackers' path through the infrastructure and recover the digital signatures they left behind.

## Network Topology

```
Internet
   │
   ├── :80   → Flask (hospital web application)
   ├── :8080 → Apache/PHP (file server)
   └── :22   → SSH
          │
   ╔═══════╧════════════╗
   ║  healthnet          ║
   ║  172.20.0.0/24      ║
   ╠═════════╤══════════╣
   ║         │           ║
  webapp    monitor      ║
  .10       .20          ║
   │                     ║
   ├─ Flask :5000        ║
   ├─ Apache :8080       ║
   ├─ SSH :22             ║
   └─ user.txt           ║
                         ║
                  Flask :8080 (internal)
                  root.txt
```

## Attack Path

1. **Reconnaissance** — `robots.txt` reveals hidden endpoints
2. **XXE Injection** — Read the application config file via XML external entity
3. **Credential Theft** — Extract portal credentials from the leaked config
4. **File Upload** — Upload a PHP webshell through the authenticated portal
5. **Remote Code Execution** — Execute commands via the uploaded webshell
6. **SSH Key Theft** — Steal the devops user's private key
7. **Initial Access** — SSH into the webapp container, capture user flag
8. **Internal Reconnaissance** — Scan the internal subnet for additional services
9. **Command Injection** — Exploit the internal monitor service running as root
10. **Privilege Escalation** — Capture the root flag via command injection

## Quick Start

```bash
git clone https://github.com/BdrhnB/xxe-vuln-lab.git
cd xxe-vuln-lab
docker compose up -d --build
```

Verify:

```bash
curl http://localhost/health
# {"service":"healthsync-webapp","status":"ok","version":"2.4.1"}
```

## Requirements

- Docker Engine 24+
- Docker Compose v2
- 2 GB RAM, 2 CPUs

## Services

| Container | Hostname | IP | Exposed |
|-----------|----------|----|---------|
| medivault-webapp | webapp | 172.20.0.10 | :80, :8080, :22 |
| medivault-monitor | monitor | 172.20.0.20 | — (internal) |

## Vulnerabilities

| CWE | Vulnerability | Location |
|-----|-------------|----------|
| CWE-611 | XML External Entity (XXE) Injection | `/api/appointment/check` |
| CWE-256 | Plaintext Credential Storage | `/etc/healthsync/app.conf` |
| CWE-434 | Unrestricted File Upload | `/uploads/upload` |
| CWE-538 | Sensitive File Exposure | `/home/devops/.ssh/id_rsa` |
| CWE-78 | OS Command Injection | Monitor `/ping`, `/diagnose` |

## License

This project is for educational and training purposes only.
