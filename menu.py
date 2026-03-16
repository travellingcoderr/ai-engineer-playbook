#!/usr/bin/env python3
import os
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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    options = [
        ("Start RAG System (Docker)", "make run-docker-rag"),
        ("Stop RAG System (Docker)", "make stop-docker-rag"),
        ("Start Research Agent (Docker)", "make run-docker-research"),
        ("Stop Research Agent (Docker)", "make stop-docker-research"),
        ("Start Multi-Agent Team (Docker)", "make run-docker-multi-agent"),
        ("Stop Multi-Agent Team (Docker)", "make stop-docker-multi-agent"),
        ("Start MCP Gateway (Local)", "make run-gateway"),
        ("Start Observability (Local)", "make run-observe"),
        ("Stop All Services", "make stop-all"),
        ("Kill All Stray Ports", "make kill-all"),
        ("Exit", "exit"),
    ]
    
    while True:
        clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}================================================={Colors.ENDC}")
        print(f"{Colors.OKCYAN}{Colors.BOLD}   🤖 AI Engineer Playbook - Command Menu 🤖   {Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}================================================={Colors.ENDC}\n")
        
        for i, (label, cmd) in enumerate(options, 1):
            if label == "Exit":
                print(f" {Colors.FAIL}[{i}]{Colors.ENDC} {label}")
            elif "Start" in label:
                print(f" {Colors.OKGREEN}[{i}]{Colors.ENDC} {label:<35}")
            elif "Stop" in label or "Kill" in label:
                print(f" {Colors.WARNING}[{i}]{Colors.ENDC} {label:<35}")
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
