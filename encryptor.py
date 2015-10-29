#!/usr/bin/python

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import base64
import zlib
import Image
import stepic

#Function to split key into chunks 
def splitter(string, chunksize):
   return [string[i:i+chunksize] for i in range(0, len(string), chunksize)]

def encrypter():

   target = open('pubkey.txt', 'r')
   key = target.read() #read in PEM formatted key from file 
   target.close()

   #Create new SHA256 hash
   h = SHA256.new()  
   #RSA 2048 bit wrapped with PKCS1 as recommended by documentation
   # Default SHA1 Hash is weak, replacing with SHA2 hash
   rsakey = RSA.importKey(key)
   rsakey = PKCS1_OAEP.new(rsakey, h)
   
   #Construct a large string to practice encrypting
   As = 'A' * 750
   Bs = 'B' * 750
   Cs = 'C' * 750
   Ds = 'D' * 750
   string = As + Bs + Cs + Ds 
   
   #Chunk size = (RSA modulus -2) -( 2 * (hash digest size))
   #In this case (256 -2 ) -( 2 * (32) )= 190
   chunks = splitter(string, 190)
   
   encrypted = '' 

   for chunk in chunks:
      encrypted += rsakey.encrypt(chunk)

   #Lets try compressing the encrypted string a little
   encrypted = zlib.compress(encrypted)

   #Add some b64 encoding to sort of obfuscate our encryption
   encrypted = base64.b64encode(encrypted)
   target = open('testrun.txt', 'w')
   output = target.write(encrypted)
   target.close()
   
   print 'Encrypted String is of size:' + str(len(encrypted)) + '\n'  

   #Steganography, Hiding the encrypted text in plain sight using least significant bit
   #Image has to be png as it is lossless format. 
   im = Image.open("cat.png")
   im2 = stepic.encode(im, encrypted)
   im2.save('encodedcat.png')      
   
def main():
   encrypter()

if __name__ == '__main__':
   main()
