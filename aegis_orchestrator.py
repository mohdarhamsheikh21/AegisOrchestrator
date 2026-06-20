#!/usr/bin/env python3
"""
================================================================================
AegisOrchestrator - Context-Aware Defensive & Offensive Security Pipeline
================================================================================
"""

import os
import sys
import subprocess
from datetime import datetime

# Enforce Root Privileges for raw network scanning
if os.geteuid() != 0:
    print("\n[-] Error: Administrative privileges required.")
    print("[*] Please execute using: sudo python3 aegis_orchestrator.py <target>\n")
    sys.exit(1)

class AegisOrchestrator:
    def __init__(self, target):
        self.target = target
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f"aegis_scan_{self.target}_{self.timestamp}"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def print_banner(self):
        banner = f"""
    █████╗ ███████╗ ██████╗ ██╗███████╗
   ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝
   ███████║█████╗  ██║  ███╗██║███████╗
   ██╔══██║██╔══╝  ██║   ██║██║╚════██║
   ██║  ██║███████╗╚██████╔╝██║███████║
   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝
   >> Automated Contextual Enumeration Engine <<
   Target: {self.target} | Logs: ./{self.output_dir}/
================================================================================
        """
        print(banner)

    def log(self, message, event_type="INFO"):
        prefix = {
            "INFO":    "[\033[94m*\033[0m]", 
            "SUCCESS": "[\033[92m+\033[0m]", 
            "ALERT":   "[\033[93m!\033[0m]", 
            "ERROR":   "[\033[91m-\033[0m]"
        }
        print(f"{prefix.get(event_type, '[*]')} {message}")

    def execute_core(self, cmd, log_name):
        """Pipeline execution engine with live terminal streaming and file buffering."""
        target_path = os.path.join(self.output_dir, log_name)
        try:
            with open(target_path, "w") as f:
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in proc.stdout:
                    print(f"    {line.strip()}")
                    f.write(line)
                proc.wait()
            return True
        except Exception as e:
            self.log(f"Pipeline execution failure: {e}", "ERROR")
            return False

    def run_reconnaissance(self):
        """Phase 1: Footprinting & Service-Mapping via Nmap."""
        self.log("Initializing service fingerprinting scan...", "INFO")
        summary_file = os.path.join(self.output_dir, "nmap_summary.txt")
        
        nmap_cmd = f"nmap -sV -sC -F -oN {summary_file} {self.target}"
        self.execute_core(nmap_cmd, "nmap_raw.log")
        
        open_ports = []
        if os.path.exists(summary_file):
            with open(summary_file, "r") as f:
                for line in f:
                    if "/tcp" in line and "open" in line:
                        port = line.split("/")[0].strip()
                        open_ports.append(int(port))
        return open_ports

    def adaptive_automation_engine(self, ports):
        """Phase 2: Contextual Decision Matrix for targeted scanning."""
        if not ports:
            self.log("No active ports identified or host is dropping packets.", "ALERT")
            return

        self.log(f"Analysis Map: Found {len(ports)} open vectors {ports}. Routing secondary tools...", "SUCCESS")

        for port in ports:
            print(f"\n--- Pivoting Attack Surface: Port {port} ---")
            
            # Web Server Layer (80/443)
            if port in [80, 443]:
                self.log(f"HTTP/HTTPS daemon detected. Launching Nikto...", "INFO")
                cmd = f"nikto -h http://{self.target}:{port} -Display V -output {os.path.join(self.output_dir, f'web_vulns_{port}.txt')}"
                self.execute_core(cmd, f"nikto_{port}.log")

            # SSH Daemon (22)
            elif port == 22:
                self.log("SSH Endpoint detected. Launching Hydra policy/credential verification...", "INFO")
                cmd = f"hydra -l root -P /usr/share/wordlists/metasploit/unix_passwords.txt ssh://{self.target} -t 4 -o {os.path.join(self.output_dir, 'ssh_brute_results.txt')}"
                self.execute_core(cmd, "hydra_ssh.log")

            # SMB Layer (445)
            elif port == 445:
                self.log("SMB Protocol detected. Provisioning NSE Vulnerability Engine...", "INFO")
                cmd = f"nmap --script smb-vuln* -p 445 -oN {os.path.join(self.output_dir, 'smb_vulnerabilities.txt')} {self.target}"
                self.execute_core(cmd, "nmap_smb.log")

    def generate_remediation_matrix(self, ports):
        """Phase 3: Automated Remediation Report Generation."""
        print("\n" + "="*80)
        self.log("Compiling Defensive Remediation Matrix...", "SUCCESS")
        print("="*80)
        
        remediation_path = os.path.join(self.output_dir, "REMEDIATION_REPORT.md")
        
        markdown_report = f"""# Aegis Security Assessment Report
**Target:** {self.target}  
**Date:** {self.timestamp}  

---

### 1. Executive Summary
An automated contextual vulnerability assessment was executed against the target asset. The following remediation matrix outlines critical actions required to harden identified services.

### 2. Technical Findings & Mitigations
"""
        for port in ports:
            if port in [80, 443]:
                markdown_report += """
#### Port 80/443 - Web Infrastructure
*   **Mitigation:** Deploy a Web Application Firewall (WAF) to filter malicious payloads. Enforce TLS 1.3 and disable insecure HTTP methods. Ensure secure response headers like `Content-Security-Policy` are explicitly configured.
"""
            elif port == 22:
                markdown_report += """
#### Port 22 - Secure Shell (SSH)
*   **Mitigation:** Disable root logins over SSH (`PermitRootLogin no`). Enforce public-key authentication, disable password authentication, and integrate an active rate-limiting daemon like `Fail2Ban`.
"""
            elif port == 445:
                markdown_report += """
#### Port 445 - Server Message Block (SMB)
*   **Mitigation:** Completely deactivate SMBv1 across all system endpoints to protect against known Remote Code Execution (RCE) flaws. Isolate file-sharing protocols within dedicated network segments.
"""

        with open(remediation_path, "w") as f:
            f.write(markdown_report)
            
        print(markdown_report)
        self.log(f"Defensive report saved to: {remediation_path}", "SUCCESS")

    def execute_pipeline(self):
        self.print_banner()
        discovered_ports = self.run_reconnaissance()
        self.adaptive_automation_engine(discovered_ports)
        self.generate_remediation_matrix(discovered_ports)
        print("\n================================================================================")
        self.log("Pipeline run complete. All artifacts successfully archived.", "SUCCESS")
        print("================================================================================")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n\033[91m[!] Error: Target not provided.\033[0m")
        print("Usage: sudo python3 aegis_orchestrator.py <Target IP / Domain>\n")
        sys.exit(1)
        
    engine = AegisOrchestrator(sys.argv[1])
    engine.execute_pipeline()
