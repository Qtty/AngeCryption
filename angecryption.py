from Crypto.Cipher import AES
from os import SEEK_END
from zlib import crc32

def encrypt(msg,iv,key):
    aes = AES.new(key,AES.MODE_ECB)
    m = [msg[i:i+16] for i in range(0,len(msg),16)]
    r = ""
    for i in m:
        r += aes.encrypt(xor(i,iv))
        iv = r[-16:]
    return r

def decrypt(msg,iv,key):
    aes = AES.new(key,AES.MODE_ECB)
    m = [msg[i:i+16] for i in range(0,len(msg),16)]
    r = ""
    for i in m:
        r += xor(iv,aes.decrypt(i))
        iv = i
    return r

def intToStr(x):
    x = hex(x)[2:]
    if "L" in x:
        x = x[:-1]
    if len(x) % 8 != 0:
        x = x.zfill(8)
    return x.decode("hex")

def xor(a,b):
    return ''.join([chr(ord(x) ^ ord(y)) for x,y in zip(a,b)])

def pngToPng(img1,img2,img3,key):
    with open(img1,"r") as f:
        source = f.read()
    with open(img2,"r") as f:
        target = f.read()
    
    source += "\x00" * (16 - len(source) % 16) * (len(source) % 16 != 0)
    
    aes = AES.new(key,AES.MODE_ECB)
    iv = xor(aes.decrypt(source[:16]),source[:8]+intToStr(len(source)-16)+"rmll")
    print "IV: " + iv.encode("hex")

    source = decrypt(source,iv,key)
    source += intToStr(crc32(source[12:])%(1<<32)) + target[8:]
    source += "\x00" * (16 - len(source) % 16)
    with open(img3,"w") as f:
        f.write(encrypt(source,iv,key))

def handleFile(src,key,iv,out,action):
    aes = AES.new(key,AES.MODE_CBC,iv)
    with open(src,"r") as f:
        s = f.read()
    with open(out,"w") as f:
        if action == "decrypt":
            f.write(decrypt(s,iv,key))
        else:
            f.write(encrypt(s,iv,key))