#!/usr/bin/env python 

from Crypto.PublicKey import RSA
  
key = RSA.generate(2048, e=65537)
pub = key.publickey().exportKey("PEM")
priv = key.exportKey("PEM")
  
target = open("pubkey.txt", "w")
target.write(pub)
target.close()
target = open("privkey.txt", "w")
target.write(priv)
target.close()
