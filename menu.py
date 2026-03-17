#!/usr/bin/env python3
import os
import socket
import subprocess
import sys

# ANSI color codes for aesthetics
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.1)
        return s.connect_ex(('127.0.0.1', port)) == 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Service port mapping for status checks
    services = {
        "RAG System": 8000,
        "MCP Gateway": 8001,
        "Observability": 8002,
        "Research Agent": 8003,
        "Multi-Agent": 8004,
        "Guardrails": 8005,
        "Resilient Gateway": 8006,
        "n8n Workflow": 5678,
        "Dashboard": 8080
    }

    options = [
        ("Start RAG System (Docker)", "make run-docker-rag", "RAG System"),
        ("Stop RAG System (Docker)", "make stop-docker-rag", "RAG System"),
        ("Start MCP Gateway (Docker)", "make run-docker-gateway", "MCP Gateway"),
        ("Stop MCP Gateway (Docker)", "make stop-docker-gateway", "MCP Gateway"),
        ("Start Research Agent (Docker)", "make run-docker-research", "Research Agent"),
        ("Stop Research Agent (Docker)", "make stop-docker-research", "Research Agent"),
        ("Start Multi-Agent Team (Docker)", "make run-docker-multi-agent", "Multi-Agent"),
        ("Stop Multi-Agent Team (Docker)", "make stop-docker-multi-agent", "Multi-Agent"),
        ("Start Guardrails (Docker)", "make run-docker-guardrails", "Guardrails"),
        ("Stop Guardrails (Docker)", "make stop-docker-guardrails", "Guardrails"),
        ("Start Resilient Gateway (Docker)", "make run-docker-resilient-gateway", "Resilient Gateway"),
        ("Stop Resilient Gateway (Docker)", "make stop-docker-resilient-gateway", "Resilient Gateway"),
        ("Start n8n (Docker)", "make run-n8n", "n8n Workflow"),
        ("Stop n8n (Docker)", "make stop-n8n", "n8n Workflow"),
        ("Start Observability (Docker)", "make run-docker-observe", "Observability"),
        ("Stop Observability (Docker)", "make stop-docker-observe", "Observability"),
        ("View Observability Logs (Live)", "make tail-observe-logs", "Observability"),
        ("Stop All Services", "make stop-all", None),
        ("Kill All Stray Ports", "make kill-all", None),
        ("Exit", "exit", None),
    ]
    
    while True:
        clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}================================================={Colors.ENDC}")
        print(f"{Colors.OKCYAN}{Colors.BOLD}   🤖 AI Engineer Playbook - Command Menu 🤖   {Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}================================================={Colors.ENDC}\n")
        
        # Determine status of each unique service
        status_map = {}
        for name, port in services.items():
            status_map[name] = is_port_open(port)

        for i, (label, cmd, service_name) in enumerate(options, 1):
            status_indicator = ""
            if service_name and service_name in status_map:
                is_running = status_map[service_name]
                service_port = services.get(service_name, "???")
                if is_running:
                    status_indicator = f"{Colors.OKGREEN}[{service_port}]-[RUNNING]{Colors.ENDC}"
                else:
                    status_indicator = f"{Colors.GRAY}[{service_port}]-[OFF]{Colors.ENDC}"

            if label == "Exit":
                print(f" {Colors.FAIL}[{i}]{Colors.ENDC} {label}")
            elif "Start" in label:
                print(f" {Colors.OKGREEN}[{i}]{Colors.ENDC} {label:<35} {status_indicator}")
            elif "Stop" in label or "Kill" in label:
                print(f" {Colors.WARNING}[{i}]{Colors.ENDC} {label:<35} {status_indicator}")
            else:
                print(f" {Colors.OKBLUE}[{i}]{Colors.ENDC} {label:<35}")
            
        print(f"\n{Colors.HEADER}{Colors.BOLD}================================================={Colors.ENDC}")
        
        try:
            choice_str = input(f"\n{Colors.BOLD}Enter a number to execute (1-{len(options)}): {Colors.ENDC}")
            choice_idx = int(choice_str) - 1
            
            if not (0 <= choice_idx < len(options)):
                input(f"\n{Colors.FAIL}Invalid option. Press Enter to try again.{Colors.ENDC}")
                continue

            cmd = options[choice_idx][1]
            if cmd == "exit":
                clear_screen()
                print(f"{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
                sys.exit(0)

            print(f"\n{Colors.OKBLUE}🚀 Executing: {choice_str}: {cmd}{Colors.ENDC}\n")

            # Execute the command natively, streaming output to the terminal!
            subprocess.run(cmd, shell=True)

            input(f"\n{Colors.BOLD}Press Enter to return to menu...{Colors.ENDC}")
        except ValueError:
            input(f"\n{Colors.FAIL}Please enter a valid number. Press Enter to try again.{Colors.ENDC}")
        except KeyboardInterrupt:
            clear_screen()
            print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
            sys.exit(0)

if __name__ == "__main__":
    main()
