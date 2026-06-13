# HealthCare

**Difficulty:** Easy
**OS:** Linux
**Attack Chain:** XXE → Credential Disclosure → File Upload → RCE → Lateral Movement → Command Injection

---

## Story

HealthSync is one of Türkiye's largest digital healthcare management platforms, connecting 47 hospitals and serving over 850,000 patients. Three weeks ago, an anonymous whistleblower surfaced on a dark-web forum claiming to possess complete patient records — medical histories, prescriptions, test results, and personal identifiers — allegedly exfiltrated from HealthSync's primary web application server.

The system administrator, a contractor named **Magnus Vinter**, has been unreachable since the breach was discovered. A preliminary external audit uncovered anomalous outbound traffic originating from the web application server on May 14, 2026 — the same day Magnus last modified the system configuration.

Your task as an incident response specialist:

1. Identify the initial attack vector used to compromise the HealthSync web application
2. Trace the lateral movement path through their internal network
3. Recover the two digital signatures left behind — one on the web server, one on an internal monitoring node

---

## Network Topology

```
┌─────────────────────────────────┐
│        Attacker Machine          │
│     (Your Attack Platform)       │
└───────────────┬─────────────────┘
                │
    ┌───────────┴──────────────┐
    │   Host Port Mappings        │
    │   80 → Flask Web App        │
    │   8080 → Apache/PHP         │
    │   22 → SSH                  │
    └───────────┬──────────────┘
                │
   ╔════════════╧════════════════╗
   ║   healthnet (172.20.0.0/24) ║
   ╠════════════╤════════════════╣
   ║            │                ║
┌──┴──────┐  ┌──┴──────┐
│ webapp   │  │ monitor  │
│.10       │  │.20       │
│          │  │          │
│Flask:5000│  │Flask:8080│
│Apache:80 │  │(internal)│
│SSH:22    │  │          │
│          │  │ root.txt │
│user.txt  │  │          │
└──────────┘  └──────────┘
```

---

## Flags

| Flag | Path | Owner | Perms |
|------|------|-------|-------|
| user.txt | `/home/devops/user.txt` | root:devops | 644 |
| root.txt | `/root/root.txt` | root:root | 640 |

---

## Setup

```bash
docker compose up -d --build
```

Verify:

```bash
curl -s http://localhost/health
# {"service":"healthsync-webapp","status":"ok","version":"2.4.1"}
```

---

## Intended Attack Path

1. **Reconnaissance** — Discover hidden paths via `robots.txt`
2. **XXE Injection** — Extract credentials from `/etc/healthsync/app.conf`
3. **Authentication Bypass** — Login to upload portal with leaked credentials
4. **File Upload — Webshell** — Upload PHP shell, gain RCE via Apache on port 8080
5. **Credential Theft** — Extract SSH private key from `/home/devops/.ssh/id_rsa`
6. **SSH Access** — Connect as `devops` on port 22, capture `user.txt`
7. **Internal Reconnaissance** — Scan internal subnet, discover monitor service at 172.20.0.20:8080
8. **Command Injection** — Exploit `/ping` endpoint, escalate to root on monitor
9. **Capture root.txt**

---

## Credentials

| User | Password | Purpose |
|------|----------|---------|
| magnus | superman | Upload portal login |
| devops | devops2026! | SSH access (key preferred) |
