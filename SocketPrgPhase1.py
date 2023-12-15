import socket
import re

#128.119.245.12

# Regular Expression Pattern to recognise ip_add_entered addresses.
ip_add_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
# Regular Expression Pattern to extract the number of ports you want to scan. 
# You have to specify <lowest_port_number>-<highest_port_number> (ex 10-100)
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")

port_min = 0
port_max = 65535
open_ports = []

print("\n****************************************************************")
print(r"""
                   _______                               
            /\     |     |  |\        /|    /\    |\    |
           /  \    |_____|  | \      / |   /  \   | \   |
          /____\   |    \   |  \    /  |  /____\  |  \  |
         /	\  |     \  |   \  /   | /      \ |   \ |
        /        \ |      \ |    \/    |/        \|    \|
""")
print("\n****************************************************************")

#function for scanning host state
def Check_Host():
    while True:
        ip_add_entered = input("\nPlease enter the ip address that you want to scan: ")
        if ip_add_pattern.search(ip_add_entered):
            break
        else:
            print(f"{ip_add_entered} is not a valid ip address")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((ip_add_entered, 80))

        if result == 0:
            print(f"Host {ip_add_entered} is online")
            try:
                HostName = socket.gethostbyaddr(ip_add_entered)[0]
                print("Host Name: %s" %HostName)
            except:
                pass
        else:
            print(f"Host {ip_add_entered} is offline")
    except:
        print("Error accurred while checking host status")
    s.close()
# Function for scanning ports
def Scan_Ports():
    global open_ports
    # Ask user to input the ip address they want to scan.
    while True:
        ip_add_entered = input("\nPlease enter the ip address that you want to scan: ")
        if ip_add_pattern.search(ip_add_entered):
            break
        else:
            print(f"{ip_add_entered} is not a valid ip address")
    while True:
        print("Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
        port_range = input("Enter port range: ")
        port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
        if port_range_valid:
            port_min = int(port_range_valid.group(1))
            port_max = int(port_range_valid.group(2))
            break
    # Create a socket object
    print(f"Scanning ports {port_min} to {port_max} on host {ip_add_entered}...\n")

    for port in range(port_min, port_max + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_add_entered, port))
            #the port won't be appended to the open ports list if connection was not successful
            open_ports.append(port)
        except:
            pass
    s.close()
    for port in open_ports:
        try:
            serviceName = socket.getservbyport(port, 'tcp')
            print(f"--Port {port} is open --Servise: {serviceName}")
        except:
            try:
                ServName = socket.getservbyport(port, 'udp')
                print(f"--Port {port} is open --Servise: {serviceName}")
            except:
                print(f"--Port {port} is open --Servise: Unknown")

def get_post():
    


def Run_order(argument):
    match argument:
        case 1:
            Check_Host()
        case 2:
            Scan_Ports()
        case 3:
            get_post()
        case default:
            print("Wrong Order Code! Try again: \n")
            Get_order()

def Get_order():
    print("Want You Want to Do? \n 1) Check Host State \n 2) Check Open Ports and Processes on Host"
      ,"\n 3) Get and  Post Method Simulation \n Enter Your Order Code: ")
    Ordr = int(input())
    Run_order(Ordr)

Get_order()