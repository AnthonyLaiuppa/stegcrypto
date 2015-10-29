#!/usr/bin/python

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import base64
import zlib
import Image
import stepic

#Split string into chunks 
def splitter(string, chunksize):
   return [string[i:i+chunksize] for i in range(0, len(string), chunksize)]
   
def decryptor():
   
   target = open('privkey.txt', 'r')
   key = target.read()
   target.close()
   
   #Create new SHA256 Hash
   h = SHA256.new()
   
   #RSA 2048 wrapped with PKCS1 as recommended by documentation 
   rsakey = RSA.importKey(key)
   rsakey = PKCS1_OAEP.new(rsakey , h)

   # target = open('testrun.txt' , 'rb') - For reading encrypted string from file
  
   #Open and decode Image to extract encrypted String 
   im = Image.open('encodedcat.png')
   encoded = stepic.decode(im)
   encoded = encoded.decode()
   # encoded = target.read()
   # target.close()
   
   #Undo B64 encoding on top of string
   encrypted = base64.b64decode(encoded)
   
   #Decompress string
   encrypted = zlib.decompress(encrypted)
   decrypted = ''
   #Chunks must be RSA modulus size
   chunks = splitter(encrypted, 256)   
   
   for chunk in chunks: 
      decrypted += rsakey.decrypt(chunk)   
   
   print decrypted
   print len(decrypted)

def main():
   decryptor()
   
if __name__ == '__main__':
   main() 
