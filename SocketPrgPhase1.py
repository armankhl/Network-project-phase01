import socket
import re

#an Example IP for you: 128.119.245.12

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
# sending client request to local host while. 
# warnning: This module only works when server.py is running on local host
def send_request(request, HOST, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            client_socket.sendall(request.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f'Response from server: {response}')        
# HTTP request simulation with local host
def get_post():
    HOST = 'localhost'
    PORT = 8080
    while True:
        Order = input("Enter Your Request in format: <GET user_id> or <POST user_name user_age>: \n (Enter 0 to Exit)\n")

        if Order == '0':
            break

        # GET Request
        request = Order.split()
        if request[0] == "GET":
            send_request(Order, HOST, PORT)

        # POST Request
        elif request[0] == "POST":
            send_request(Order, HOST, PORT)

        else:
            print("Invalid request try again")
# User guid
def ask_countinue():
    argument = int(input("Do want to countinue? (Enter-> 1 to continue or 0 to exit): "))
    match argument:
        case 1:
            Get_order()
        case 0:
            exit()
        case default:
            print("Wrong Order Code! Try again: \n")
            ask_countinue()
# execute user order
def Run_order(argument):
    match argument:
        case 1:
            Check_Host()
            ask_countinue()
        case 2:
            Scan_Ports()
            ask_countinue()
        case 3:
            get_post()
            ask_countinue()
        case 4:
            exit()
        case default:
            print("Wrong Order Code! Try again: \n")
            Get_order()
#get user order
def Get_order():
    print("Want You Want to Do? \n 1) Check Host State \n 2) Check Open Ports and Processes on Host"
      ,"\n 3) HTTP Request Simulation \n 4) Exit \n Enter Your Order Code: ")
    Ordr = int(input())
    Run_order(Ordr)

if __name__ == '__main__':
    Get_order()
