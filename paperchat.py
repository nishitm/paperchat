import hashlib
import os
import text2pdf
import time

def newSheet(hash, seed, key):
    #  key='ajgyepocnjiiwsdgriplazmnbkreqduyjfwqalkirhgpqamneiujfhgvyoebtgykebkd'
    for i in range(0, 50):
        hash.update(seed + "1324-053dsfgkjbsdfnqr;sjdfg")
        seed = hash.digest()
        while (ord(seed[0]) > 233):  # 9*26 - to achieve constant probability of 0-26
            hash.update(seed + "kmbjkahsrtueggja'sfknbjfgkhsjsdlgfa'dbniugsdgnblkjsdg")
            seed = hash.digest()
        key = key + chr((ord(seed[0]) % 26) + 65)

    seed = hash.hexdigest().upper()

    soubor = open("/tmp/" + seed, 'w')

    for parts in range(0, 2):

        if parts == 0:
            soubor.write("!(0) DESTROY BEFORE ....................\n\n!")
            soubor.write("!(1) USE THIS TO SEND A MESSAGE ONLY TO .....................!")
            soubor.write(
                "                                                                                                                                         50 characters\n")
        else:
            soubor.write("!(0) DESTROY BEFORE ....................\n\n!")
            soubor.write("!(2) USE THIS TO RECEIVE A MESSAGE ONLY FROM ......................!\n")
        soubor.write(' ')
        for i in range(0, 149):
            soubor.write('_');
        soubor.write("\n")
        for j in range(0, 2):
            soubor.write('|');
            for i in range(0, 50):
                soubor.write('  |')
            soubor.write("\n")
        soubor.write('|')
        for i in range(0, 50):
            soubor.write('__|')
        soubor.write("\n")
        for i in range(0, 50):
            soubor.write(' | ')
        soubor.write("\n")

        for line in range(0, 26):
            str = ' '
            for s in range(0, 50):
                offset = ord(key[s]) + (25 - line)
                if offset > ord('Z'):
                    offset = offset - 26
                str = str + chr(ord('A') + line) + chr(offset) + ' '
            soubor.write(str + "\n")

        if parts == 4:
            soubor.write("\n\n\n\n\n\n")
        else:
            for j in range(0, 4):
                for i in range(0, 50):
                    soubor.write("  |")
                soubor.write("\n")
        if parts == 0:
            soubor.write(' ')
            for s in range(0, 4):
                soubor.write('------CUT HERE-----DESTROY UPPER PART')
            soubor.write("\n")
        else:
            soubor.write(' ')
            for s in range(0, 1):
                soubor.write(
                    "                --------------- DESTROY THE WHOLE PAPER ----- YOU'VE RECEIVED A MESSAGE ----- DESTROY THE WHOLE PAPER ---------------")
            soubor.write('\n')

        for i in range(0, 50):
            soubor.write("  |")
        soubor.write("\n")

        for line in range(0, 0):
            str = ' '
            for s in range(0, 50):
                offset = (s % 26) + 65 + line
                if offset > ord('Z'):
                    offset = offset - 26
                str = str + '$' + chr(offset) + ' '
            soubor.write(str + "\n")
            if line == 5:
                if parts == 0:
                    soubor.write(' ')
                    for s in range(0, 4):
                        soubor.write('------CUT HERE-----DESTROY UPPER PART')
                    soubor.write("\n")
                else:
                    soubor.write(' ')
                    for s in range(0, 2):
                        soubor.write(
                            "-------YOU'VE RECEIVED A MESSAGE, DESTROY THE WHOLE PAPER, OR CUT HERE TO KEEP THE MESSAGE ---")
                    soubor.write('\n')
        soubor.write(' ')
        for i in range(0, 149):
            soubor.write('_');
        soubor.write("\n")
        for j in range(0, 2):
            soubor.write('|');
            for i in range(0, 50):
                soubor.write('  |')
            soubor.write("\n")
        soubor.write('|')
        for i in range(0, 50):
            soubor.write('__|')
        soubor.write("\n")

        soubor.write("\nLast 5 letters of code must be sent with the message. Code of this sheet is : " + seed[5:len(
            seed) - 5] + "  " + "!" + seed[len(seed) - 5:] + "!\n\n\n\n\n")

        if (parts == 0):
            for i in range(0, 150):
                soubor.write("-")
            # soubor.write("\n")
            for i in range(0, 1):
                soubor.write(
                    "       --------------------- TEAR APART HERE AND GIVE THE LOWER PART TO YOUR FRIEND WHO WILL RECEIVE AN ENCRYPTED MESSAGE -------------------");
            soubor.write("\n")
            for i in range(0, 150):
                soubor.write("-")
            soubor.write("\n\n\n\n\n")

    # now we can create a pdf file and send it to browser
    soubor.close()
    return [hash, seed, key]


def index(req):
    hash = hashlib.md5()
    seed = str(time.time())
    key = ''

    hash, seed, key = newSheet(hash, seed, key)
    pdfclass = text2pdf.PyText2Pdf()
    pdfclass.parse_args("/tmp/" + str(seed))
    pdfclass.convert()
    os.remove("/tmp/" + str(seed))
    lines = open("/tmp/" + str(seed) + ".pdf", "rb").read()
    os.remove("/tmp/" + seed + ".pdf")
    req.content_type = "application/pdf"
    req.headers_out.add("Content-transfer-encoding", "binary")
    req.headers_out.add("Content-length", str(len(lines)))
    req.headers_out.add("Content-disposition", "attachment; filename=sheet" + seed + ".pdf")
    req.send_http_header()
    req.write(lines)
