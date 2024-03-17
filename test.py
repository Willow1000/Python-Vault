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
    print(status)

conf(directory='Kali',target_dir='D:\Downloads')