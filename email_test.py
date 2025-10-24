import gmail

email_id="karan.sharma.433215@gmail.com"
app_pass="mmoi yejo irnz vndx"

def send_openacn_ack(uemail,uname,uacn,upass):
    con=gmail.GMail(email_id,app_pass)
    upass=upass.replace(' ','')
    sub="Congrates!! your account has been opened..."
    utext=f'''Hello {uname} !
    Welcome to ABC Bank
    your account no is {uacn}
    your password is {upass}
    kindly change your password when you login first

    thank you 
    ABC Bank 
    Noida
    '''
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)

def send_otp(uemail,otp,amt):
    con=gmail.GMail(email_id,app_pass)
    sub="otp for fund transfer..."
    utext=f""" Your otp is {otp} to transfer amount {amt}
kindly use this otp to complete transfer
please , dont share it to anyone else 

Thanks 
ABC Bank
Noida"""
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)

def send_otp_4_pass(uemail,otp):
    con=gmail.GMail(email_id,app_pass)
    sub="otp for password recovery"
    
    utext=f"""Your otp is {otp} to recover password
Please don't share to anyone else

Thanks
ABC Bank
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)