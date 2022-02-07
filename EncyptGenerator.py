import random as ran
import getpass
import random
from math import gcd
import math
 

alpha = "4W[rYZK’.vyenqmAVh8f3Mx+7lB2^uzdkG~(:d>Q“_60acEPR/p\9L]j1|D{<C)*I&@=Xb;J?Ft-Nwo%gU!T#5ic`S}$sOH" #Encryption Table
brute_counter = n = phi  = e = d = 0

try:
   input = raw_input
except NameError:
   pass

try:
   chr = unichr
except NameError:
   pass

#------------------------------------------- Function Zone -----------------------------------------------------
def PrimeGenerator():       #Generate Prime Number
    x = True
    while(x):
        ran = random.randint(100,1000)
        flag = True
        if ran > 1:
            for i in range(2,ran):
                if (ran % i == 0):
                    flag = False
        if flag:
            x = False
            return ran

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

def coprimes(a):            #Searching E
    l = []
    for x in range(2, a):
        if gcd(a, x) == 1 and modinv(x,phi) != None:
            l.append(x)
    for x in l:
        if x == modinv(x,phi):
            l.remove(x)
    return l

def encrypt_block(m):
    c = modinv(m**e, n)
    if c == None:
        print('No modular multiplicative inverse for block ' + str(m) + '.')
    return c

def encrypt_string(s):
    val = encrypt_block(ord(s))
    part = ""
    for p in str(val):
        part += alpha[int(p)]

    part += ","
    return part

def encrypt(msg):
    enc = ""
    for c in msg:
        enc += encrypt_string(c)
    return enc


def ranNum():
    loop = True
    while(loop):
        num = ran.randint(100,999)
        if num % 2 == 0:
            loop = False
    return num

# --------------------------------- Make a connection with Server.py -------------------------------------------

 
username = input(" Username : ")
password = input(" Password : ") 

#Encryption
p = PrimeGenerator() 
q = PrimeGenerator()

ch = True
while ch:               # Check If value P equal to Q. Both value can not be same
    if q == p :
        q = PrimeGenerator()
    else:
        ch = False 

print ("\n P: " + str(p))
print (" Q: " + str(q))

n = p * q
print (" N: " + str(n))

phi = (p-1) * (q-1)
print (" PHI: " + str(phi))

a = coprimes(phi)
e = random.choice(a) 
print ("\n Public Key: " + str(e))

d = modinv(e,phi)
print (" Private Key: " + str(d))
# Encypting Process
    
user = encrypt(username)
sec = encrypt(password)
    
flag = ranNum()
print (" Flag Number : " + str(flag))

login = str(user) +"#"+ str(sec)+ str(flag)  +"<" + str(n) + ">" + str(d)    
print (" Encrypt Before Shifting: " + str(login))

shift = 5
new_ind = 0
shiflog = ""

# Shifting 
for i in login:
    if i in alpha:
        new_ind = alpha.index(i) + shift 
        calc = new_ind % 94 
        shiflog += alpha[calc] 
    else:
        shiflog += i 
    
print(" Encrypt After shifting: " + str(shiflog))

