from tkinter import *
import sqlite3,sys

def connection():
    try:
        conn=sqlite3.connect("book.db")
    except:
        print("cannot connect to the database")
    return conn    


def verifier():
    a=b=c=d=e=f=0
    if not book_name.get():
        t1.insert(END,"<>Book name is required<>\n")
        a=1
    if not rack_no.get():
        t1.insert(END,"<>rack no is required<>\n")
        b=1
    if not main.get():
        t1.insert(END,"<>main is required<>\n")
        c=1
    if not author.get():
        t1.insert(END,"<>author name is required<>\n")
        e=1
    if not publications.get():
        t1.insert(END,"<>publications is Required<>\n")
        f=1
    if a==1 or b==1 or c==1 or d==1 or e==1 or f==1:
        return 1
    else:
        return 0


def add_book():
            ret=verifier()
            if ret==0:
                conn=connection()
                cur=conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS bookS(NAME TEXT,rack_no INTEGER,main TEXT,author TEXT,publications TEXT)")
                cur.execute("insert into bookS values(?,?,?,?,?)",(book_name.get(),int(rack_no.get()),main.get(),author.get(),publications.get()))
                conn.commit()
                conn.close()
                t1.insert(END,"BOOK ADDED SUCCESSFULLY\n")


def view_book():
    conn=connection()
    cur=conn.cursor()
    cur.execute("select * from bookS")
    data=cur.fetchall()
    conn.close()
    for i in data:
        t1.insert(END,str(i)+"\n")


def delete_book():
    ret=verifier()
    if ret==0:
        conn=connection()
        cur=conn.cursor()
        cur.execute("DELETE FROM bookS WHERE rack_no=?",(int(rack_no.get()),))
        conn.commit()
        conn.close()
        t1.insert(END,"SUCCESSFULLY DELETED BOOK DETAILS\n")

def update_book():
    ret=verifier()
    if ret==0:
        conn=connection()
        cur=conn.cursor()
        cur.execute("UPDATE bookS SET NAME=?,rack_no=?,main=?,author=?,publications=? where rack_no=?",(book_name.get(),int(rack_no.get()),main.get(),author.get(),publications.get(),int(rack_no.get())))
        conn.commit()
        conn.close()
        t1.insert(END,"UPDATED SUCCESSFULLY\n")


def clse():
    sys.exit() 


if _name=="main_":
    root=Tk()
    root.title("Book Management System")
     
    book_name=StringVar()
    rack_no=StringVar()
    main=StringVar()
    author=StringVar()
    publications=StringVar()
    
    label1=Label(root,text="Book name:")
    label1.place(x=0,y=0)

    label2=Label(root,text="rack no:")
    label2.place(x=0,y=30)

    label3=Label(root,text="Main:")
    label3.place(x=0,y=60)

    label5=Label(root,text="Author Name:")
    label5.place(x=0,y=120)

    label6=Label(root,text="publication:")
    label6.place(x=0,y=150)

    e1=Entry(root,textvariable=book_name)
    e1.place(x=100,y=0)

    e2=Entry(root,textvariable=rack_no)
    e2.place(x=100,y=30)

    e3=Entry(root,textvariable=main)
    e3.place(x=100,y=60)
    
    e5=Entry(root,textvariable=author)
    e5.place(x=100,y=120)

    e6=Entry(root,textvariable=publications)
    e6.place(x=100,y=150)
    
    t1=Text(root,width=80,height=20)
    t1.grid(row=10,column=1)
   


    b1=Button(root,text="ADD BOOOKS",command=add_book,width=40)
    b1.grid(row=11,column=0)

    b2=Button(root,text="VIEW ALL BOOKS",command=view_book,width=40)
    b2.grid(row=12,column=0)

    b3=Button(root,text="DELETE BOOKS",command=delete_book,width=40)
    b3.grid(row=13,column=0)

    b4=Button(root,text="UPDATE INFO",command=update_book,width=40)
    b4.grid(row=14,column=0)

    b5=Button(root,text="EXIT",command=clse,width=40)
    b5.grid(row=15,column=0)


    root.mainloop()