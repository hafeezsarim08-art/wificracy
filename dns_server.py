#!/usr/bin/env python3
import socket
import threading

class WificracyDNSServer:
    def __init__(self, listen_ip="0.0.0.0", target_ip="10.0.0.1", port=53):
        self.listen_ip = listen_ip
        self.target_ip = target_ip  
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def forge_dns_response(self, data):
        Transaction_ID = data[0:2]
        Flags = b'\x81\x80'
        Questions = data[4:6]
        Answer_RRs = b'\x00\x01'
        Authority_RRs = b'\x00\x00'
        Additional_RRs = b'\x00\x00'
        
        Query = b''
        offset = 12
        while True:
            length = data[offset]
            Query += data[offset:offset + length + 1]
            offset += length + 1
            if length == 0:
                break
        
        Query += data[offset:offset + 4]
        Response_Name = b'\xc0\x0c'
        Response_Type = b'\x00\x01'   
        Response_Class = b'\x00\x01'  
        Response_TTL = b'\x00\x00\x00\x3c' 
        Response_Len = b'\x00\x04'   
        Response_IP = bytes(int(x) for x in self.target_ip.split('.'))
        
        return (Transaction_ID + Flags + Questions + Answer_RRs + 
                Authority_RRs + Additional_RRs + Query + Response_Name + 
                Response_Type + Response_Class + Response_TTL + 
                Response_Len + Response_IP)

    def process_request(self, data, addr):
        try:
            self.server_socket.sendto(self.forge_dns_response(data), addr)
        except Exception:
            pass

    def start(self):
        try:
            self.server_socket.bind((self.listen_ip, self.port))
            print("[+] Autonomous DNS core engine initializing on UDP port 53...")
        except PermissionError:
            print("[-] DNS Error: Root execution privileges required (sudo) for Port 53.")
            return

        while True:
            try:
                data, addr = self.server_socket.recvfrom(1024)
                threading.Thread(target=self.process_request, args=(data, addr), daemon=True).start()
            except (KeyboardInterrupt, SystemExit):
                break
            except Exception:
                pass
        self.server_socket.close()

if __name__ == "__main__":
    server = WificracyDNSServer()
    server.start()
  
