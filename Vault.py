# Importing necessary libraries
import os
import shutil
import time
import json
import random as rd
from cryptography.fernet import Fernet
import pyperclip
from getpass import getpass

# Defining of constants
BACKUP_DIR='Backup'
PASSWD_FILE = 'passwd.json'
CARS_FILE = 'cars.txt'

# Subordinate Functions  
def conf(file=None, directory=None, target_dir='./'):
    if file:
        return os.path.exists(os.path.join(target_dir, file))
    elif directory:
        return os.path.exists(os.path.join(target_dir, directory))
    return False
def unlock():
    json_list=[]
    if conf(file=PASSWD_FILE):
        json_list.append(PASSWD_FILE)
    if PASSWD_FILE in json_list: 
        from cryptography.fernet import Fernet
        with open(CARS_FILE,'rb') as f:
            key=f.read()
        with open(PASSWD_FILE,'rb') as f:
            cont=f.read()
        cont_decr=json.loads(Fernet(key).decrypt(cont).decode())
        return cont_decr
    else:
        return 
def lock(passwd_dict):
    json_list=[]
    if conf(file=CARS_FILE):
        pass
    else:
        with open(CARS_FILE,'wb') as f:
            key = Fernet.generate_key()
            f.write(key)
        with open(PASSWD_FILE,'w') as file:
            file.write('')    
    if conf(file=PASSWD_FILE):
        json_list.append(PASSWD_FILE)
    if PASSWD_FILE in json_list: 
        with open(CARS_FILE,'rb') as f:
            key=f.read()
        cont=json.dumps(passwd_dict).encode('utf-8')
        cont_encr=Fernet(key).encrypt(cont)
        with open(PASSWD_FILE,'wb') as f:
            f.write(cont_encr)
            
    else:
        return        

def backup():
    if conf(directory='Backup'):
        shutil.copy(PASSWD_FILE, os.path.join(BACKUP_DIR, PASSWD_FILE))
        shutil.copy(CARS_FILE, os.path.join(BACKUP_DIR, CARS_FILE))
    else:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        shutil.copy(PASSWD_FILE, BACKUP_DIR)
        shutil.copy(CARS_FILE, BACKUP_DIR)


def securityQuiz():
    city=getpass('in which city were you born? '.upper()).lower()
    color=getpass('what is your favorite colour? '.upper()).lower()
    nick_name=getpass('what was your childhood nickname? '.upper()).lower()
    securityQuizDict = {'city':city,'color':color,'nick_name':nick_name}
    return securityQuizDict

# Main 
class essentials():
    json_list=[]
    if conf(file=PASSWD_FILE):
        json_list.append(PASSWD_FILE)
    if PASSWD_FILE in json_list:
        s=unlock()
        passwd_dict=s
    else:
        passwd_dict={}
    username=''    
   
    @classmethod  
    def memb(cls):
        passwd_dict=cls.passwd_dict
        json_list=[]
        if conf(file=PASSWD_FILE):
            json_list.append(PASSWD_FILE)
        if PASSWD_FILE in json_list: 
            username=input('enter your vault username: '.upper())
            cls.username=username
            vault_password=getpass('enter your vault password: '.upper())
            s=unlock()
            keys=[i for i in s.keys()]
            values=[i for i in s.values()]
            count=3
            while vault_password!=values[keys.index(username)] and count>0:
                print(f'incorrect password {count} more attempts remaining')
                vault_password=getpass('enter your vault password: '.upper())
                count-=1
                if count ==0:
                    print('answer the following security questions to reset your password'.upper())
                    [city,color,nick_name] = securityQuiz().values()
                    if color in values and city in values and nick_name in values:
                        new_passwd=getpass('enter your new password: '.upper())
                        new_passwd_conf=getpass('confirm your new password: '.upper())
                        count=0
                        while new_passwd != new_passwd_conf:
                            print('The password you entered do not match')
                            new_passwd=getpass('enter your new password: '.upper())
                            new_passwd_conf=getpass('confirm your new password: '.upper())
                            count+=1
                            if count==3:
                                print('maximum number of attempts reached'.upper())
                                quit()
                        else:
                            passwd_dict.pop(username)
                            passwd_dict.update({username:new_passwd})
                            print('password was reset succssefuly!!'.upper())
                            continue
                    else:
                        print('wrong details!!'.upper())
                        return False
            else:
                return True
    @classmethod            
    def new(cls):
        passwd_dict=cls.passwd_dict
        vault_user_name=input('enter your vault username: '.upper())
        cls.username = vault_user_name
        vault_pass = getpass('set your vault password: '.upper())
        conf_vault_pass=getpass('confirm your vault password: '.upper())
        count=3
        while conf_vault_pass!=vault_pass:
            print(f'password doesnt match please try again you have {count} more attempts'.upper())
            conf_vault_pass=getpass('confirm your vault password: '.upper())
            count-=1
            if count==0:
                print('too many attempts try again later'.upper())
                break 
        else:
            print('answer the following emergency questions'.upper())
            [city,color,nick_name]=securityQuiz().values()
            passwd_dict.update({vault_user_name:vault_pass,'nickname':nick_name,'city':city,'color':color})
            lock(passwd_dict)
            print('account succssefully created!'.upper()) 
        return True 

    @classmethod
    def act(cls):
        passwd_dict=cls.passwd_dict
        print(f'olaa, {cls.username} welcome to your vault'.upper())
        choice = ''
        while True:
            choice=input("would you like to 'retrieve' a password? ||'create' a new one? || 'exit' ? ".upper()).upper()
            if choice =='retrieve'.upper():
                account_type = input("'Email' address or 'account?' ".upper()).upper()
                if account_type == 'account'.upper():
                    acc=input('Enter the a/c: '.upper())
                    username=input('enter your username: '.upper())
                    bio=acc+' '+username
                    passwd_dict=unlock()
                    value=passwd_dict.get(bio,'invalid account or username')
                    if value == 'invalid account or username':
                        print(value.upper())
                    else:
                        pyperclip.copy(value)    
                        print(f'Your "{acc}" password for "{username}" has been copied to clipboard')
                elif account_type == 'Email address'.upper() or account_type=='email'.upper():
                    mail_address = input('Enter the e-mail address: '.upper())
                    bio = mail_address
                    s=unlock()
                    value=passwd_dict.get(bio,'invalid account or username')
                    if value == 'invalid account or username':
                        print(value.upper())
                    else:
                        pyperclip.copy(value)    
                        print(f'Your "{bio}" password has been copied to clipboard')
            elif choice=='create'.upper():
                choice=input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                if choice=='g':
                    lower='abcdefghijklmnopqrstuvwxyz'
                    upper=lower.upper()
                    number='0123456789'
                    symbols='!@#$%^&*'

                    al=lower+upper+number+symbols
                    length=16
                    password=''.join(rd.sample(al,length))
                elif choice == 'a':
                    password=getpass('enter the password: '.upper())
                    conf_pass=getpass('confirm your password: '.upper())
                    count=3
                    while conf_pass !=password:
                        print(f'passwords do not match,please try again {count} more attempts remaining'.upper())
                        password=getpass('enter the password: '.upper())
                        conf_pass=getpass('confirm your password: '.upper())
                        count-=1
                        if count==0:
                            print('maximum number of attempts exceeded,kindly try again later'.upper())
                            break  
                account_type = input("'Email' address or 'account'? ".upper()).upper()
                if account_type == 'account'.upper():
                    account=input('enter name of a/c: '.upper())
                    username=input('enter your username: '.upper())
                    bio=account+' '+username
                elif account_type == 'email address'.upper() or account_type=='email'.upper():
                    bio = input('Enter the e-mail address: '.upper())
                passwd_dict.update({bio:password})     
                pyperclip.copy(password)       
                print('your password has been copied to clipboard'.upper()) 
                lock(passwd_dict)   
                
            elif choice == 'exit'.upper():
                print('Your vault has been locked'.upper())
                time.sleep(2.2)
                break
            else:
                print('invalid input'.upper())

# Logic
def vault():
    try:
        if essentials.memb():
            essentials.act()
        elif essentials.memb()==None:
            essentials.new()
            essentials.act()
        elif essentials.memb() == False:
            print('The Vault Has Been Locked')
            return
    except UnboundLocalError:
        print('Wrong details last chance!'.upper())
        os.remove(CARS_FILE)
        os.remove(PASSWD_FILE)
        shutil.copy(os.path.join(BACKUP_DIR,PASSWD_FILE))
        shutil.copy(os.path.join(BACKUP_DIR,CARS_FILE))
        if essentials.memb():
            essentials.act()
        elif essentials.memb()==None:
            essentials.new()
            essentials.act()
        else:
            print('VAULT HAS BEEN LOCKED')
            return
    finally:
        backup()
# Running
if __name__ == '__main__':
    vault()    
