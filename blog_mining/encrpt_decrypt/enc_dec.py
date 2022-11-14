LETTERS_SMALLS = 'abcdefghijklmnopqrstuvwxyz'
LETTERS_CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '0123456789'

#Encryption
def encrypt(message, key):
    encrypted = ''
    key1=key
    if(key1>10):
        key1=key%10
    if(key>26):
        key=key%26
    for chars in message:
        if chars in LETTERS_SMALLS:
            num = LETTERS_SMALLS.find(chars)
            num =num+key
            if(num>=26):
                num=num%26
            encrypted +=  LETTERS_SMALLS[num]
        elif chars in LETTERS_CAPS:
            num = LETTERS_CAPS.find(chars)
            num =(num+key)
            if(num>=26):
                num=num%26
            encrypted +=  LETTERS_CAPS[num]
        elif chars in NUMBERS:
            num = NUMBERS.find(chars)
            num =num+key1
            if(num>=10):
                num=num%10
            encrypted +=  NUMBERS[num]
        else:
            encrypted+=chars
    return encrypted

#Decryption
def decrypt(message, key):
    decrypted = ''
    key1=key
    if(key1>10):
        key1=key%10
    if(key>26):
        key=key%26
    for chars in message:
        if chars in LETTERS_SMALLS:
            num = LETTERS_SMALLS.find(chars)
            num =num-key
            decrypted +=  LETTERS_SMALLS[num]
        elif chars in LETTERS_CAPS:
            num = LETTERS_CAPS.find(chars)
            num =num-key
            decrypted +=  LETTERS_CAPS[num]
        elif chars in NUMBERS:
            num = NUMBERS.find(chars)
            num =num-key1
            decrypted +=  NUMBERS[num]
        else:
            decrypted+=chars
    return decrypted

pwd=input("Enter password: ")
key=int(input("Enter EID: "))
print("Encrypted Message: "+encrypt(pwd,key))
enc=encrypt(pwd,key)
print("Decrypted Message: "+decrypt(enc,key))