#!/usr/bin/python
from os import path, listdir
from os import lstat, walk
from os import system
import sqlite3, sys


def Gather():
    print('Building database...')
    ExclusionList = ['media', 'dev', 'tmp', 'cdrom', 'rofs', 'mnt',
                     'proc', 'sys']
    conn = sqlite3.connect('/permissions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE permissions (bits text, uid text, gid text, item text)''')
    conn.commit()

    for i in listdir('/'):
        if not (i in ExclusionList):       
            for Root, Dirs, Files in walk('/' + i):
                for Dir in Dirs:
                    CurrentDir = path.join(Root, Dir)
                    bits = oct(lstat(CurrentDir).st_mode)[4:]
                    uid = lstat(CurrentDir).st_uid
                    gid = lstat(CurrentDir).st_gid
                    c.execute("INSERT INTO permissions VALUES (?,?,?,?)", 
                              (bits, uid, gid, CurrentDir)) 
                    conn.commit()

                    
                for File in Files:
                    CurrentFile = path.join(Root, File)
                    bits = oct(lstat(CurrentFile).st_mode)[4:]
                    uid = lstat(CurrentFile).st_uid
                    gid = lstat(CurrentFile).st_gid
                    c.execute("INSERT INTO permissions VALUES (?,?,?,?)", 
                              (bits, uid, gid, CurrentFile)) 
                    conn.commit()

    conn.close()
    print('Complete.')
      

def Restore():
    #x = 0
    con = sqlite3.connect('/permissions.db')
    for line in con.iterdump():
        #x += 1
        try:
            split_string = line.split("'")
            if (path.exists(split_string[7])):
                bits, uid = split_string[1], split_string[3]
                gid, item = split_string[5], split_string[7]
                system('chmod ' + bits + ' ' + item)
                system('chown ' + uid + ' ' + item)
                system('chgrp ' + gid + ' ' + item)
                print('processed ' + item)
        except:
            pass
        
        #if (x >= 4):
            #sys.exit()

            
if __name__ == '__main__':
    pass
