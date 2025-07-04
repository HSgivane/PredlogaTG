import sqlite3
from date import *


con = sqlite3.connect("tg.db")
cur = con.cursor()


def table(cur, con):
    cur.execute("CREATE TABLE IF NOT EXISTS user ( tg_name varchar (20), tg_id int, last int, permission varchar (20));")
    con.commit()


def idea(cur, con):
    cur.execute("CREATE TABLE IF NOT EXISTS idea ( tg_name varchar (20), tg_id int, photo_id int, text varchar (300), type int, primary_id int);")
    con.commit()


def datetable(cur, con):
    cur.execute("CREATE TABLE IF NOT EXISTS date ( tg_name varchar (20), tg_id int, date_num varchar(3), inc int);")
    con.commit()


def db_delete(primary_id, cur, con):
    cur.execute("DELETE FROM idea WHERE (primary_id) = ('{primary_id}')".\
                format(primary_id=primary_id))
    con.commit()

    
def db_tgideamem(tg_id, tg_name, photo_id, text, primary_id, cur, con, typ_e):
    cur.execute("INSERT INTO idea (tg_name, tg_id, photo_id, text, type, primary_id) VALUES ('{tg_name}', '{tg_id}', '{photo_id}', '{text}', '{typ_e}', '{primary_id}')".\
                format(tg_name=tg_name, tg_id=tg_id, photo_id=photo_id, text=text, typ_e=typ_e, primary_id=primary_id))
    con.commit()
    

def db_takeidea(typ_e, cur, con):
    cur.execute("SELECT * FROM idea WHERE type='{typ_e}';".\
                format(typ_e=typ_e))
    
    records = cur.fetchall()
    
    if not records:
        return False
    
    else:
        return records[0][0], records[0][2], records[0][3], records[0][5]


def db_lastidea(typ_e, cur, con):
    cur.execute("SELECT * FROM idea WHERE type='{typ_e}';".\
                format(typ_e=typ_e))
    
    records = cur.fetchall()
    
    if not records:
        return False
    
    else:
        return records[0][1], records[0][5]


def db_tgid(tg_id, tg_name, cur, con):
    cur.execute("SELECT * FROM user WHERE tg_id='{tg_id}'".\
                format(tg_id=tg_id))
    
    records = cur.fetchall()
    
    if not records:
        cur.execute("INSERT INTO user (tg_name, tg_id, permission) VALUES ('{tg_name}', '{tg_id}', 'default')".\
                    format(tg_name=tg_name, tg_id=tg_id))
        date_t = date_today()
        cur.execute("INSERT INTO date (tg_name, tg_id, date_num, inc) VALUES ('{tg_name}', '{tg_id}', '{date_t}', 0)".\
                    format(tg_name=tg_name, tg_id=tg_id, date_t=date_t))        
        con.commit()
    else:
        cur.execute("UPDATE user SET (last)=('0') WHERE (tg_id) = ('{tg_id}')".\
                    format(tg_id=tg_id))
        con.commit()        

    
    
def db_admcheck(tg_id, cur, con):
    cur.execute("SELECT * FROM user WHERE (tg_id='{tg_id}') AND (permission='admin')".\
                format(tg_id=tg_id))
    
    records = cur.fetchall()
    
    if not records:
        return False
    else:
        return True
    
    
def db_bancheck(tg_id, cur, con):
    cur.execute("SELECT * FROM user WHERE (tg_id='{tg_id}') AND (permission='ban')".\
                format(tg_id=tg_id))
    
    records = cur.fetchall()
    
    if not records:
        return False
    else:
        return True
    

def db_tgadm(tg_id, cur, con):
    cur.execute("UPDATE user SET (permission)=('admin') WHERE (tg_id) = ('{tg_id}')".\
                format(tg_id=tg_id))
    con.commit()


def db_tgban(tg_id, cur, con):
    cur.execute("UPDATE user SET (permission)=('ban') WHERE (tg_id) = ('{tg_id}')".\
                format(tg_id=tg_id))
    con.commit()

 
def db_tgprikol(tg_id, cur, con):
    cur.execute("UPDATE user SET (last)=('1') WHERE (tg_id) = ('{tg_id}')".\
                format(tg_id=tg_id))
    con.commit()
    

def db_tgmem(tg_id, cur, con):
    cur.execute("UPDATE user SET (last)=('2') WHERE (tg_id) = ('{tg_id}')".\
                format(tg_id=tg_id))
    con.commit()


def db_nothing(tg_id, cur, con):
    cur.execute("UPDATE user SET (last)=('0') WHERE (tg_id) = ('{tg_id}')".\
                format(tg_id=tg_id))
    con.commit()


def last_com(tg_id, cur, con):
    cur.execute("SELECT * FROM user WHERE (tg_id='{tg_id}')".\
                format(tg_id=tg_id))
    
    records = cur.fetchall()
    
    if not records:
        return False
    else:
        if records[0][2] == 1:
            return(1)
        elif records[0][2] == 2:
            return(2)
        else:
            return(0)


def db_inccheck(tg_id, cur, con):
    cur.execute("SELECT * FROM date WHERE (tg_id='{tg_id}')".\
                format(tg_id=tg_id))
    
    records = cur.fetchall()
    
    date_tt = date_today()
    
    if not records:
        return False
    else:
        if records[0][3] >= 3 and records[0][2] == date_tt:
            return False
        elif records[0][2] != date_tt:
            cur.execute("UPDATE date SET (date_num)=('{date_num}'), (inc)=('{inc}') WHERE (tg_id) = ('{tg_id}')".\
                        format(date_num=date_tt, inc=1, tg_id=tg_id))
            con.commit()
            return True
        else:
            inc = int(records[0][3]) + 1
            cur.execute("UPDATE date SET (inc)=('{inc}') WHERE (tg_id) = ('{tg_id}')".\
                        format(inc=inc, tg_id=tg_id))
            con.commit()            
            return True
       
         
table(cur, con)
idea(cur, con)
datetable(cur, con)
