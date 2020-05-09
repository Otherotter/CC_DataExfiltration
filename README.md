# covert-exfiltrating-channel
## Test Server
    python3 Main.py [-p : required] [-h : optional]
          -p  --> change port
          -h  --> change localhost
          
    example: 
        python3 Main.py -p 2000


## Test Client
    python3 Client.py [-p : required] [-h : optional]
             -p  --> change port
              -h  --> change localhost
              
    example: 
        python3 Client.py -p 2000
      
  
         
## COMMAND CENTER
    COMMANDS:
       [ACCESS <password> : escalate privilage]
       [CLIENTS : print clients] 
       [COMMAND <IP> <OPTION> <(optional)> : command client]
       [DROP : drop privilage]
           <IP> : Type in client's IP to send to specific client. ALL to send to all clients
           <OPTION>: [echo] [send] [disconnect]
           
    example:
        //While in the client
        ACCESS PASSWORD
        CLIENTS
        COMMAND ALL ECHO
        COMMAND ALL SEND
        COMMAND ALL DISCONNECT
        COMMAND 127.0.0.1 ECHO
        COMMAND 127.0.0.1 SEND
        COMMAND 127.0.0.1 DISCONNECT
        DROP
        
        
        
        
