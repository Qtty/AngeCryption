import menu
import angecryption

args = menu.menu()
if args.action in ["encrypt","decrypt"]:
    angecryption.handleFile(args.source,args.key,args.iv,args.output,args.action)
else:
    angecryption.pngToPng(args.source,args.target,args.output,args.key)