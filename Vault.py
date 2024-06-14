def conf(file=None,directory=None,target_dir='./'):
    import os
    status = False
    if file !=None:
        for root,directory,files in os.walk(target_dir):
            for f in files:
                if file in f:
                    status=True
    elif directory !=None:
        for root,directories,files in os.walk(target_dir):
            for d in directories:
                if directory in directories:
                    status=True
    return status

def lock():
    import os
    from cryptography.fernet import Fernet
    json_list=[]
    if conf(file='cars.txt'):
        pass
    else:
        with open('cars.txt','wb') as f:
            key = Fernet.generate_key()
            f.write(key)
    if conf(file='passwd.json'):
        json_list.append('passwd.json')
    if 'passwd.json' in json_list: 
        with open('cars.txt','rb') as f:
            key=f.read()
        with open('passwd.json','rb') as f:
            cont=f.read()
        cont_encr=Fernet(key).encrypt(cont)
        with open('passwd.json','wb') as f:
            f.write(cont_encr)
    else:
        return        


def unlock():
    import os
    json_list=[]
    if conf(file='passwd.json'):
        json_list.append('passwd.json')
    if 'passwd.json' in json_list: 
        from cryptography.fernet import Fernet
        with open('cars.txt','rb') as f:
            key=f.read()
        with open('passwd.json','rb') as f:
            cont=f.read()
        cont_decr=Fernet(key).decrypt(cont).decode()
        with open('passwd.json','w') as f:
            f.write(cont_decr)
    else:
        return         

def backup():
    import os
    import shutil
    if conf(directory='Backup'):
        with open('./passwd.json','rb') as f:
            cont_passwd_json = f.read()
        with open('./Backup/passwd.json','wb') as f:
            f.write(cont_passwd_json)    
        with open('./cars.txt', 'rb') as f:
            cont_cars_txt = f.read()    
        with open('./Backup/cars.txt','wb') as f:
            f.write(cont_cars_txt)   
    else:
        os.makedirs('./Backup')
        shutil.copy('./passwd.json','./Backup')         
        shutil.copy('./cars.txt','./Backup')   

unlock()
class essentials():
    import os
    import json
    json_list=[]
    if conf(file='passwd.json'):
        json_list.append('passwd.json')
    if 'passwd.json' in json_list:
        with open('passwd.json','r') as f:
            s=json.load(f)
            passwd_dict=s
    else:
        passwd_dict={}
    username=''    
   
    @classmethod  
    def memb(cls):
        import os
        import json
        passwd_dict=cls.passwd_dict
        json_list=[]
        if conf(file='passwd.json'):
            json_list.append('passwd.json')
        if 'passwd.json' in json_list: 
            username=input('enter your vault username: '.upper())
            cls.username=username
            
            vault_password=input('enter your vault password: '.upper())
            with open('passwd.json','r') as f:
                s=json.load(f)
                keys=[i for i in s.keys()]
                values=[i for i in s.values()]
                count=3

                while vault_password!=values[keys.index(username)] and count>0:
                    print(f'incorrect password {count} more attempts remaining')
                    vault_password=input('enter your vault password: '.upper())
                    count-=1
                    if count ==0:
                        print('answer the following security questions to reset your password'.upper())
                        city=input('in which city were you born? '.upper()).lower()
                        color=input('what is your favorite colour? '.upper()).lower()
                        nick_name=input('what was your childhood nickname? '.upper()).lower()
                        if color in values and city in values and nick_name in values:
                            new_passwd=input('enter your new password: '.upper())
                            new_passwd_conf=input('confirm your new password: '.upper())
                            count=0
                            while new_passwd != new_passwd_conf:
                                print('The password you entered do not match')
                                new_passwd=input('enter your new password: '.upper())
                                new_passwd_conf=input('confirm your new password: '.upper())
                                count+=1
                                if count==3:
                                    print('maximum number of attempts reached'.upper())
                                    quit()
                            else:
                                with open('passwd.json','w+') as f:
                                    passwd_dict.pop(username)
                                    passwd_dict.update({username:new_passwd})
                                    json.dump(passwd_dict,f,indent=4,sort_keys=True)
                                    print('password was reset succssefuly!!'.upper())
                                    continue

                        else:
                            print('kindly try again later')
                            break

                else:
                    return True
    @classmethod            
    def new(cls):
        import json
        passwd_dict=cls.passwd_dict
        vault_user_name=input('enter your vault username: '.upper())
        cls.username = vault_user_name
        vault_pass = input('set your vault password: '.upper())
        conf_vault_pass=input('confirm your vault password: '.upper())
        count=3
        while conf_vault_pass!=vault_pass:
            print(f'password doesnt match please try again you have {count} more attempts'.upper())
            conf_vault_pass=input('confirm your vault password: '.upper())
            count-=1
            if count==0:
                print('too many attempts try again later'.upper())
                break 

        else:

            print('answer the following emergency questions'.upper())
            nick_name=input('what was your childhood nickname? '.upper()).lower()
            city=input('in which city were you born? '.upper()).lower()
            color=input('what is your favorite colour? '.upper()).lower()
            passwd_dict.update({vault_user_name:vault_pass,'nickname':nick_name,'city':city,'color':color})
            with open('passwd.json','w+') as file:
                json.dump(passwd_dict,file)
            print('account succssefully created!'.upper()) 
        return True 

    @classmethod
    def act(cls):
        import json
        import random as rd 
        from time import sleep
        
        passwd_dict=cls.passwd_dict
        print(f'olaa, {cls.username} welcome to your vault'.upper())
        choice = ''
        while True:
            choice=input('would you like to retrieve a password? ||create a new one? || exit"? '.upper()).upper()
            if choice =='retrieve'.upper():
                account_type = input('Email address or account? '.upper()).upper()
                if account_type == 'account'.upper():
                    acc=input('Enter the a/c: '.upper())
                    username=input('enter your username: '.upper())
                    bio=acc+' '+username
                elif account_type == 'Email address'.upper() or account_type=='email'.upper():
                    mail_address = input('Enter the e-mail address: '.upper())
                    bio = mail_address
                    m = mail_address
                next    #For 'shielding' to prevent the next block of code from being treated as an else
                with open('passwd.json','r') as f:
                    s=json.load(f)
                    m=s.get(bio,'invalid account or username')
                    if m == 'invalid account or username':
                        print(m.upper())
                    else:    
                        print(f'Your "{bio}" password is {m}')
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
                    password=input('enter the password: '.upper())
                    conf_pass=input('confirm your password: '.upper())
                    count=3
                    while conf_pass !=password:
                        print(f'passwords do not match,please try again {count} more attempts remaining'.upper())
                        password=input('enter the password: '.upper())
                        conf_pass=input('confirm your password: '.upper())
                        count-=1
                        if count==0:
                            print('maximum number of attempts exceeded,kindly try again later'.upper())
                            break  
                account_type = input('Email address or account? '.upper()).upper()
                if account_type == 'account'.upper():
                    account=input('enter name of a/c: '.upper())
                    username=input('enter your username: '.upper())
                    bio=account+' '+username
                elif account_type == 'email address'.upper() or account_type=='email'.upper():
                    bio = input('Enter the e-mail address: '.upper())
                passwd_dict.update({bio:password})
                with open('passwd.json','w+') as f:
                    json.dump(passwd_dict,f)             
                print(f'YOUR PASSWORD IS: {password}')    
                
            elif choice == 'exit'.upper():
                print('Your vault has been locked'.upper())
                sleep(3)
                break
            else:
                print('invalid input'.upper())

                 
            
lock()



def vault():
    try:
        unlock()
        if essentials.memb():
            essentials.act()
            lock()
            backup()
        elif essentials.memb()==None:
            essentials.new()
            essentials.act()
            lock()
            backup()
        else:
            lock()
            backup()
    except UnboundLocalError:
        print('Wrong details last chance!!'.upper())
        import shutil
        import os
        os.remove('./cars.txt')
        os.remove('./passwd.json')
        shutil.copy('./Backup/passwd.json','./')
        shutil.copy('./Backup/cars.txt','./')
        unlock()
        if essentials.memb():
            essentials.act()
            lock()
            backup()
        elif essentials.memb()==None:
            essentials.new()
            essentials.act()
            lock()
            backup()
        else:
            lock()
            backup()
vault()    
