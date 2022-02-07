import math


alpha = "4W[rYZK’.vyenqmAVh8f3Mx+7lB2^uzdkG~(:d>Q“_60acEPR/p\9L]j1|D{<C)*I&@=Xb;J?Ft-Nwo%gU!T#5ic`S}$sOH"


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

    return tmp 

def removeflag(data):
    flg = gettheflag(data)
    
    for chc in flg:
        data = data.replace(chc,"")

    return data

if __name__ == "__main__":

    user = input("Insert Encrypted Data : ")

    deuser = deshifting(user)   

    Dt = Nt = spuser = scrt = ""
    fl = sub = 0

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
            spuser += x         
    
    print (" Before Flag Remove: " + str(spuser))
    cipher = removeflag(spuser)
    print (" After Flag Remove: " + str(cipher))

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

    print (" N: " + str(n) + "\n D: " + str(d))

    username = decrypt(spuser,d,n)
    password = decrypt(scrt,d,n)

    print (" Username : " + str(username)) 
    print (" Password : " + str(password))

