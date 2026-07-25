import os
import time
import subprocess
import socket
from colorama import Fore, init

init(autoreset=True)

C = Fore.CYAN
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
W = Fore.WHITE
R = Fore.RED


def run(cmd):
    try:
        return subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.DEVNULL
        ).decode(errors="ignore")

    except:
        return ""


def clear():
    os.system("clear")


def banner():
    print(
        M + """
╔══════════════════════════════════════╗
║                                      ║
║        👑 ARIF WIFI TOOL 👑          ║
║                                      ║
╚══════════════════════════════════════╝
"""
    )


def get_ip():

    data = run("ip -4 addr show wlan0")

    for line in data.splitlines():

        if "inet " in line:
            return line.split()[1].split("/")[0]

    return "Unknown"


def get_gateway():

    data = run("ip route")

    for line in data.splitlines():

        if "default" in line:
            return line.split()[2]

    ip = get_ip()

    if ip != "Unknown":
        return ip.rsplit(".", 1)[0] + ".1"

    return "Unknown"


def get_mac(ip):

    data = run("ip neigh")

    for line in data.splitlines():

        parts = line.split()

        if len(parts) >= 5:

            if parts[0] == ip and "lladdr" in parts:

                index = parts.index("lladdr")

                return parts[index + 1]

    return "Not Found"


def hostname_lookup(ip):

    try:
        return socket.gethostbyaddr(ip)[0]

    except:
        return ""

def mac_vendor(mac):

    if mac == "Not Found":
        return "Unknown"

    try:

        result = subprocess.check_output(
            ["curl", "-s", f"https://api.macvendors.com/{mac}"],
            timeout=5
        ).decode().strip()

        if result == "":
            return "Unknown"

        return result

    except:

        return "Unknown"



def device_name(ip):

    if ip.endswith(".1"):
        return "Router"

    if ip == get_ip():
        return "My Device"

    name = hostname_lookup(ip)

    if name:
        return name

    return "Unknown Device"



def device_scan():

    devices = []

    ip = get_ip()

    if ip == "Unknown":
        return devices


    network = ip.rsplit(".", 1)[0] + ".0/24"


    result = run(
        f"nmap -sn {network}"
    )


    for line in result.splitlines():

        if "Nmap scan report for" in line:

            found_ip = line.split()[-1]

            mac = get_mac(found_ip)

            vendor = "Unknown"


            if not found_ip.endswith(".1"):

                vendor = mac_vendor(mac)


            devices.append({

                "name": device_name(found_ip),
                "ip": found_ip,
                "mac": mac,
                "vendor": vendor

            })


    return devices



def show_devices(devices):

    print(
        C + "\n📱 DEVICE LIST"
    )

    print(
        M + "━━━━━━━━━━━━━━━━━━━━"
    )


    count = 1


    for dev in devices:

        print(
            Y + f"\n{count}) 📱 {dev['name']}"
        )


        print(
            W + "   IP    : " +
            G + dev["ip"]
        )


        print(
            W + "   MAC   : " +
            C + dev["mac"]
        )


        print(
            W + "   Brand : " +
            G + dev["vendor"]
        )


        print(
            M + "━━━━━━━━━━━━━━━━━━━━"
        )


        count += 1

def wifi_info():

    print(
        B + "\n╭──────── 📶 WIFI INFORMATION ────────╮"
    )

    print(
        Y + "│ WiFi Name : " +
        W + "Connected WiFi"
    )

    print(
        Y + "│ IP        : " +
        G + get_ip()
    )

    print(
        Y + "│ Gateway   : " +
        C + get_gateway()
    )

    print(
        B + "╰────────────────────────────────────╯"
    )



def new_device_alert():

    print(
        G + "\n🚨 New Device Alert : Normal"
    )



def main():

    while True:

        #clear()

        banner()

        wifi_info()

        devices = device_scan()

        show_devices(devices)

        new_device_alert()


        print(
            M + "\n🔄 Auto Refresh : " +
            G + "ON"
        )


        for i in range(5, 0, -1):

            print(
                Y + f"⏳ Refresh In : {i}s",
                end="\r"
            )

            time.sleep(1)
            
            
            clear()


if __name__ == "__main__":

    main()

