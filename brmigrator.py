from xml.dom import minidom
import os
import sys

print("\n Berilo Rojo 1.1 old extras.xml to new metadata migrator")
print(" Main file is berilorojo.py")
print(" ========================")

try:
    DIR = sys.argv[1]
except IndexError:
    print("\n Berilo Rojo old extras.xml to new metadata migrator usage:")
    print(" To use, first delete the meta directory in your repository's directory, and specify the repo's directory when running.")
    print(' To specify the directory of your repository:')
    print(" (Don't just copy and paste it, remember to specify the correct directory CAREFULLY!)\n")
    print(' On Linux: "brmigrator.py /directory/to/repository/"')
    print(' On Windows: "brmigrator.py C:/directory/to/repository/"\n')
    print(' The directory specified must also have APK files so that Berilo Rojo can use it.')
    print(" ======================== \n")
    sys.exit()

META_DIR_OUT = "meta/"
META_DIR = DIR + META_DIR_OUT
extra_path = DIR + "extras.xml"

if not os.path.isdir(META_DIR):
    try:
        os.mkdir(META_DIR)
    except PermissionError:
        print("\nError:\nUnable to write to directory, try checking the permissions of the directory or if it is an accesible location.")

def convertOldextras():
    extrainfo = None
    if not os.path.isfile(extra_path):
        sys.exit()
    extrainfo = minidom.parse(extra_path)
    extracount = extrainfo.getElementsByTagName("apkid").length

    print(" Converting old extras.xml to metadata xml files.\n (Which can be used to generate the new extras.xml file.)")
    print(" ======================== \n")

    for i in range(extracount):
        metafile = META_DIR + str(extrainfo.getElementsByTagName("apkid").item(i).firstChild.nodeValue) + ".xml"

        cmt = extrainfo.getElementsByTagName("cmt").item(i)
        catg = extrainfo.getElementsByTagName("catg").item(i)
        catg2 = extrainfo.getElementsByTagName("catg2").item(i)
        
        mdom = minidom.Document()
        
        mocc = mdom.createElement('pkg')
        mocc = mdom.appendChild(mocc)
        
        if not catg == None:
            catg = mdom.importNode(catg, True)
            child = mocc.appendChild(catg)
        
        if not catg2 == None:
            catg2 = mdom.importNode(catg2, True)
            child = mocc.appendChild(catg2)
        
        if not cmt == None:
            cmt = mdom.importNode(cmt, True)
            child = mocc.appendChild(cmt)
        
        try:
            with open(metafile, 'xb') as meta:
                meta.write(mdom.toprettyxml(indent = "  ", encoding="UTF-8"))
                print("\nMetadata saved to: " + metafile)
                print(" ======================== \n")
        except FileExistsError:
            continue
        mdom.unlink()

convertOldextras()