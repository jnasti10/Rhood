import pyotp
import time

totp = pyotp.TOTP("R4TFYIX5HPKIHS7R").now()
print(totp)
