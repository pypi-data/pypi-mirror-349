import random,PrintSlow

def encryptext():
    file=open("chars.txt","r")
    chars=file.readlines()
    file.close()

    counter=0
    for char in chars:
        chars[counter]=char.strip("\n")
        counter+=1
        
    file=open("key.txt","r")
    key=file.readlines()
    file.close()

    counter=0
    for char in key:
        key[counter]=char.strip("\n")
        counter+=1


    #ENCRYPT
    plain_text = input("Enter a message to encrypt: ")
    cipher_text = ""

    for letter in plain_text:
        index = chars.index(letter)
        cipher_text += key[index]

    print("Done.")


    number=""
    for carrier in range(0,20):
        number+=str(random.randint(0,9))

    if save:
        passwordfile=open("encryptext output "+number+".txt","w")
        passwordfile.write(cipher_text)
        passwordfile.close()
        print("OUTPUT TO FILE:" + cipher_text)
    else:
        print("OUTPUT:" + cipher_text)



def decryptext():
    import random

    file=open("chars.txt","r")
    chars=file.readlines()
    file.close()

    counter=0
    for char in chars:
        chars[counter]=char.strip("\n")
        counter+=1
        
    file=open("key.txt","r")
    key=file.readlines()
    file.close()

    counter=0
    for char in key:
        key[counter]=char.strip("\n")
        counter+=1


    #DECRYPT
    cipher_text = input("Enter a message to decrypt: ")
    plain_text = ""

    for letter in cipher_text:
        index = key.index(letter)
        plain_text += chars[index]

    print("Done.")


    number=""
    for carrier in range(0,20):
        number+=str(random.randint(0,9))

    if save:
        passwordfile=open("decryptext output "+number+".txt","w")
        passwordfile.write(plain_text)
        passwordfile.close()
        print("OUTPUT TO FILE:" + plain_text)
    else:
        print("OUTPUT:" + plain_text)



def generatekeychar():
    import random
    import string

    chars = list(" " + string.punctuation + string.digits + string.ascii_letters)
    random.shuffle(chars)#shuffled twice so the original alphabet cannot be found just by checking index of letter
    file=open("chars.txt","w")
    for carrier in chars:
        file.write(carrier+"\n")
    file.close()

    key = chars.copy()
    random.shuffle(key)
    file=open("key.txt","w")
    for carrier in key:
        file.write(carrier+"\n")
    file.close()
    #you need both chars.txt and key.txt as the key cipher text matches to the chars cipher to find out the mapping
    #the next step would be to shift the key.txt every letter to make it an enigma machine with two rotors

    print("Done.")

    print("OUTPUT TO FILE:" + "cannot show...")

def run():
    #main code
    print("Encryptext V4: MESSAGE ENCRYPT AND DECRYPTOR")
    global save
    save = False#refers to creating a save file output
    while True:
        i = input("type command to run: encrypt(e), decrypt(d), generate key and char(g) and exit(q)")
        if i == 'g':
            generatekeychar()
        elif i == 'd':
            decryptext()
        elif i == 'e':
            encryptext()
        elif i == 'q':
            exit()


