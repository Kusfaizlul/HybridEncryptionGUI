import socket
import math
import errno
import sys
from multiprocessing import Process
  
alpha = "4W[rYZK’.vyenqmAVh8f3Mx+7lB2^uzdkG~(:d>Q“_60acEPR/p\9L]j1|D{<C)*I&@=Xb;J?Ft-Nwo%gU!T#5ic`S}$sOH" #Encryption Table

try:
   input = raw_input
except NameError:
   pass

try:
   chr = unichr
except NameError:
   pass


#-------------------------------------- Function Zone --------------------------------------------------------

def egcd(a, b):             #Greatest common divisor
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):           #Multiplicative Inverse
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def decrypt_block(c,d,n):
    m = modinv(c**int(d), int(n))
    if m == None:
        print('No modular multiplicative inverse for block ' + str(c) + '.')
    return m

def decrypt_string(v,d,n):
    Pro = ""
    for x in v:
        Pro += chr(decrypt_block((ord(x)),d,n))
    return Pro

def decrypt(enc,d,n):
    temp = dec = t = ""
    for y in enc:
        if y != ",":
            temp += str(alpha.index(y))
        else:
            t += chr(int(temp))
            temp = ""

    dec = decrypt_string(t,d,n)
    return dec

def readfiles():
    f = open("Database.txt","r")
    return f

def deshifting(cipher):
    decip =""
    new_ind = 0
    for i in cipher:
        if i in alpha:
            new_ind = alpha.index(i) - 5
            decip += alpha[new_ind % 95]
        else:
            decip += i
    
    return decip

def gettheflag(me):
    tmp = ""
    i = 0

    while i<3:
        j = -3 + i
        tmp += me[j]
        i += 1

    return tmp #    kena buat flag checker

def removeflag(data):
    flg = gettheflag(data)
    
    for chc in flg:
        data = data.replace(chc,"")

    return data



#--------------------------------------- Main Function -------------------------------------------------------

def ProcessStart(server):
    new = 0
    result = 1
    loop = True

    if result == 1:
        while loop:             
            if new == 0:                        # Only Run for the first time to open file        
            
                data = readfiles()              # Open files
        
                username = []
                password = []
        
                for x in data:

                    user = x                    # Get data on files
                    deuser = deshifting(user)   # Deshifting
            
                    Dt = Nt = spuser = scrt = ""
                    fl = sub = 0
            
                    #   Spliting E and PHI value
                    for x in deuser:
                        if x == "<" or fl == 1:
                            fl = 1

                            if x == ">" or sub == 1:
                                sub = 1
                                if x.isnumeric():
                                    Dt += x

                            elif sub == 0:
                                if x.isnumeric():
                                    Nt += x
                        else:
                            spuser += x         # spuser == split user
            
                    cipher = removeflag(spuser)
  
                    pswrd = 0
                    spuser = ""
            
                    # Spliting Username and Password
                    for x in cipher:
                        if x == "#":
                            pswrd = 1
                    
                        elif pswrd == 1:
                            scrt += x
                
                        else:
                            spuser += x

                    n = int(Nt)
                    d = int(Dt)
            
                    # Decrypting
                    username.append(decrypt(spuser,d,n))
                    password.append(decrypt(scrt,d,n))
                
                    new = 1                     # Updating to make sure run once only
                    #data.close()
            print ("--- THE SERVER IS READY ---")

            wspc = "whitespace"
             
            bf = int(server.recv(1024).decode())
            if bf == 9999:
                print ("The Client Were Forcely Quit Due to Brute Force !")
                server.send(wspc.encode())
                return
            else:
                server.send(wspc.encode())

            sq = server.recv(1024).decode()
            if int(sq) == 9999:
                print ("The Client Were Forcely Quit Due to SQL Injection !")
                return
            else:
                server.send(wspc.encode())

            #    Get from Client.py   
            UsCl = server.recv(1024).decode()

            #    decrypt tuk client
            reuser = deshifting(UsCl)
        
            #    Split login and password then decyrpt 
            du = nu = cpuser = scrt = cpass = nmu =""
            fl = sub = passs = 0

            for x in reuser:
                if x == "<" or fl == 1:
                    fl=1
                    if x == ">" or sub == 1:
                        sub = 1
                        if x.isnumeric():
                            du += x
                    elif sub == 0:
                        if x.isnumeric():
                            nu += x
                else:
                    cpuser += x

            for x in cpuser:
                if x == "#":
                    passs = 1
                elif passs == 1:
                    scrt += x
                else:
                    nmu += x

            d = int(du)
            n = int(nu)

            cpuser = decrypt(nmu,d,n)
            cpass = decrypt(scrt,d,n)

            for i in range(len(username)):
                if cpuser == username[i] and cpass == password[i]:
                    result = 2 #"Succesfully logged in !"
                    loop = False
                    print ("IP " + str(addr) + " Successfull Logged In. Welcome " + cpuser)
                else:
                    result = 1#"Invalid credential please try again !"

            #    Result
            server.send(str(result).encode())
            print("\n\n")
    
    elif result == 2:
        print ("IP " + str(addr) + " Successfull Logged In. Welcome")


#--------------------------------------- Server Zone -----------------------------------------------------------

if __name__ == '__main__':

    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ''
    port = 4848
    
    #   Binding with port and ip

    try:
        S.bind((host, port))
    except socket.error as e:
        print(str(e))
        sys.exit()
    
    #   Open 5 connection to listen
    
    S.listen(5)
    
    while True:
        try:
            server, addr = S.accept()
            print('Sucessfully Connected !! ')

            p = Process(target=ProcessStart, args=(server,))
            p.start()

        except socket.error:
            print('an exception occurred!')

    S.close()
