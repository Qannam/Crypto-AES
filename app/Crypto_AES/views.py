from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from django.shortcuts import redirect

class AESCipher(object):

    def __init__(self, key):
        if len(key) != 32:
            print()
            raise Exception("Sorry, you key length is " + str(len(key)) +" key size should be 32 byte length 256 bit") 
        self.bs = AES.block_size
        self.key = key.encode("utf8") # key size should be 32 byte length 256 bit

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


def index(request):
    template = loader.get_template("Crypto_AES/index.html")
    context = {
    }
    return HttpResponse(template.render(context, request))

def encrypt(request):
    errorMessage=""
    if request.method =='GET':
        return redirect("index")
    template = loader.get_template("Crypto_AES/index.html")
    encKey = request.POST["encryptionKey"]
    orginal_plainText = request.POST["plainText"]

    if len(encKey) != 32:
        errorMessage = "Your key length is " + str(len(encKey)) +" bytes. The key size should be 32 bytes (256-bit)."
    else:
        try:
            AES = AESCipher(encKey)
            cipherText = AES.encrypt(orginal_plainText)
        except Exception as ex:
            errorMessage= ex

    if errorMessage != "":
        context = {
            "orginal_plainText": orginal_plainText,
            "orginal_encryptionKey": encKey,
            "encryption_error_message": errorMessage,
        }
    else: 
        context = {
            "cipherText": cipherText,
            "orginal_plainText": orginal_plainText,
            "orginal_encryptionKey": encKey,
            "encryption_success_message": "The message has been successfully encrypted.",
        }
    return HttpResponse(template.render(context, request))

def decrypt(request):
    errorMessage=""
    if request.method =='GET':
        return redirect("index")
    template = loader.get_template("Crypto_AES/index.html")
    decKey = request.POST["decryptionKey"]
    orginal_cipherText = request.POST["cipherText"]
    if len(decKey) != 32:
        errorMessage = "Your key length is " + str(len(decKey)) +" bytes. The key size should be 32 bytes (256-bit)."  
    else:
        try:
            AES = AESCipher(decKey)
            plainText = AES.decrypt(orginal_cipherText)
            if plainText == "":
                errorMessage="Incorrect key"
        except Exception as ex:
            if "Incorrect padding" in str(ex):
                errorMessage= "Incorrect Cipher Text: " + str(ex)
            else:
                errorMessage= ex
    if errorMessage != "":
        context = {
            "orginal_cipherText": orginal_cipherText,
            "orginal_decryptionKey": decKey,
            "decryption_error_message": errorMessage,
            "auto_scroll": "decryptionBox"
        }
    else:
        context = {
            "plainText": plainText,
            "orginal_cipherText": orginal_cipherText,
            "orginal_decryptionKey": decKey,
            "decryption_success_message": "The message has been successfully decrypted.",
            "auto_scroll": "decryptionBox"
            }
    return HttpResponse(template.render(context, request))