import argparse
import sys
from puremagic import from_file

def checkKey(k):
    if len(k) != 16:
        raise argparse.ArgumentTypeError("the key must be 16 bytes in length")
    return k

def checkIv(iv):
    try:
        iv = iv.decode("hex")
    except:
        raise argparse.ArgumentTypeError("the iv must be in hex")
    if len(iv) != 16:
        raise argparse.ArgumentTypeError("the iv must be 16 bytes in length")
    return iv

def checkFile(f):
    fileTypes = ["png","pdf"]

    try:
        open(f,"r")
    except Exception as e:
        raise argparse.ArgumentTypeError("can't open {}: {}".format(f,e[1]))

    if from_file(f,mime=True).split("/")[1] not in fileTypes:
        raise argparse.ArgumentTypeError("the file must be either a {}".format("or a".join(fileTypes)))

    return f


def menu():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--key",type=checkKey,help="the encryption key",required=True)
    parser.add_argument("-s","--source",type=checkFile,help="the source file(the one that shows up by default in the result file)",required=True)
    parser.add_argument("--action",choices=["encrypt","decrypt","png-png","png-pdf"],help="the action to perform:\nencrypt: {}\ndecrypt: {}\nother: {}".format("encrypt the result file(flag --iv required)","decrypt the result file(flag --iv required)","generate an angecrypted file with the corresponding file types(flag -t/--target required)"),required=True)
    parser.add_argument("--iv",type=checkIv,help="the iv generated from the encryption phase")
    parser.add_argument("-t","--target",type=checkFile,help="the target file(the one that's hidden in the result file)")
    parser.add_argument("-o","--output",help="the output/result file (default %(default)s)",default="angecryption.out")
    
    namespace = parser.parse_args()
    if namespace.action in ["encrypt","decrypt"]:
        if namespace.iv == None:
            parser.error('IV not specified')
    else:
        if namespace.target == None:
            parser.error('TARGET file not specified')
    return namespace

if __name__=="__main__":
    args = menu()
    print args