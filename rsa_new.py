
from PrimeGenerator import *

def gcd(a, b):
    if a%b == 0:
        return b
    return gcd(b, a%b)

def MI(num, mod):
	x, xold = 0, 1
	y, yold = 1, 0
	store = mod

	while mod:
		q = num//mod
		num, mod = mod, num % mod
		x, xold = xold - q*x, x
		y, yold = yold - q*y, y

	if num != 1:
		print('No MI, gcd is ' + str(num))
	else:
		MI = xold
		if MI < 0:
			MI = MI + store
		return MI


def gethex(C, blocksize):
	b = bin(C)[2:].zfill(blocksize)
	c = ''
	counter = 0
	while True:
		block = b[counter:(counter+8)]
		c += hex(int(block, 2))[2:].zfill(2)
		counter += 8
		if counter == blocksize:
			break
	return c

def crt(a,b,n):
    crt_c_c = 0
    crt_f_c = 1

    crt_b_bin_c = bin(b)[2:]

    for crt_i_c in crt_b_bin_c:
        crt_c_c = crt_c_c * 2
        crt_f_c = (crt_f_c*crt_f_c) % n

        if crt_i_c == "1" :
            crt_c_c = crt_c_c + 1
            crt_f_c = (crt_f_c*a) % n
    return crt_f


n_rsa = 256
blockSize = 128
numBytes = blockSize // 8
e = 65537

check_last_block = 0
padding_byte = "0"*numBytes
padding = ''
print("padding : "+padding_byte)
for pad in padding_byte:
    #print("pad count : "+str(pad))
    int_pad = ord(pad)
    #print("pad int : "+str(int_pad))
    bin_pad = bin(int_pad)[2:].zfill(8)
    #print("pad bin : "+str(bin_pad))
    padding = padding + bin_pad
    #print("pad size : "+str(padding))

pad_length = len(padding)
print("pad length : "+str(pad_length))

primeNumGenerate = PrimeGenerator ( bits = n_rsa // 2)

check = 0
while(check == 0):
    p = primeNumGenerate.findPrime()
    q = primeNumGenerate.findPrime()

    while ( p == q ):
        p = primeNumGenerate.findPrime()
        q = primeNumGenerate.findPrime()

    print("p : "+str(p))
    print("q : "+str(q))

    n = p*q
    print("n : "+str(n))

    totient = (p-1)*(q-1)
    print("totient : "+str(totient))

    #x = gcd(11, 10800)
    #print("x : "+str(x))

    x = gcd(totient, e)
    print("gcd : "+str(x))
    check = 1

d = MI(e, totient)
print("d : "+str(d))

print("Public Key : PU = (e, n) : "+str(e)+" , "+str(n))
print("Private Key : PR = (d, n) : "+str(d)+" , "+str(n))

inputFile = open("inNew.txt","r")
outputFile = open("outNew.txt","w")

#ENCRYPTION PART
msg = inputFile.read()
print(msg)

length = len(msg)
print("msg length : "+str(length))
# 128 bit = 16 byte; msg w byte e thake so, byte diye devide hobe
if ( (length % numBytes) != 0 ):
    check_last_block = 1
    remaining = numBytes - (length % numBytes)
    msg = msg + remaining * "0"
    print("remaining size : "+str(remaining))

temp = ""
cipher = ""
for ch in msg:
    int_ch = ord(ch)
    bin_ch = bin(int_ch)[2:].zfill(8)
    temp = temp + bin_ch
    temp_length = len(temp)
    #check for 256 bit 
    #if (temp_length == 128):
    if (temp_length == blockSize):
        temp = padding + temp
        int_temp = int(temp,2)
        print("int_temp value : "+str(int_temp))
        #encrypt messange using public key
        #enctyptMsg = pow(int_temp, e, n)


        #Try CRT for encryption
        #d_new = d % (p-1)
        #Vp = pow (ch_int,d_new, p)
        #Vq = pow ()

        # a = int_temp
        # b = e
        # n = n
        
        crt_c = 0
        crt_f = 1

        crt_b_bin = bin(e)[2:]

        for crt_i in crt_b_bin:
            crt_c = crt_c * 2
            crt_f = (crt_f*crt_f) % n

            if crt_i == "1" :
                crt_c = crt_c + 1
                crt_f = (crt_f*int_temp) % n
        xx = crt_f
        print("xx : "+str(xx))

        #crt complete
        enctyptMsg = crt_f
        
        #256 implement
        #hexMsg = gethex(enctyptMsg, blockSize)
        hexMsg = gethex(enctyptMsg, n_rsa)
        cipher = cipher + hexMsg
        temp =""
        
print("cipher msg : "+cipher)
outputFile.write(cipher)
outputFile.close()

#DECRYPTION PART
inputCipher = open("outNew.txt","r")
decryptMsg =""
decryptMsgRemovePadding = ""

while (True):
    #check for 256 bit 
    #ch = inputCipher.read(32)

    #256 implement
    #count = blockSize // 4
    count = n_rsa // 4
    ch = inputCipher.read(count)
    if (ch == ''):
        break
    #calculate int value from hex-cipher
    b = ""
    length_int = len(ch) // 2
    for i in range(length_int):
        hexVal_ci = ch[2*i] + ch[2*i+1]
        hexVal_int = int (hexVal_ci, 16)
        hexVal_bin = bin(hexVal_int)[2:].zfill(8)
        b = b + hexVal_bin
    
    ch_int = int(b,2)
    #decrypt messange using private key
    #de_msg_int = pow(ch_int, d, n)

    #print("xxPOW : "+str(de_msg_int))
    
    #Try CRT for decryption
    

    crt_c = 0
    crt_f = 1

    crt_b_bin = bin(d)[2:]
    crt_length = len(crt_b_bin)

    for crt_i in crt_b_bin:
        crt_c = crt_c * 2
        crt_f = (crt_f*crt_f) % n

        if crt_i == "1" :
            crt_c = crt_c + 1
            crt_f = (crt_f*ch_int) % n
    xx = crt_f
    print("xx : "+str(xx))

    #crt complete

    de_msg_int = crt_f

    # CRT USING EQUATION
    d_new_p = d % (p-1)
    Vp = crt (ch_int,d_new_p, p)
    d_new_q = d % (q-1)
    Vq = crt (ch_int,d_new_q,q)

    mulInv_q = MI(q,p)
    Xp = q * mulInv_q
    mulInv_p = MI(p,q)
    Xq = p * mulInv_p

    M_crt = ((Vp*Xp)+(Vq*Xq)) % n
    print("M_CRT : "+str(M_crt))

    # end using eq
    
    de_msg_int = M_crt
    
    de_msg =""
    de_msg_pad = ""
    #256 implement
    #b_msg = bin(de_msg_int)[2:].zfill(blockSize)
    b_msg = bin(de_msg_int)[2:].zfill(n_rsa)
    #256 implement
    #for i in range(numBytes):
    for i in range((n_rsa // 8)):
        de_bin = b_msg[i*8: (i+1)*8]
        de_int = int (de_bin,2)
        de_msg = de_msg + chr(de_int)
        if (i>=numBytes):
            de_bin_pad = b_msg[i*8: (i+1)*8]
            de_int_pad = int (de_bin_pad,2)
            de_msg_pad = de_msg_pad + chr(de_int_pad)
    
    
    decryptMsg = decryptMsg + de_msg
    decryptMsgRemovePadding = decryptMsgRemovePadding + de_msg_pad
    
print("decrypted msg : "+decryptMsg)
print("decrypted msg after removing pad : "+decryptMsgRemovePadding)
if (check_last_block == 1):
    print("remaining size : "+str(remaining))
    length_final = len(decryptMsgRemovePadding)
    #trying to remove last block padding
    #for i in range (remaining):
    #    print("check : "+decryptMsgRemovePadding[length_final-1])
    #    decryptMsgRemovePadding[length_final-1] = chr(" ")
    #    length_final= length_final- 1

    
    print("decrypted msg after removing last block pad : "+decryptMsgRemovePadding[:(length_final-remaining)])
