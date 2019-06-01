from Crypto.Cipher import AES
from os import SEEK_END
from zlib import crc32
from puremagic import from_file

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
    source += "\x00" * (16 - len(source) % 16) * (len(source) % 16 != 0)
    with open(img3,"w") as f:
        f.write(encrypt(source,iv,key))

def pngToPdf(src,tar,out,key):
    #order == 1: img is source else pdf is source
    order = 1
    if from_file(src,mime=True).split("/")[1] == "png":
        with open(src,"r") as f:
            img = f.read()
        with open(tar,"r") as f:
            pdf = f.read()
    else:
        order = 0
        with open(tar,"r") as f:
            img = f.read()
        with open(src,"r") as f:
            pdf = f.read()

    img += "\x00" * (16 - len(img) % 16) * (len(img) % 16 != 0)
    aes = AES.new(key,AES.MODE_ECB)
    iv = xor(aes.decrypt(img[:16]),"%PDF-\x00obj\nstream")
    print "IV: " + iv.encode("hex")

    img = decrypt(img,iv,key)
    img += "\x00endstream\nendobj\n" + pdf
    img += "\x00" * (16 - len(img) % 16) * (len(img) % 16 != 0)
    with open(out,"w") as f:
        if order:
            f.write(encrypt(img,iv,key))
        else:
            print "[+] encrypt \"{}\" to get the target file".format(out)
            f.write(img)


def handleFile(src,key,iv,out,action):
    aes = AES.new(key,AES.MODE_CBC,iv)
    with open(src,"r") as f:
        s = f.read()
    with open(out,"w") as f:
        if action == "decrypt":
            f.write(decrypt(s,iv,key))
        else:
            f.write(encrypt(s,iv,key))

if __name__=="__main__":
    pngToPdf("tests/tst1.png","tests/tst.pdf","tests/ange","yellow submarine",0)