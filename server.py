import socket
import threading



# Color styles
reset 	= "\x1b[0m" # All attributes off(color at startup)

bold 	= "\x1b[1m" # Bold on(enable foreground intensity)
_bold 	= "\x1b[21m" # Bold off(disable foreground intensity)

underline = "\x1b[4m" # Underline on
_underline = "\x1b[24m" # Underline off

blink	= "\x1b[5m" # blink on(enable background intensity)
_blink	= "\x1b[25m" # blink off(disable background intensity)

black 	= "\x1b[30m"
red 	= "\x1b[31m"
green 	= "\x1b[32m" 
yellow 	= "\x1b[33m"
blue 	= "\x1b[34m" 
magenta = "\x1b[35m"
cyan 	= "\x1b[36m" 
white 	= "\x1b[37m" 

light_gray 		= "\x1b[90m"
light_red 		= "\x1b[91m" 
light_green 	= "\x1b[92m" 
light_yellow 	= "\x1b[93m" 
light_blue 		= "\x1b[94m" 
light_megenta 	= "\x1b[95m" 
light_cyan 		= "\x1b[96m" 
light_white 	= "\x1b[97m" 

fg_reset = "\x1b[39m" # Default(foreground color at startup)

black_Bg 	= "\x1b[40m"
red_Bg 		= "\x1b[41m"
green_Bg 	= "\x1b[42m" 
yellow_Bg 	= "\x1b[43m"
blue_Bg 	= "\x1b[44m" 
magenta_Bg 	= "\x1b[45m"
cyan_Bg 	= "\x1b[46m" 
white_Bg 	= "\x1b[47m" 

light_gray_Bg 		= "\x1b[100m"
light_red_Bg 		= "\x1b[101m" 
light_green_Bg 		= "\x1b[102m" 
light_yellow_Bg 	= "\x1b[103m" 
light_blue_Bg 		= "\x1b[104m" 
light_megenta_Bg 	= "\x1b[105m" 
light_cyan_Bg 		= "\x1b[106m" 
light_white_Bg 		= "\x1b[107m" 

resetBg = "\x1b[49m " # Default(foreground color at startup)







# Server IP and Port
SERVER_IP = input(f'{black_Bg+light_yellow}server ip:{fg_reset} ')
SERVER_PORT = int(input(f'{black_Bg+light_yellow}server port:{fg_reset} '))
print(f'\r{reset}')

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and start listening for incoming connections
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

print(f"\n{ black_Bg+light_green }[server]{fg_reset} Running, Waiting for connections...{reset}")


shutdown_event = threading.Event()

clients = [] # (client_socket, client_address)
clients_lock = threading.Lock()




# Broadcast messages to all clients
def broadcast(message, _source, _source_addr):
    with clients_lock:
        for client, addr in clients:
            if client != _source: # Not the one who sent the message
                try:
                    client.send(message)
                except:
                    client.close()
                    clients.remove((client, addr))
                    print(f'\n{black_Bg+light_red}[client] {fg_reset}{client_address[0]}:{client_address[1]} disconnected {reset}')


# Handle clients' connections
def client_handler(client_socket, client_address):
    while not shutdown_event.is_set():
        try:
            message = client_socket.recv(1024)

            if not message:
                raise
            broadcast(message, client_socket, client_address)

        except:
            try:
                with clients_lock:
                    clients.remove((client_socket, client_address))
                client_socket.close()
            except:
                break
            print(f'\n{black_Bg+light_red}[client] {fg_reset}{client_address[0]}:{client_address[1]} disconnected {reset}')
            break



# Server command system
def command():
    while True:
        cmd = input()

        # Quit
        if cmd == '/q':
            with clients_lock:
                for client, addr in clients:
                    client.close()
            shutdown_event.set()
            server_socket.close()
            break

        # Show clients
        elif cmd == '/c': 
            print(f'\n\n{black_Bg+white}****** clients ******{reset}\n')

            for client, addr in clients:
                print(f'  {black_Bg+light_blue}[{addr[0]}] {addr[1]}{reset}' )
                
            print(f'\n{black_Bg+white}*********************{reset}\n')

        # Help
        elif cmd == '/h':
            print('\nServer commands:')
            print('/h -- Show this help message')
            print('/q -- Shut down the server')
            print('/c -- List all connected clients\n')

# Execute command access
thread_cmd = threading.Thread(target=command)
thread_cmd.start()



# Accept multiple clients using threading
Client_threads=[]
while not shutdown_event.is_set():
    try:
        # Get new connection
        client_socket, client_address = server_socket.accept()
        with clients_lock:
            clients.append((client_socket, client_address))

        print(f"\n{ black_Bg+light_blue }[client]{fg_reset}" +
            f" New connection from " +
            f"{client_address[0]}:{client_address[1]}" +
            f"{reset}")

        # Client handler
        thread = threading.Thread(target=client_handler, args=(client_socket, client_address))
        thread.start()
        Client_threads.append(thread)
    except:
        pass


for thread in Client_threads:
    thread.join()

print(f'{light_red}\nServer has been shut down.{reset}')
print(f'{light_red}Good luck :){reset}')