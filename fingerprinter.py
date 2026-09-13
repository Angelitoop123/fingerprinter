from colorama import Fore, Style, init
from scapy.all import ARP, Ether, srp
from rich.console import Console
from rich.table import Table

import ipaddress
import nmap
import os
import psutil
import pyfiglet
import socket
import sys
import time

#===========================DECORACIÓN=============================#

table = Table(title="==== ALL RESULTS ====")

console = Console()


def banner() -> None:
    init(autoreset=True)
    BANNER = pyfiglet.figlet_format(text="FINGERPRINTER", font="slant")
    print(Fore.MAGENTA + Style.NORMAL + BANNER)


def table_results(table, data) -> None:
    headers = ("IP ADDRESS", "MAC")
    colors = ["purple"] * 2

    for header, color in zip(headers, colors):
        table.add_column(header=header, style=color)

    for pair in data:
        table.add_row(*map(str, pair))

    console.print(table)


banner()

#=================================================================#

#
#
#
#
#
#
#
#

#==================================== LÓGICA DEL SCRIPT ================================#

def all_networks() -> list:
    networks = []

    for interface, addresses in psutil.net_if_addrs().items():
        for address in addresses:
            if address.family != socket.AF_INET:
                continue
            ip = address.address
            netmask = address.netmask

            if not netmask:
                continue

            try:
                network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
            except ValueError:
                continue

            networks.append({
                "interface": interface,
                "ip": ip,
                "netmask": netmask,
                "network": network
            })

    return networks


networks = all_networks()

print(f'\n{Fore.CYAN}[*]{Fore.WHITE} Looking up for all networks...\n')

time.sleep(3)

if networks:
    print(f'{Fore.CYAN}[*]{Fore.WHITE} Showing all results...\n')

    time.sleep(3)

    for index, net in enumerate(networks, start=1):
        print(f'[{index}] {net["interface"]:<30} | {str(net["network"]):<18}')

    print(f'\n{Fore.CYAN}[*]{Fore.WHITE} Select a network to scan: ')

    network_input = input("").strip()

    try:
        network_index = int(network_input) - 1

        if network_index < 0 or network_index >= len(networks):
            print(f"\n{Fore.RED}[!] Invalid network selection")
            sys.exit()

        selected = networks[network_index]

    except ValueError:
        print(f"\n{Fore.RED}[!] Invalid network selection")
        sys.exit()

else:
    print(f"\n{Fore.RED}[!] No networks found")
    sys.exit()


network = selected["network"]
interface = selected["interface"]

print(f"\n{Fore.GREEN}[+] Selected: {network}")
print(f"{Fore.GREEN}[+] Interface: {interface}\n")


#==================================== NMAP ================================#

try:
    nm = nmap.PortScanner()
except nmap.PortScannerError:
    print(f"\n{Fore.RED}[!] Nmap is not installed or cannot be found")
    sys.exit()


try:
    nm.scan(hosts=str(network), arguments="-sn")
except Exception as e:
    print(f"\n{Fore.RED}[!] Nmap error: {e}")
    sys.exit()


#Hallar los host activos en la red
ALL_HOSTS = nm.all_hosts()


#==================================== HALLAR LA MAC DE CADA HOST ACTIVO ================================#

def get_mac(all_host: list) -> list:
    ip_mac = []

    for ip in all_host:
        try:
            if ipaddress.IPv4Address(ip) not in network:
                continue
            packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op="who-has", pdst=ip)
            resp, _ = srp(packet, iface=interface, timeout=2, retry=2, verbose=False)

            for _, r in resp:
                if r.haslayer(Ether):
                    pair = (ip, r[Ether].src)
                    ip_mac.append(pair)
                    break

        except Exception as e:
            print(f'{Fore.RED}[!] Could not get MAC for {ip}: {e}')

    return ip_mac


#===============================================================================================#

def target_info(target: str, active_hosts: list) -> None:
    try:
        if not target:
            print(f'{Fore.RED}[-] Invalid IP ADDRESS!!\n')
            return

        try:
            target_ip = ipaddress.IPv4Address(target)
        except ValueError:
            print(f'\n{Fore.RED}[-] Invalid IP ADDRESS!!\n')
            return

        if target_ip not in network:
            print(f'\n{Fore.RED}[-] IP ADDRESS is not inside the selected network!!\n')
            return

        try:
            mac_exists = next(pair[1] for pair in active_hosts if pair[0] == target)
        except StopIteration:
            print(f'\n{Fore.RED}[-] Invalid IP ADDRESS!!\n')
            return

        if mac_exists:
            nm.scan(hosts=target, arguments="-sV -O --host-timeout 30s --max-retries 1")
            host_info = nm[target]

            manufacturer = host_info.get("vendor", {})
            ports = host_info.get("tcp", {})
            osmatch = host_info.get("osmatch", [])

            print(f"\n{Fore.GREEN}IP ADDRESS: {target}")
            print(f"{Fore.GREEN}MAC: {mac_exists}")

            if manufacturer:
                print(f"{Fore.GREEN}MANUFACTURER: {manufacturer}")
            else:
                print(f"{Fore.YELLOW}MANUFACTURER: Unknown")

            if osmatch:
                for os in osmatch:
                    print(f'{Fore.GREEN}OS: {os.get("name", "Unknown")}\n')
            else:
                print(f'{Fore.YELLOW}OS: Unknown\n')

            if ports:
                for port in ports:
                    state = ports[port].get("state", "unknown")
                    service = ports[port].get("name", "unknown")

                    print(f'{Fore.GREEN}Port: {port}\n'
                          f'\t| State: {state}\n'
                          f'\t| Service: {service}')
            else:
                print(f'{Fore.RED}[-] No TCP ports found.')

    except KeyboardInterrupt:
        print(f'\n{Fore.RED}[!] Connection interrupted!!')
        sys.exit()

    except nmap.PortScannerError as e:
        print(f'\n{Fore.RED}[!] Nmap error: {e}')

    except Exception as e:
        print(f'\n{Fore.RED}[!] Error: {e}')


#===============================================================================================#

if __name__ == "__main__":
    active_hosts = get_mac(ALL_HOSTS)

    table_results(table, active_hosts)

    print(f'\n{Fore.CYAN}[*]{Fore.WHITE} IP TARGET: ')

    target = input("").strip()

    target_info(target=target, active_hosts=active_hosts)

    os.system("")
