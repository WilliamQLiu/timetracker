""" An example of an encryption algorithm (AES)
    Advanced Encryption Standard is a symmetric block cipher
    It has a fixed data block size of 16 bytes
    Its keys can be 128, 192, or 256 bits long

 """

from Crypto.Cipher import AES
from base64 import b64encode, b64decode
#import os

BLOCK_SIZE = 32 # Block size for the cipher object must be 16, 24, 32 for AES
PADDING = '*'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
#secret = os.urandom(BLOCK_SIZE)
secret = '\xfd\x06\xea\xd1\xb3\x91e\xff\x998\xe8\xa4\x1eT\xfbrn\x08\xa7g\x8a\x9a\xe2U\xd8H\xc1\xcf\xb8\xf7o\x91'
cipher = AES.new(secret)

def create_encryption(message):

    EncodeAES = lambda c, s: b64encode(c.encrypt(pad(s)))
    #pdb.set_trace()

    # Encode a string
    encoded = EncodeAES(cipher, message)
    #print "Encrypted string:", encoded

    return encoded

def return_decryption(message):

    DecodeAES = lambda c, e: c.decrypt(b64decode(e)).rstrip(PADDING)
    # Decode the encoded string
    decoded = DecodeAES(cipher, message)
    #print "Decrypted string:", decoded

    return decoded
