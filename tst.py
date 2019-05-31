from Crypto.Cipher import AES

key = "yellow submarine"
iv = "556cd80986986b0300760808c8db0672".decode("hex")
aes = AES.new(key,AES.MODE_CBC,iv)
with open("out1.png","r") as f:
    s=f.read()

with open("out2.png","w") as f:
    f.write(aes.encrypt(s))