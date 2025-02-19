from Crypto.Protocol.KDF import PBKDF2
from cryptography.fernet import Fernet
from Crypto import Random
import base64


salt = Random.new().read(8)


def encrypt(pwd, msg):

	"""
	param pwd: password or passphrase (type: str)
	param msg: message to encrypt (type: str or bytes) 
	
	return base64 encoded encrypted message
	"""
	
	try:
		msg = msg.encode()
	
	except:
		pass
	
	key = PBKDF2(pwd, salt, 32)
	
	key = base64.urlsafe_b64encode(key)
	
	f = Fernet(key)
	
	e = f.encrypt(msg)

	return base64.b64encode(e)
	
def decrypt(pwd, msg):
	
	"""
	param pwd: password or passphrase (type: str)
	param msg: message to uncrypt (type: bytes) 
	
	return uncrypted decoded message (str)
	"""
	
	msg = base64.b64decode(msg)
	
	key = PBKDF2(pwd, salt, 32)
	
	key = base64.urlsafe_b64encode(key)
	
	f = Fernet(key)
	
	d = f.decrypt(msg)
	
	return d.decode()