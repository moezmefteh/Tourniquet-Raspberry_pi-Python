from tkinter import *
import mysql.connector
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)

mydb=mysql.connector.connect(host="127.0.0.1",user="moez",password='project123PROJECT',port='3306',database="caisse")
cursor =mydb.cursor()


def check ():
  global label
  CodeQR=textbox.get("1.0","end-1c")
  entrer=cursor.execute("SELECT entre FROM ticket JOIN soire_cour ON ticket.id_event=soire_cour.id_soire WHERE num_ticket= '{}'".format(CodeQR))
  CODE=cursor.fetchall()
  try :
    if ( CODE[0][0] == 'False'): 
        now = datetime.datetime.now()
        label = Label(fenetre, text="ticket valide")
        label.pack()
        cursor.execute("UPDATE ticket SET entre = 'True'  WHERE num_ticket = '{}'".format(CodeQR))
        mydb.commit()
        ordre="UPDATE  ticket SET heur_entre = '{}' WHERE num_ticket= '{}'"
        cursor.execute(ordre.format(now, CodeQR))
        mydb.commit()
        GPIO.output(7,True)
            
    if ( CODE[0][0] == 'True'):
        cursor.execute("SELECT heur_entre FROM ticket WHERE num_ticket= '{}'".format(CodeQR))
        c=cursor.fetchall()
        label = Label(fenetre, text="ticket deja utilise a "+str(c[0][0]) )
        label.pack()       
  except :
    label = Label(fenetre, text="ticket non valide")
    label.pack()

def connexion():
  try :
    label.destroy()
    label.pack()
    check()
    textbox.delete("1.0","end-1c")
  except :
    check()
    textbox.delete("1.0","end-1c")

while True :
  fenetre = Tk()
  label0= Label(fenetre, text="please check your ticket")
  label0.pack()
  textbox=Text(fenetre,height=1, width=30)
  textbox.pack()
  textbox.focus_force()
  connexion()
  fenetre.mainloop()
    
