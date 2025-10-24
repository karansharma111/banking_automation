import random

def captcha():
    a=str(random.randint(0,9))
    b=chr(random.randint(65,81))
    c=str(random.randint(0,9))
    d=chr(random.randint(97,122))

    values=' '+a+' '+b+' '+c+' '+d+' '
    return values

