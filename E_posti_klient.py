import email
from email.message import EmailMessage
import smtplib
import ssl
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
import time
import threading

def vali_pilt():
    global file
    file=filedialog.askopenfilename()
    return file

def muuta_lisa(event):
    file=vali_pilt()
    lisa_.insert(0,file)

def progressbar():
    if progress.winfo_ismapped():
        progress.grid_remove()  
    else:
        progress.grid(row=11, column=4, pady=20)  
        threading.Thread(target=run_progress).start() 

def run_progress():
    progress.start()
    time.sleep(4)  
    progress.stop()
    progress.grid_remove()

def start_sending(event):
    progressbar() 
    uus_niit = threading.Thread(target=saada)  
    uus_niit.start()  

file=None
def saada():
    kellele = email_.get()
    teema = teema_.get()
    kiri = kiri_.get("1.0", END).rstrip('\n')
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    kellelt = 'posvystakmariia@gmail.com'
    parool = 'rlop buyk lrpk rwqx'  

    msg = EmailMessage()
    msg['Subject'] = teema
    msg['From'] = kellelt
    to = kellele.split(',')  
    to = [address.strip() for address in to]
    msg['To'] = ','.join(to)
    text_sisu = kiri
    html_sisu = f"""
    <html>
      <body>
        <h1>{teema}</h1>
        <p>{text_sisu}</p>
      </body>
    </html>
    """
    msg.set_content(text_sisu)
    msg.add_alternative(html_sisu, subtype='html')

    attachment_name = None
    if file:
        try:
            with open(file, 'rb') as f:
                file_data = f.read()
                attachment_name = f.name.split('/')[-1]
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=attachment_name)
        except Exception as e:
            messagebox.showerror("Faili viga", f"Manuse lisamine ebaõnnestus:\n{e}")
            return
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(kellelt, parool)
            server.send_message(msg)

        messagebox.showinfo("Edukalt saadetud", "Kiri on saadetud!")
    except Exception as e:
        messagebox.showerror("Viga", f"Kiri saatmine ebaõnnestus:\n{e}")

def selge(event):
    email_.delete(0,END)
    teema_.delete(0,END)
    lisa_.delete(0,END)
    kiri_.delete("1.0",END)

def salvesta(kellele, teema, kiri):
    fail='login.txt'
    uus_email=(f"email: {kellele}, teema: {teema}, kiri: {kiri}")
    with open (fail, 'a',  encoding="utf-8") as f:
        f.write(uus_email)
    print("Email salvestatud faili. ")


def forms(event):
    kellele = email_.get()
    teema = teema_.get()
    kiri = kiri_.get("1.0", END).strip()
    salvesta(kellele, teema, kiri)

aken=Tk()
aken.title("E-kirja saatmine")
aken.geometry("700x700")
aken.configure(bg="back")
aken.resizable(width=False, height=True)
aken.iconbitmap("112-gmail_email_mail-512.ico")

pilt = PhotoImage(file="4.png")
email1=Label(aken, text="EMAIL:", bg="#606060", font=("Arial", 17), fg="white", width=7, height=1)
teema=Label(aken, text="TEEMA:", bg="#606060", font=("Arial", 17), fg="white", width=7, height=1)
lisa=Label(aken, text="LISA:", bg="#606060", font=("Arial", 17), fg="white", width=7, height=1)
kiri=Label(text="KIRI:", bg="#606060", font=("Arial", 17), fg="white", width=7, height=1)
pilt_=Label(aken,image=pilt)
t=Label(aken, text="Gmail", bg="black", font=("Arial", 20), fg="white", width=7, height=1)
pilt_.grid(row=0, column=2, pady=5)
t.grid(row=0, column=1, pady=5)
email1.grid(row=1, column=1, pady=5)
teema.grid(row=2, column=1,pady=5)
lisa.grid(row=3, column=1,pady=5)
kiri.grid(row=4, column=1, pady=40)


email_=Entry(aken, bg="#606060", font=("Arial", 17), fg="white", width=30)
teema_=Entry(aken, bg="#606060", font=("Arial", 17), fg="white", width=30)
lisa_=Entry(aken, bg="#606060", font=("Arial", 17), fg="white", width=30)
kiri_=Text(aken, bg="#606060", font=("Arial", 17), fg="white", width=30, height=10)
email_.grid(row=1, column=2, pady=5, columnspan=7)
teema_.grid(row=2, column=2, pady=5, columnspan=7)
lisa_.grid(row=3, column=2, pady=5, columnspan=7)
kiri_.grid(row=4, column=2, pady=5, columnspan=7, rowspan=5)

lisa_nupp=Button(aken, text="LISA PILT", bg="lightblue", font=("Arial", 12), fg="black", relief=RAISED)
lisa_nupp.bind("<Button-1>", muuta_lisa)
lisa_nupp.grid(row=10, column=4, pady=5)
saat_nupp=Button(aken, text="SAADA", bg="lightblue", font=("Arial", 12), fg="black", relief=RAISED)
saat_nupp.bind("<Button-1>", start_sending)
saat_nupp.grid(row=10, column=3, pady=5)
progress = ttk.Progressbar(aken, orient="horizontal", length=300, mode="determinate")
clear_nupp=Button(aken, text="SELGE", bg="lightblue", font=("Arial", 12), fg="black", relief=RAISED)
clear_nupp.bind("<Button-1>", selge)
clear_nupp.grid(row=10, column=5, pady=5)
sal_nupp=Button(aken, text="SALVESTA", bg="lightblue", font=("Arial", 12), fg="black", relief=RAISED)
sal_nupp.bind("<Button-1>", forms)
sal_nupp.grid(row=10, column=6, pady=5)
aken.mainloop()
