import menu
import angecryption

funcs = {"png-png":angecryption.pngToPng,"png-pdf":angecryption.pngToPdf}

args = menu.menu()
if args.action in ["encrypt","decrypt"]:
    angecryption.handleFile(args.source,args.key,args.iv,args.output,args.action)
else:
    funcs[args.action](args.source,args.target,args.output,args.key)