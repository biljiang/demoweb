# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 20:39:25 2018

@author: Feng
"""

from datetime import datetime
import urllib3
import certifi
import json
import rsa
from binascii import b2a_hex, a2b_hex
#from Crypto.Cipher import AES
#urllib3.disable_warnings()

def license_check():
    try: 
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        r = http.request('GET', 
                     'https://avarun.cn/static/license/ShangHaiAdressVerification/expirationdate.txt')
        if r.status==200:
            Ex_time=datetime.strptime(r.data.decode(),'%Y-%m-%d %H:%M:%S\n')
            if datetime.now()<Ex_time:
                return("your license status is good!")
            else:
                return("your license is expired!")
                
        else:
            return("fail to get license file.")
    except:
        return("Network error.")

class rsadecrypt():
    def __init__(self, prikey):
        self.prikey = prikey

    def decrypt(self, text):
        # 因为rsa加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串        
        decrypt_text = rsa.decrypt(a2b_hex(text), self.prikey)
        return decrypt_text
    
def lic_loc_chk():
    with open('static/license_check/private.pem','r') as f:
        prikey = rsa.PrivateKey.load_pkcs1(f.read().encode()) 
        
    with open('static/license_check/ency.lic','r') as f:
        ency_lic= f.read()
        
    rs_de_obj = rsadecrypt (prikey)
    lic_str = rs_de_obj.decrypt(ency_lic.encode()).decode()
    lic = json.loads(lic_str)    
    Ex_date = datetime.strptime(lic["Expiration"],'%Y-%m-%d')
    if datetime.now()<Ex_date:
        return("your license local check is good!")
    else:
        return("your license local check expired!")    

if __name__=='__main__':
   print (license_check())
   print (lic_loc_chk())
    
