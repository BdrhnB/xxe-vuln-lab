This repository allows you to prove your xxe security skills

# HealthCare

> **Category:** Web / Linux
> **Attack Chain:** XXE → Credential Disclosure → File Upload → RCE → Internal Pivot → Command Injection → Privilege Escalation

---

## Narrative

*A classified intelligence briefing lands on your desk at 06:42 AM.*

"Agent,

Three weeks ago, an anonymous whistleblower surfaced on a dark-web forum claiming to possess over 850,000 patient records — full medical histories, prescriptions, test results, and personal identifiers — allegedly exfiltrated from **HealthSync**, Türkiye'nin en büyük dijital sağlık yönetim platformu.

The records have been confirmed authentic. They are being auctioned in batches of 10,000.

HealthSync's CISO initially denied any breach, but a preliminary external audit has uncovered anomalous outbound traffic from their primary web application server. The system administrator, a contractor named **Magnus Vinter**, has been unreachable for the past five days.

Your mission:

1.  **Identify** how the attackers gained initial access to the HealthSync web application.
2.  **Trace** the lateral movement path through their internal network.
3.  **Recover** the two digital signatures (flags) left behind by the attackers — one on the web server, one on an internal monitoring node.

The flags serve as proof of compromise for the board of directors.

We've isolated the servers in a lab environment. The network topology has been preserved. You have local access.

Proceed."

---

## Lab Topology

```
                   ┌──────────────────────────────┐
                   │     Attacker Machine          │
                   │     (Your Kali / Parrot)      │
                   └──────────────┬───────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │   Host Port Mappings        │
                    │   5001 → Flask Web App      │
                    │   8082 → Apache/PHP         │
                    │   2223 → SSH                │
                    └─────────────┬──────────────┘
                                  │
              ╔═══════════════════╧═══════════════════╗
              ║         healthnet (172.20.0.0/24)      ║
              ╠═══════════════════╤═══════════════════╣
              ║                   │                   ║
       ┌──────┴──────┐     ┌──────┴──────┐
       │   webapp     │     │   monitor   │
       │ 172.20.0.10  │     │ 172.20.0.20 │
       │              │     │             │
       │ Flask :5000  │     │ Flask :8080  │
       │ Apache :8080 │     │  (internal) │
       │ SSH    :22   │     │             │
       │              │     │  root.txt   │
       │  user.txt    │     │             │
       └──────────────┘     └──────────────┘
```

---

## Objectives

| Flag | Location | Container | Access Level |
|------|----------|-----------|-------------|
| `user.txt` | `/home/devops/user.txt` | webapp | devops shell |
| `root.txt` | `/root/root.txt` | monitor | root shell |

---

## Setup

```bash
docker compose up -d --build
```

Wait 30 seconds for the services to initialize, then verify:

```bash
curl -s http://localhost:5001/ | head -5
curl -s http://localhost:5001/health
```

---

## Hints

> Use these only if you're stuck. They are layered from gentle nudge to full reveal.

<details>
<summary><b>Hint 1</b> — Where to start looking</summary>
Every web application has a sitemap. Check `robots.txt` — developers often disallow sensitive paths.
</details>

<details>
<summary><b>Hint 2</b> — Something smells like XML</summary>
The appointment form sends XML to an API endpoint. XML parsers can be dangerous if they resolve external entities. Try reading a local file.
</details>

<details>
<summary><b>Hint 3</b> — Did you get creds?</summary>
If you've read the config file, you have a username and password. Look for login pages under the disallowed paths.
</details>

<details>
<summary><b>Hint 4</b> — You're in. Now what?</summary>
The upload panel accepts `.php` files. The files are served by Apache on a different port. Check port 8081.
</details>

<details>
<summary><b>Hint 5</b> — Need a foothold?</summary>
Check `/home/devops/.ssh/` for SSH keys. SSH is listening on port 2222.
</details>

<details>
<summary><b>Hint 6</b> — You have a shell. Where's the second flag?</summary>
The root flag isn't on this machine. Check `/etc/hosts` and scan the internal subnet.
</details>

<details>
<summary><b>Hint 7</b> — Found the monitor service?</summary>
The `/ping` endpoint takes a host parameter. What happens if you append a semicolon?
</details>
>>>>>>> a00a62a (all lab completly updated)
