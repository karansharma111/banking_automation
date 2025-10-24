from tkinter import Tk,Label,Entry,Button,messagebox,Frame,ttk
import sqlite3 , time,random
from tkinter.ttk import Combobox
from gen_captcha import captcha
from PIL import Image,ImageTk
from table_creation import generate
import sqlite3
from email_test import send_openacn_ack,send_otp,send_otp_4_pass
import re

generate()

def show_dt():
    dt=time.strftime("%A %d-%b-%Y %r")
    lbl_dt.configure(text=dt)
    lbl_dt.after(1000,show_dt)

list_img=['images/logo.jpg','images/logo1.jpg','images/logo2.png','images/logo3.jpg','images/logo4.jpg']
def img_animation():
    index=random.randint(0,4)
    img=Image.open(list_img[index]).resize((170,100))
    imgtk=ImageTk.PhotoImage(img,master=root)
    img_lbl=Label(root,image=imgtk)
    img_lbl.place(relx=0,rely=0)
    img_lbl.image=imgtk
    img_lbl.after(1500,img_animation)

root=Tk()
root.state('zoomed')
root.configure(bg='pink',highlightthickness=10,highlightcolor='magenta')

lbl_title=Label(root,text="Banking Automation ",font=('verdna',40,'underline'),bg='pink',fg='blue')
lbl_title.pack()

lbl_dt=Label(root,font=('Arial',10,'bold'),bg="pink")
lbl_dt.pack(pady=10)
show_dt()

img=Image.open("images/logo.jpg").resize((170,100))
imgtk=ImageTk.PhotoImage(img,master=root)

img_lbl=Label(root,image=imgtk)
img_lbl.place(relx=0,rely=0)
img_animation()

lbl_footer=Label(root,text=" Developed By :\nKaran Sharma @8178673404",font=('verdna',15),bg="pink")
lbl_footer.pack(side='bottom')

code_captcha=captcha()

def main_screen():

    def refresh():
        global code_captcha
        code_captcha=captcha()
        lbl_captcha_gen.configure(text=code_captcha)

    frm=Frame(root,highlightbackground='blue',highlightthickness=2,highlightcolor='blue')
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=0.77)
    
    def forgot():
         frm.destroy()
         fp_screen()

    def login():
        utype = e_acn.get()
        uacnno=e_acn_no.get()
        upass=e_pass.get()

        ucaptcha=e_enter_captcha.get()
        global code_captcha
        code_captcha=code_captcha.replace(' ','')

        if utype=='Admin':
            if uacnno=='0' and upass=='admin':
                if code_captcha==ucaptcha:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror("Login","Invalid captcha")
            else:
                messagebox.showerror("Login","You are not Admin!")
        else:
            
            if code_captcha==ucaptcha:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                query='select * from accounts where acn_acno=? and acn_pass=?'
                curobj.execute(query,(uacnno,upass))
                row=curobj.fetchone()
                if row==None:
                    messagebox.showerror("Login","invalid ACN/PASS")
                else:
                    frm.destroy()
                    user_screen(row[0],row[1])
            else:
                 messagebox.showerror("Login","Invalid captcha")

    lbl_acn=Label(frm,text="Acc_type",font=('verdna',20),bg='powderblue')
    lbl_acn.place(relx=0.3,rely=0.1)

    e_acn=Combobox(frm,values=['User','Admin'],font=('Arial',19))
    e_acn.current(0)
    e_acn.place(relx=0.45,rely=0.1)

    lbl_acn_no=Label(frm,text='Acc No',font=('verdna',20),bg='powderblue')
    lbl_acn_no.place(relx=0.3,rely=0.2)

    e_acn_no=Entry(frm,font=('Arial',20),bd=4)
    e_acn_no.place(relx=0.45,rely=0.2)
    e_acn_no.focus()

    lbl_pass=Label(frm,text='Password',bg='powderblue',font=('verdna',20))
    lbl_pass.place(relx=0.3,rely=0.3)

    e_pass=Entry(frm,font=('Arial',20),bd=4,show='*')
    e_pass.place(relx=0.45,rely=0.3)

    lbl_captcha=Label(frm,text='Captcha',bg='powderblue',font=('verdna',20))
    lbl_captcha.place(relx=0.3,rely=0.4)

    lbl_captcha_gen=Label(frm,text=code_captcha,font=('Arial',20),fg='green')
    lbl_captcha_gen.place(relx=0.45,rely=0.4)

    refresh_button=Button(frm,text='refresh',font=('Arial',10),command=refresh,bg='light green')
    refresh_button.place(relx=0.54,rely=0.4)

    lbl_enter_captcha=Label(frm,text='Enter Captcha',bg='powderblue',font=('verdna',20))
    lbl_enter_captcha.place(relx=0.3,rely=0.5)

    e_enter_captcha=Entry(frm,font=('Arial',20),bd=4)
    e_enter_captcha.place(relx=0.45,rely=0.5)

    submit_btn=Button(frm,text='Login',font=('verdna',18),bd=4,bg='green',fg='white',command=login)
    submit_btn.place(relx=0.3,rely=0.6,relwidth=0.4)

    create_btn=Button(frm,text='Create Acc',font=('verdna',18),bd=4,bg='blue',fg='white',command=create_screen)
    create_btn.place(relx=0.3,rely=0.72,relwidth=0.19)

    forget_btn=Button(frm,text='Forgot Pass',font=('verdna',18),bd=4,bg='red',fg='white',command=forgot)
    forget_btn.place(relx=0.51,rely=0.72,relwidth=0.19)

def fp_screen():
    frm=Frame(root,highlightbackground='red',highlightthickness=2,highlightcolor='red')
    frm.configure(bg='orange')
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=0.77)

    def back():
        frm.destroy()
        main_screen()

    def fp_pass():
        ueamil=e_email.get()
        uacn=e_acn_no.get()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where acn_acno=?'
        curobj.execute(query,(uacn,))
        torow=curobj.fetchone()
        if torow==None:
            messagebox.showerror("Forgot Password","ACN does not exist")
        else:
            if ueamil==torow[3]:
                otp=random.randint(1000,9999)
                send_otp_4_pass(ueamil,otp)
                messagebox.showinfo("Forgot Pasword","Otp sent to registered email,kindly verify")
                def verify_otp(): 
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query='select acn_pass from accounts where acn_acno=?'
                            curobj.execute(query,(uacn,))
                            
                            messagebox.showinfo('Forgot Password',f"Your Password is {curobj.fetchone()[0]} ")
                            conobj.close()
                            frm.destroy()
                            main_screen()
                        else:
                            messagebox.showerror("Forgot Password","Invalid otp!")

                otp_e=Entry(frm,font=('Arial',20,'bold'),bd=5)
                otp_e.place(relx=.4,rely=.6)
                otp_e.focus()

                verify_btn=Button(frm,command=verify_otp,text="verify",bg='green',fg='white',bd=3,font=('Arial',15))
                verify_btn.place(relx=.7,rely=.6)

            else:
                messagebox.showerror("Forgot Password","Email is not matched")

    back_btn=Button(frm,text="Back",font=('Arial',15),command=back)
    back_btn.place(relx=0,rely=0)

    lbl_acn_no=Label(frm,text='Acc No',font=('verdna',20),bg='orange')
    lbl_acn_no.place(relx=0.3,rely=0.2)

    e_acn_no=Entry(frm,font=('Arial',20),bd=4)
    e_acn_no.place(relx=0.45,rely=0.2)
    e_acn_no.focus()

    lbl_email=Label(frm,text='Email',font=('verdna',20),bg='orange')
    lbl_email.place(relx=0.3,rely=0.3)

    e_email=Entry(frm,font=('Arial',20),bd=4)
    e_email.place(relx=0.45,rely=0.3)
    e_email.focus()

    submit_btn=Button(frm,text='Submit',command=fp_pass,font=('verdna',18),bd=4,bg='green',fg='white')
    submit_btn.place(relx=0.3,rely=0.5,relwidth=0.4)
   
def admin_screen():
    frm=Frame(root,highlightbackground='green',highlightthickness=2,highlightcolor='green')
    frm.configure(bg='light green')
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=0.77)

    def back():
        frm.destroy()
        main_screen()

        back_btn=Button(frm,text="Back",font=('Arial',15),command=back)
        back_btn.place(relx=0,rely=0)

    def open():
        infrm=Frame(frm,highlightbackground='blue',highlightthickness=2)
        infrm.place(relx=0.27,rely=0.1,relheight=0.8,relwidth=0.7)

        h_lbl=Label(infrm,text='Open Account Window',font=('verdna',15,'bold'),fg='purple')
        h_lbl.place(relx=0.4,rely=0.01)

        def openac():
            uname=name_e.get()
            uemail=email_e.get()
            umob=mob_e.get()
            uadhar=adhar_e.get()
            uadr=adr_e.get()
            udob=dob_e.get()
            upass=captcha()
            upass=upass.replace(' ','')
            ubal=0
            uopendate=time.strftime("%A %d-%b-%Y")

            #empty validation
            if len(uname)==0 or len(uemail)==0 or len(umob)==0 or len(uadhar)==0 or len(uadr)==0 or len(udob)==0:
                messagebox.showerror("Open Account","Empty fields are not allowed")
                return

            #email validation
            match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]+",uemail)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of email")
                return
                
            #mob validation
            match=re.fullmatch("[6-9][0-9]{9}",umob)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of mob")
                return
                
            #mob adhar
            match=re.fullmatch("[0-9]{12}",uadhar)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of adhar")
                return
                

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into accounts values(null,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query,(uname,upass,uemail,umob,uadhar,uadr,udob,ubal,uopendate))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute("select max(acn_acno) from accounts")
            uacn=curobj.fetchone()[0]
            conobj.close()
            send_openacn_ack(uemail,uname,uacn,upass)
            messagebox.showinfo("Account","Account Opened and details sent to email")
            frm.destroy()
            admin_screen()

        name_lbl=Label(infrm,text="Name",font=('Arial',18))
        name_lbl.place(relx=0.01,rely=0.2)

        name_e=Entry(infrm,font=('verdna',18),bd=4)
        name_e.place(relx=0.1,rely=0.2)

        mob_lbl=Label(infrm,text="Mob",font=('Arial',18))
        mob_lbl.place(relx=0.01,rely=0.4)

        mob_e=Entry(infrm,font=('verdna',18),bd=4)
        mob_e.place(relx=0.1,rely=0.4)

        adhar_lbl=Label(infrm,text="Aadhar",font=('Arial',18))
        adhar_lbl.place(relx=0.01,rely=0.6)

        adhar_e=Entry(infrm,font=('verdna',18),bd=4)
        adhar_e.place(relx=0.1,rely=0.6)

        dob_lbl=Label(infrm,text="DOB",font=('Arial',18))
        dob_lbl.place(relx=0.5,rely=0.2)

        dob_e=Entry(infrm,font=('verdna',18),bd=4)
        dob_e.place(relx=0.6,rely=0.2)

        email_lbl=Label(infrm,text="Email",font=('Arial',18))
        email_lbl.place(relx=0.5,rely=0.4)

        email_e=Entry(infrm,font=('verdna',18),bd=4)
        email_e.place(relx=0.6,rely=0.4)

        adr_lbl=Label(infrm,text="Address",font=('Arial',18))
        adr_lbl.place(relx=0.5,rely=0.6)

        adr_e=Entry(infrm,font=('verdna',18),bd=4)
        adr_e.place(relx=0.6,rely=0.6)

        open_btn=Button(frm,text='Open',command=openac,font=('verdna',18),bd=4,bg='light green',fg='black')
        open_btn.place(relx=0.57,rely=0.7)


    def close_acc():
        infrm=Frame(frm,highlightbackground='blue',highlightthickness=2)
        infrm.place(relx=0.27,rely=0.1,relheight=0.8,relwidth=0.7)

        h_lbl=Label(infrm,text='Close Account Window',font=('verdna',15,'bold'),fg='purple')
        h_lbl.place(relx=0.4,rely=0.01)

        def sent_close_otp():
            uacn=acnno_e.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(uacn,))
            torow=curobj.fetchone()
            if torow==None:
                messagebox.showerror("Close Account","ACN does not exist")
            else:
                otp=random.randint(1000,9999)
                send_otp_4_pass(torow[3],otp)
                messagebox.showinfo("close Account","Otp sent to registered email,kindly verify")
                def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query='delete from accounts where acn_acno=?'
                            curobj.execute(query,(uacn,))
                            
                            messagebox.showinfo('Close Account',"Account Closed ")
                            conobj.commit()
                            conobj.close()
                            frm.destroy()
                            admin_screen()
                        else:
                            messagebox.showerror("Close Account","Invalid otp!")

                otp_e=Entry(frm,font=('Arial',20,'bold'),bd=5)
                otp_e.place(relx=.4,rely=.6)
                otp_e.focus()

                verify_btn=Button(frm,command=verify_otp,text="verify",bg='pink',bd=3,font=('Arial',15))
                verify_btn.place(relx=.8,rely=.6)

        lbl_acn_no=Label(frm,text='Acc No',font=('verdna',20))
        lbl_acn_no.place(relx=0.3,rely=0.2)

        acnno_e=Entry(frm,font=('Arial',20),bd=4)
        acnno_e.place(relx=0.45,rely=0.2)
        acnno_e.focus()

        send_otp_btn=Button(frm,text='Send OTP',font=('verdna',18),bd=4,bg='light green',fg='black')
        send_otp_btn.place(relx=0.57,rely=0.3)

        lbl_otp=Label(frm,text='Enter otp',font=('verdna',20))
        lbl_otp.place(relx=0.3,rely=0.5)

        e_otp=Entry(frm,font=('Arial',20),bd=4)
        e_otp.place(relx=0.45,rely=0.5)
        e_otp.focus()

        close_btn=Button(frm,text='Close',font=('verdna',18),bd=4,bg='light green',fg='black',command=sent_close_otp)
        close_btn.place(relx=0.61,rely=0.6)



            

    def view():
        infrm=Frame(frm,highlightbackground='blue',highlightthickness=2)
        infrm.place(relx=0.27,rely=0.1,relheight=0.8,relwidth=0.7)

        h_lbl=Label(infrm,text='View Accounts Window',font=('verdna',15,'bold'),fg='purple')
        h_lbl.place(relx=0.4,rely=0.01)

        tree = ttk.Treeview(infrm, columns=("A","B","C","D","E","F"), show="headings")
        tree.heading("A", text="ACN0.")
        tree.heading("B", text="NAME")
        tree.heading("C", text="Email")
        tree.heading("D", text="MOB")
        tree.heading("E", text="OPEN DATE")
        tree.heading("F", text="BALANCE")

        tree.column("A", width=100,anchor="center")
        tree.column("B", width=150,anchor="center")
        tree.column("C", width=200,anchor="center")
        tree.column("D", width=100,anchor="center")
        tree.column("E", width=100,anchor="center")
        tree.column("F", width=100,anchor="center")
        
        
        tree.place(relx=.1,rely=.1,relwidth=.8,relheight=.4) 

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select acn_acno,acn_name,acn_email,acn_mob,acn_opendate,acn_bal from accounts'
        curobj.execute(query)
        for tup in curobj.fetchall():
            tree.insert("", "end", values=tup)
        conobj.close()

    lbl_acn_no=Label(frm,text='Acc No',font=('verdna',20))
    lbl_acn_no.place(relx=0.3,rely=0.2)

    e_acn_no=Entry(frm,font=('Arial',20),bd=4)
    e_acn_no.place(relx=0.45,rely=0.2)
    e_acn_no.focus()

    send_otp_btn=Button(frm,text='Send OTP',font=('verdna',18),bd=4,bg='light green',fg='black')
    send_otp_btn.place(relx=0.57,rely=0.3)

    lbl_otp=Label(frm,text='Enter otp',font=('verdna',20))
    lbl_otp.place(relx=0.3,rely=0.5)

    e_otp=Entry(frm,font=('Arial',20),bd=4)
    e_otp.place(relx=0.45,rely=0.5)
    e_otp.focus()

    view_btn=Button(frm,text='View',font=('verdna',18),bd=4,bg='light green',fg='black')
    view_btn.place(relx=0.61,rely=0.6)


    open_btn=Button(frm,text='Open Acc',font=('verdna',18),bd=4,bg='blue',fg='white',command=open)
    open_btn.place(relx=0.05,rely=0.2,relwidth=0.19)

    close_btn=Button(frm,text='Close Acc',font=('verdna',18),bd=4,bg='blue',fg='white',command=close_acc)
    close_btn.place(relx=0.05,rely=0.4,relwidth=0.19)

    view_btn=Button(frm,text='View',font=('verdna',18),bd=4,bg='blue',fg='white',command=view)
    view_btn.place(relx=0.05,rely=0.6,relwidth=0.19)

def create_screen():
    frm=Frame(root,highlightbackground='blue',highlightthickness=2,highlightcolor='blue')
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=0.77)

    def back():
        frm.destroy()
        main_screen()

    back_btn=Button(frm,text="Back",font=('Arial',15),command=back)
    back_btn.place(relx=0,rely=0)

    infrm=Frame(frm,highlightbackground='blue',highlightthickness=2)
    infrm.place(relx=0.2,rely=0.1,relheight=0.8,relwidth=0.7)

    h_lbl=Label(infrm,text='Sorry!! \n only admin can create account...',font=('verdna',15,'bold'),fg='purple')
    h_lbl.place(relx=0.4,rely=0.3)


def user_screen(uacno,uname):
    frm=Frame(root,highlightbackground='green',highlightthickness=2,highlightcolor='green')
    frm.configure(bg='light green')
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=0.77)

    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    query='select * from accounts where acn_acno=?'
    curobj.execute(query,(uacno,))
    row=curobj.fetchone()
    conobj.close()

    def back():
        frm.destroy()
        main_screen()

    back_btn=Button(frm,text="Back",font=('Arial',15),command=back)
    back_btn.place(relx=0,rely=0)

    h_lbl=Label(frm,text=f'Welcome, {row[1]}',font=('verdna',15,'bold'),fg='purple',bg='light green')
    h_lbl.place(relx=0.4,rely=0.01)

    def check_details():
            infrm=Frame(frm,highlightbackground='blue',highlightthickness=2)
            infrm.place(relx=0.27,rely=0.1,relheight=0.8,relwidth=0.7)

            h_lbl=Label(infrm,text='Detail Window',font=('verdna',15,'bold'),fg='purple')
            h_lbl.place(relx=0.4,rely=0.01)

            acn_lbl=Label(infrm,text=f"Account No.\t=\t{row[0]}",font=('verdna',15),fg='black')
            acn_lbl.place(relx=0.1,rely=0.2)

            bal_lbl=Label(infrm,text=f"Account Balance\t=\t{row[8]}",font=('verdna',15),fg='black')
            bal_lbl.place(relx=0.1,rely=0.3)

            aadhar_lbl=Label(infrm,text=f"Aadhar No.\t=\t{row[5]}",font=('verdna',15),fg='black')
            aadhar_lbl.place(relx=0.1,rely=0.4)

            open_date_lbl=Label(infrm,text=f"Opened Date\t=\t{row[9]}",font=('verdna',15),fg='black')
            open_date_lbl.place(relx=0.1,rely=0.5)

            dob_lbl=Label(infrm,text=f"Date Of Birth\t=\t{row[7]}",font=('verdna',15),fg='black')
            dob_lbl.place(relx=0.1,rely=0.6)

    check_btn=Button(frm,text='Check Details',font=('verdna',18),bd=4,bg='blue',fg='white',command=check_details)
    check_btn.place(relx=0.05,rely=0.2,relwidth=0.19)

    def update_details():
            infrm=Frame(frm,highlightbackground='blue',highlightthickness=2)
            infrm.place(relx=0.27,rely=0.1,relheight=0.8,relwidth=0.7)

            h_lbl=Label(infrm,text='Update Window',font=('verdna',15,'bold'),fg='purple')
            h_lbl.place(relx=0.4,rely=0.01)

            def Update():
                uname=name_e.get()
                uemail=email_e.get()
                umob=mob_e.get()
                upass=e_pass.get()

                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                query='update accounts set acn_name=?,acn_pass=?,acn_email=?,acn_mob=? where acn_acno=?'
                curobj.execute(query,(uname,upass,uemail,umob,uacno))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Update","Deatails Updated")
                frm.destroy()
                user_screen(None,uacno)

            name_lbl=Label(infrm,text="Name",font=('Arial',18))
            name_lbl.place(relx=0.01,rely=0.2)

            name_e=Entry(infrm,font=('verdna',18),bd=4)
            name_e.place(relx=0.1,rely=0.2)
            name_e.insert(0,row[1])

            mob_lbl=Label(infrm,text="Mob",font=('Arial',18))
            mob_lbl.place(relx=0.01,rely=0.4)

            mob_e=Entry(infrm,font=('verdna',18),bd=4)
            mob_e.place(relx=0.1,rely=0.4)
            mob_e.insert(0,row[4])

            lbl_pass=Label(infrm,text='Password',font=('Arial',18))
            lbl_pass.place(relx=0.5,rely=0.2)

            e_pass=Entry(infrm,font=('verdna',18),bd=4)
            e_pass.place(relx=0.65,rely=0.2)
            e_pass.insert(0,row[2])

            email_lbl=Label(infrm,text="Email",font=('Arial',18))
            email_lbl.place(relx=0.5,rely=0.4)

            email_e=Entry(infrm,font=('verdna',18),bd=4)
            email_e.place(relx=0.65,rely=0.4)
            email_e.insert(0,row[3])

            open_btn=Button(infrm,text='Update',command=Update,font=('verdna',18),bd=4,bg='light green',fg='black')
            open_btn.place(relx=0.57,rely=0.7)

            

    update_btn=Button(frm,text='Update Details',font=('verdna',18),bd=4,bg='blue',fg='white',command=update_details)
    update_btn.place(relx=0.05,rely=0.35,relwidth=0.19)

    def deposite():
            infrm=Frame(frm,highlightbackground='blue',highlightthickness=2)
            infrm.place(relx=0.27,rely=0.1,relheight=0.8,relwidth=0.7)

            h_lbl=Label(infrm,text='Deposite Window',font=('verdna',15,'bold'),fg='purple')
            h_lbl.place(relx=0.4,rely=0.01)

            amt_lbl=Label(infrm,text='Amount',font=('verdna',20))
            amt_lbl.place(relx=0.15,rely=0.2)

            amt_e=Entry(infrm,font=('verdna',20),bd=4)
            amt_e.place(relx=0.4,rely=0.2)

            def deposite_amt():
                uamt=float(amt_e.get())
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                query='update accounts set acn_bal=acn_bal+? where acn_acno=?'
                curobj.execute(query,(uamt,uacno))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Deposite",f"{uamt}Amount Deposited")
                frm.destroy()
                user_screen(None,uacno)


            deposite_btn=Button(infrm,text='Deposite',font=('verdna',18),bd=4,bg='green',fg='white',command=deposite_amt)
            deposite_btn.place(relx=0.54,rely=0.5,relwidth=0.19)

    deposite_btn=Button(frm,text='Deposite',font=('verdna',18),bd=4,bg='blue',fg='white',command=deposite)
    deposite_btn.place(relx=0.05,rely=0.5,relwidth=0.19)

    def withdraw():
            infrm=Frame(frm,highlightbackground='blue',highlightthickness=2)
            infrm.place(relx=0.27,rely=0.1,relheight=0.8,relwidth=0.7)

            h_lbl=Label(infrm,text='Withdraw Window',font=('verdna',15,'bold'),fg='purple')
            h_lbl.place(relx=0.4,rely=0.01)

            amt_lbl=Label(infrm,text='Amount',font=('verdna',20))
            amt_lbl.place(relx=0.15,rely=0.2)

            amt_e=Entry(infrm,font=('verdna',20),bd=4)
            amt_e.place(relx=0.4,rely=0.2)

            def withdraw_amt():
                uamt=float(amt_e.get())
                if row[8]>uamt:
                    conobj=sqlite3.connect(database="bank.sqlite")
                    curobj=conobj.cursor()
                    query='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                    curobj.execute(query,(uamt,uacno))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Withdraw",f"{uamt} Amount withdrawn")
                    frm.destroy()
                    user_screen(None,uacno)

                else:
                    messagebox.showerror("Withdraw","insufficient amount")
                                     

            deposite_btn=Button(infrm,text='Withdraw',font=('verdna',18),bd=4,bg='green',fg='white',command=withdraw_amt)
            deposite_btn.place(relx=0.54,rely=0.5,relwidth=0.19)

    withdraw_btn=Button(frm,text='Withdraw',font=('verdna',18),bd=4,bg='blue',fg='white',command=withdraw)
    withdraw_btn.place(relx=0.05,rely=0.65,relwidth=0.19)

    def transfer():
            infrm=Frame(frm,highlightbackground='blue',highlightthickness=2)
            infrm.place(relx=0.27,rely=0.1,relheight=0.8,relwidth=0.7)

            h_lbl=Label(infrm,text='Transfer Window',font=('verdna',15,'bold'),fg='purple')
            h_lbl.place(relx=0.4,rely=0.01)

            

            def transfer_amt():
                toacn=to_e.get()
                uamt=float(amt_e.get())

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where acn_acno=?'
                curobj.execute(query,(toacn,))
                torow=curobj.fetchone()
                if torow==None:
                    messagebox.showerror("Transfer","To ACN does not exist")
                else:
                    if row[8]>uamt:
                        otp=random.randint(1000,9999)
                        send_otp(row[3],otp,uamt)
                        messagebox.showinfo("Transfer","otp sent to your regestered email,kindly verify")
                        lbl_otp=Label(infrm,text='Enter otp',font=('verdna',20))
                        lbl_otp.place(relx=0.15,rely=0.5)

                        def verify_otp():
                            uotp=int(e_otp.get())
                            if otp==uotp:
                                conobj=sqlite3.connect(database="bank.sqlite")
                                curobj=conobj.cursor()
                                query1='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                                query2='update accounts set acn_bal=acn_bal+? where acn_acno=?'
                                curobj.execute(query1,(uamt,uacno))
                                curobj.execute(query2,(uamt,toacn))
                                conobj.commit()
                                conobj.close()
                                messagebox.showinfo('Transfer',f'{uamt} Amount Transfered')
                                frm.destroy()
                                user_screen(uacno,None)
                            else:
                                 messagebox.showerror("Transfer","invalid otp!")

                        e_otp=Entry(infrm,font=('Arial',20),bd=4)
                        e_otp.place(relx=0.4,rely=0.5)
                        e_otp.focus()


                        verify_btn=Button(infrm,command=verify_otp,text="verify",bg="green",bd=2,font=('Arial',15))
                        verify_btn.place(relx=0.6,rely=0.6)
                    else:
                        messagebox.showerror("Transfer","Insufficient amount")


            transfer_btn=Button(infrm,text='Transfer_amt',font=('verdna',18),bd=4,bg='green',fg='white',command=transfer_amt)
            transfer_btn.place(relx=0.54,rely=0.5,relwidth=0.19)

            to_lbl=Label(infrm,text='To ACN',font=('verdna',20))
            to_lbl.place(relx=0.15,rely=0.2)

            to_e=Entry(infrm,font=('verdna',20),bd=4)
            to_e.place(relx=0.4,rely=0.2)

            amt_lbl=Label(infrm,text='Amount',font=('verdna',20))
            amt_lbl.place(relx=0.15,rely=0.35)

            amt_e=Entry(infrm,font=('verdna',20),bd=4)
            amt_e.place(relx=0.4,rely=0.35)

    transfer_btn=Button(frm,text='Transfer',font=('verdna',18),bd=4,bg='blue',fg='white',command=transfer)
    transfer_btn.place(relx=0.05,rely=0.8,relwidth=0.19)

      
main_screen()
root.mainloop()