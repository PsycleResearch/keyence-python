import socket                
  
s = socket.socket()          
s.connect(('192.168.0.100', 9004)) 
s.settimeout(1000)
s.send(b"LON\r")

print(s.recv(1024).decode('utf-8'))
s.close()
