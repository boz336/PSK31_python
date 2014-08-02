# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 12:07:16 2014

@author: rtb  

Copied from KD4HSO's YouTube Video: 
https://www.youtube.com/watch?v=7IzxZKL2uUE    
"""

##PSK31 binary data source generator
# Output file is used to drive a GNU Radio DBPSK Modulator at 31.25bps

import struct

#Prompt user to input a string to transmit
INPUT_STRING = 'n4ons the quick brown fox jumped over the lazy dog 0123456789'

#Varicode dictionary converts character to string of binary
VARICODE_DICTIONARY = {'a':'1011',
                       'b':'1011111',
                       'c':'101111',
                       'd':'101101',
                       'e':'11',
                       'f':'111101',
                       'g':'1011011',
                       'h':'101011',
                       'i':'1101',
                       'j':'111101011',
                       'k':'10111111',
                       'l':'11011',
                       'm':'111011',
                       'n':'1111',
                       'o':'111',
                       'p':'111111',
                       'q':'110111111',
                       'r':'10101',
                       's':'10111',
                       't':'101',
                       'u':'110111',                       
                       'v':'1111011',
                       'w':'1101011',
                       'x':'11011111',
                       'y':'1011101',
                       'z':'111010101',
                       ' ':'1',
                       '0':'10110111',
                       '1':'10111101',
                       '2':'11101101',
                       '3':'11111111',
                       '4':'101110111',
                       '5':'101011011',
                       '6':'101101011',
                       '7':'110101101',
                       '8':'110101011',
                       '9':'110110111',
                       ':':'11110101',
                       ';':'110111101',
                       '!':'111111111',
                       '"':'101011111',
                       '#':'111110101',
                       '$':'111011011',
                       '%':'1011010101',
                       '.':'1010111',
                       ',':'1110101',
                       'A':'1111101',
                       'B':'11101011',
                       'C':'10101101',
                       'D':'10110101',
                       'E':'1110111',
                       'F':'11011011',
                       'G':'11111101',
                       'H':'101010101',
                       'I':'1111111',
                       'J':'111111101',
                       'K':'101111101',
                       'L':'11010111',
                       'M':'10111011',
                       'N':'11011101',
                       'O':'10101011',
                       'P':'11010101',
                       'Q':'111011101',
                       'R':'10101111',
                       'S':'1101111',
                       'T':'1101101',
                       'U':'101010111',
                       'V':'110110101',
                       'W':'101011101',
                       'X':'101110101',
                       'Y':'101111011',
                       'Z':'101111011',
                       'CR':'11111',
                       'DEL':'1110110101'}                               

# This string wil hold the varicode; initialize it to 8 bit preamble
varicode_string = ''
varicode_string += '00000000'

# For each character, concatenate the varicode, adding the termination 00
for char in INPUT_STRING:
    varicode_string += VARICODE_DICTIONARY[char]
    varicode_string += '00'
    
# Now add the postamble
varicode_string += '11111111'

# Pad with ones (more postamble) to form whole bytes
# Only works if varicode string is at least 8 bits long;  use the preamble
while len(varicode_string)%8 !=0:
    varicode_string += '1'
    
print('Non-inverted varicode string:')
print(varicode_string)
print('')

# Open a file for writing
f = open('psk21_tx.bin', 'wb')

# Grab 8 string bits at a time
# Convert to unsigned bytes and invert (Due to the way the BPSK modulator 
# block in GRC works)

for n in range(0, len(varicode_string)/8) :
    u8 = ~int( varicode_string[8*n:8*(n+1)], 2) % 2**8
    print "%x" % u8
    f.write( struct.pack('@B', u8))
f.close()
