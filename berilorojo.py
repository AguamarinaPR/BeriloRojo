#
# Aguamarina Server/Berilo Rojo script 1.1
# Rewritten from scratch in Python, with PHP script Berilo Rojo 1.0 as reference implementation
# PHP script Berilo Rojo 1.0 was based on Aptoide server generate script version 1.4
#
########################################
#
# Configuration is now done through command-line arguments and is no longer hardcoded.
#
from pyaxmlparser import APK
from xml.dom import minidom
from PIL import Image
import os
import time
import hashlib
import sys
import zipfile
import logging

print("\n Berilo Rojo 1.1")
print(" Repository generator for Aguamarina")
print(" ========================")

def showUsage():
    print("\n Berilo Rojo usage:")
    print(' To specify the directory of your repository:')
    print(" (Don't just copy and paste it, remember to specify the correct directory CAREFULLY!)\n")
    print(' On Linux: "berilorojo.py /directory/to/repository/"')
    print(' On Windows: "berilorojo.py C:/directory/to/repository/"\n')
    print(' The directory specified must also have APK files so that Berilo Rojo can use it.')
    print(" ======================== \n")
    print(' To specify the mode of operation, after the directory, add one of these:\n')
    print(' -a = Metadata files, info.xml and extras.xml (default mode)')
    print(' -m = Metadata files only')
    print(' -i = info.xml only')
    print(' -e = extras.xml only')
    print('\n Example of usage:\n')
    print(' "berilorojo.py /directory/to/repository/ -a"')
    print(" ======================== \n")
    sys.exit()

try:
    DIR = sys.argv[1]
    try:
        MODE = sys.argv[2]
    except IndexError:
        MODE = "-a"
except IndexError:
    showUsage()

ICON_DIR_OUT = "icons/"
ICON_DIR = DIR + ICON_DIR_OUT
META_DIR_OUT = "meta/"
META_DIR = DIR + META_DIR_OUT
xml_path = DIR + "info.xml"
extra_path = DIR + "extras.xml"
logging.basicConfig(level=logging.ERROR) # To disable some ugly looking nonfatal warnings

invalidziperror = "The APK could not be read! Maybe it is corrupted. Skipping...\n"
spacewarn = []

if not os.path.isdir(ICON_DIR):
    try:
        os.mkdir(ICON_DIR)
    except PermissionError:
        print("\nError:\nUnable to write to directory, try checking the permissions of the directory or if it is an accesible location.")

if not os.path.isdir(META_DIR):
    os.mkdir(META_DIR)

# Particularly common for Android 1.0 APKs to lack sdkver number, so we'll set those to 0
def getSdkver(sdknum):
    if not isinstance(sdknum, str):
        sdknum = '0'
    elif not sdknum.isdecimal():
        sdknum = '0'
    return sdknum

def getMd5(archive):
    mdhash = hashlib.md5()
    with open(archive, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            mdhash.update(chunk)
    return mdhash.hexdigest()

def getModTime(archive):
    ctim = time.ctime(archive)
    dtim = time.strptime(ctim)
    return time.strftime('%Y-%m-%d', dtim)
    

def getInfo(apkfile):
    send = {}
    # If an APK is an invalid zip, we want to skip over it instead of exiting out.
    try:
        parseapk = APK(apkfile)
        out = parseapk.application
        if not isinstance(out, str):
            out = "Nameless App"
        send['name'] = out
        out = parseapk.icon_info
        if not isinstance(out, str):
            out = ""
        send['icon'] = out
        out = parseapk.package
        send['pkg'] = out
        out = parseapk.version_name
        send['ver'] = out
        out = parseapk.version_code
        send['vercode'] = out
    except zipfile.BadZipfile:
        out = "invalid zip"
        send['pkg'] = out
    out = str(int(os.path.getsize(apkfile) / 1024))
    send['size'] = out
    out = getSdkver(parseapk.get_min_sdk_version())
    send['sdkver'] = out
    out = getMd5(apkfile)
    send['md5h'] = out
    out = getModTime(os.path.getmtime(apkfile))
    send['date'] = out
    return send

def getIcon(data, icon, apk):
    icfinal = ICON_DIR_OUT + apk
    try:
        with zipfile.ZipFile(data, 'r') as archive:
            with archive.open(icon, 'r') as iclone:
                with Image.open(iclone, mode="r") as iclone:
                    width, height = iclone.size
                    iclone.thumbnail((96, 96))
                    iclone.save(ICON_DIR + apk, "PNG")
                    iclone.close()
            archive.close()
    except zipfile.BadZipfile:
        icfinal = ""
    return(icfinal)

dump = []
for files in os.scandir(DIR):
    if str(files.name).endswith('.apk'):
        dump.append(str(files.name))
    else:
        continue

def genMetafiles():
    metaless = []
    for metas in dump:
        rtrn = getInfo(DIR + metas)
        if rtrn["pkg"] == "invalid zip":
            print(metas + ": " + invalidziperror)
            continue
        elif not os.path.isfile(META_DIR + rtrn["pkg"] + ".xml"):
            metaless.append(metas)
        else:
            continue
    # Some characters are reserved for XML and to use those, you will need to use escape sequences.
    if not metaless == []:
        print(" Enter metadata for the apps")
        print(" ======================== \n")
    for newmeta in metaless:
        rtrn = getInfo(DIR + newmeta)
        metafile = META_DIR + rtrn["pkg"] + ".xml"
        
        print("Primary categories available:\n Games\n Applications\n Others")
        catg = input("Enter primary category for "+ rtrn["name"] + " (" + rtrn["pkg"] +"):\n")
        match catg:
            case "Applications":
                print("\nSecondary categories available for Applications:\n Comics, Communication, Entertainment, Finance,\n Health, Lifestyle, Multimedia, News & Weather,\n Productivity, Reference, Shopping, Social,\n Sports, Themes, Tools, Travel,\n Demo, Software Libraries, Other")
            case "Games":
                print("\nSecondary categories available for Games:\n Arcade & Action, Brain & Puzzle, Cards & Casino,\n Casual, Emulators, Other")
            case _:
                print('\nThere are no secondary categories for primary categories that are not "Games" or "Applications".\nDespite this, you have the option to enter one.')
        catg2 = input("\nEnter secondary category for "+ rtrn["name"] + " (" + rtrn["pkg"] +"):\n")
        cmt = input("\nEnter a description for "+ rtrn["name"] + " (" + rtrn["pkg"] +"):\n")
        mdom = minidom.Document()
        
        mocc = mdom.createElement('pkg')
        mocc = mdom.appendChild(mocc)
        
        mchild = mdom.createElement('catg')
        mchild = mocc.appendChild(mchild)
        mvalue = mdom.createTextNode(catg)
        mvalue = mchild.appendChild(mvalue)
        
        mchild = mdom.createElement('catg2')
        mchild = mocc.appendChild(mchild)
        mvalue = mdom.createTextNode(catg2)
        mvalue = mchild.appendChild(mvalue)
        
        mchild = mdom.createElement('cmt')
        mchild = mocc.appendChild(mchild)
        mvalue = mdom.createTextNode(cmt)
        mvalue = mchild.appendChild(mvalue)
        
        try:
            with open(metafile, 'xb') as meta:
                meta.write(mdom.toprettyxml(indent = "  ", encoding="UTF-8"))
                print("\nMetadata saved to: " + metafile)
                print(" ======================== \n")
        except FileExistsError:
            continue
        mdom.unlink()

dom = minidom.Document()
root = dom.createElement('apklst')
root = dom.appendChild(root)
def genInfoxml():
    print(" Generating info.xml")
    print(" ======================== \n")
    for apk in dump:
        print("APK: " + apk)
        rtrn = getInfo(DIR + apk)        
        if rtrn["pkg"] == "invalid zip":
            print(apk + ": " + invalidziperror)
            continue
        
        if rtrn['icon'] == "":
            icon = rtrn['icon']
        else:
            icon = getIcon(DIR + apk, rtrn["icon"], rtrn["pkg"])
        
        if not isinstance(rtrn['ver'], str):
            ver = ""
        else:
            ver = rtrn["ver"]
        
        if not isinstance(rtrn['vercode'], str):
            vercode = ""
        else:
            vercode = rtrn["vercode"]
        
        metapath = META_DIR + rtrn["pkg"] + ".xml"
        metainfo = None
        if os.path.isfile(metapath):
            metainfo = minidom.parse(metapath)
        
        if " " in apk:
            spacewarn.append(apk)
            apk = apk.replace(" ", "%20")
        
        print("Package (hasID): " + rtrn["pkg"])
        print("Version: " + ver)
        print("Version Code: " + vercode)
        print("Name: " + rtrn["name"])
        print("Icon: " + rtrn["icon"])
        print("Icon(L): " + icon)
        print("Date: " + rtrn["date"])
        print("Md5Hash: " + rtrn["md5h"])
        print("Size: " + rtrn["size"] + "KB")
        print("Minimum Android SDK version: " + rtrn["sdkver"])
        print(" ======================== \n")
        
        occ = dom.createElement('package')
        occ = root.appendChild(occ)
        
        child = dom.createElement('name')
        child = occ.appendChild(child)
        value = dom.createTextNode(rtrn["name"])
        value = child.appendChild(value)
        
        child = dom.createElement('path')
        child = occ.appendChild(child)
        value = dom.createTextNode(apk)
        value = child.appendChild(value)
        
        child = dom.createElement('ver')
        child = occ.appendChild(child)
        value = dom.createTextNode(ver)
        value = child.appendChild(value)
        
        child = dom.createElement('vercode')
        child = occ.appendChild(child)
        value = dom.createTextNode(vercode)
        value = child.appendChild(value)
        
        child = dom.createElement('apkid')
        child = occ.appendChild(child)
        value = dom.createTextNode(rtrn["pkg"])
        value = child.appendChild(value)
        
        child = dom.createElement('icon')
        child = occ.appendChild(child)
        value = dom.createTextNode(icon)
        value = child.appendChild(value)
        
        # Metadata
        if not metainfo == None:
            
            catg = metainfo.getElementsByTagName("catg").item(0)
            if not catg == None:
                catg = dom.importNode(catg, True)
                child = occ.appendChild(catg)
        
            catg2 = metainfo.getElementsByTagName("catg2").item(0)
            if not catg2 == None:
                catg2 = dom.importNode(catg2, True)
                child = occ.appendChild(catg2)
        
        child = dom.createElement('date')
        child = occ.appendChild(child)
        value = dom.createTextNode(rtrn["date"])
        value = child.appendChild(value)
        
        child = dom.createElement('md5h')
        child = occ.appendChild(child)
        value = dom.createTextNode(rtrn["md5h"])
        value = child.appendChild(value)
        
        child = dom.createElement('sz')
        child = occ.appendChild(child)
        value = dom.createTextNode(rtrn["size"])
        value = child.appendChild(value)
        
        child = dom.createElement('sdkver')
        child = occ.appendChild(child)
        value = dom.createTextNode(rtrn["sdkver"])
        value = child.appendChild(value)
    with open(xml_path, 'wb') as xmlinfo:
        xmlinfo.write(dom.toprettyxml(indent = "  ", encoding="UTF-8"))
        print("info.xml saved to: " + xml_path)
        print(" ======================== \n")
    dom.unlink()

edom = minidom.Document()
eroot = edom.createElement('extras')
eroot = edom.appendChild(eroot)
def genExtrasxml():
    print(" Generating extras.xml")
    print(" ======================== \n")
    for apk in dump:
        rtrn = getInfo(DIR + apk)
        if rtrn["pkg"] == "invalid zip":
            print(apk + ": " + invalidziperror)
            continue
        
        eocc = edom.createElement('pkg')
        eocc = eroot.appendChild(eocc)
        
        metapath = META_DIR + rtrn["pkg"] + ".xml"
        metainfo = None
        if os.path.isfile(metapath):
            metainfo = minidom.parse(metapath)
            cmt = metainfo.getElementsByTagName("cmt").item(0)
            if not cmt == None:
                print("APK: " + apk)
                print("Name: " + rtrn["name"])
                print("Package ID: " + rtrn["pkg"])
                print(" ======================== \n")
                
                echild = edom.createElement('apkid')
                echild = eocc.appendChild(echild)
                evalue = edom.createTextNode(rtrn["pkg"])
                evalue = echild.appendChild(evalue)
                
                # Metadata
                
                cmt = edom.importNode(cmt, True)
                echild = eocc.appendChild(cmt)
    with open(extra_path, 'wb') as xmlextra:
        xmlextra.write(edom.toprettyxml(indent = "  ", encoding="UTF-8"))
        print("extras.xml saved to: " + extra_path)
        print(" ======================== \n")
    edom.unlink()

match MODE:
    case "-a":
        genMetafiles()
        genInfoxml()
        genExtrasxml()
    case "-m":
        genMetafiles()
    case "-i":
        genInfoxml()
    case "-e":
        genExtrasxml()
    case _:
        showUsage()

if spacewarn:
    print("WARNING: At least one APK in the repo has a space in its file name!\n")
    for spapk in spacewarn:
        print(' "' + spapk + '" has a space in its filename!')
    print("\nURLs cannot have any spaces in them, so the spaces in the APK file paths")
    print('in "info.xml" have been escaped as "%20", but your web server might escape')
    print("the names differently. It is suggested that you remove the spaces in any")
    print("APK filenames with spaces in them to prevent unexpected behavior and then")
    print("run Berilo Rojo again.")
    print(" ======================== \n")
