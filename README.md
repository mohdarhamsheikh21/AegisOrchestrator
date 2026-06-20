# Aegis — Automated Contextual Security Assessment Pipeline

A Red Team reconnaissance tool built in Python that performs adaptive,
context-aware vulnerability scanning against a target IP or domain.

## What It Does

Aegis runs in three automated phases:

Phase 1 — Reconnaissance
Fingerprints the target using Nmap (-sV -sC) to discover open ports
and identify running services and their versions.

Phase 2 — Adaptive Automation
Instead of running every tool blindly, Aegis reads the discovered ports
and routes the correct tool to each service automatically:
- Port 80/443 → Nikto (web vulnerability scan)
- Port 22     → Hydra (SSH brute force / credential test)
- Port 445    → Nmap SMB vuln scripts (checks for EternalBlue etc.)

Phase 3 — Remediation Report
Generates a structured Markdown report with specific hardening
recommendations for every vulnerability found. Output is saved
to a timestamped directory for documentation.

## Usage

sudo python3 aegis_orchestrator.py <target IP or domain>

Example:
sudo python3 aegis_orchestrator.py 192.168.1.1

## Output
All scan results, tool logs, and the remediation report are saved to:
aegis_scan_<target>_<timestamp>/

## Requirements
- Kali Linux
- Nmap, Nikto, Hydra (pre-installed on Kali)
- Python 3

## Note
This tool is built for ethical security testing only.
Use only on systems you own or have explicit permission to test.

## Tech Stack
Python 3 · Subprocess · Nmap · Nikto · Hydra

## Screenshots
<img width="810" height="439" alt="Screenshot 2026-06-20 223431" src="https://github.com/user-attachments/assets/b1bf8cca-4f02-44d3-b782-c00eacaf8594" />

<img width="810" height="436" alt="Screenshot 2026-06-20 223510" src="https://github.com/user-attachments/assets/2db40dc4-b62a-4bd2-a829-6189cd2b57ab" />


<img width="817" height="442" alt="Screenshot 2026-06-20 232745" src="https://github.com/user-attachments/assets/04dfc1bf-0b09-4898-96d8-4371dd3a1c36" />

<img width="817" height="442" alt="Screenshot 2026-06-20 232745" src="https://github.com/user-attachments/assets/62facb75-d129-4080-a14b-bd7a8e1d2730" />
