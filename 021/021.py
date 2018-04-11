#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180412
#通常，登陆某个网站或者 APP，需要使用用户名和密码。密码是如何加密后存储起来的呢？请使用 Python 对密码加密。
'''

import hashlib,random

def encrypt_passwd(passwd,salt=None):    
    if salt==None:
        salt = ''.join(random.sample('01234567890abcdefghigABCDEFGHI', 10))
    else:
        salt = salt
    m = hashlib.md5()
    m.update(passwd + salt)
    passwd = m.hexdigest()
    return salt+passwd
 
def validate_password(hashed, password):  
    return hashed == encrypt_passwd(password,hashed[:10])
    
    

if __name__ == "__main__":
    password_new = raw_input("Set your password\n")
    password_saved = encrypt_passwd(password_new)
    password_again = raw_input("Now,type in your password\n")
    print "Yes,you got it." if validate_password(password_saved, password_again) else "No,it's wrong."
