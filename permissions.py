#!/usr/bin/python
import os
import sqlite3

database = '/permissions.py'

def Gather():
    global databae
    conn = sqlite3.connect(database)
    c = conn.cursor()

    print('Building database...')
    ExclusionList = ['media', 'dev', 'tmp', 'cdrom', 'rofs', 'mnt',
                     'proc', 'sys']

    c.execute('''CREATE TABLE permissions (bits text, uid text, gid text, item text)''')
    conn.commit()

    for i in os.listdir('/'):
        if not (i in ExclusionList):       
            for Root, Dirs, Files in os.walk('/' + i):
                for Dir in Dirs:
                    CurrentDir = os.path.join(Root, Dir)
                    stats = os.lstat(CurrentDir)
                    bits = oct(stats[0])[4:]
                    uid = stats[4]
                    gid = stats[5]
                    c.execute("INSERT INTO permissions VALUES (?,?,?,?)", 
                              (bits, uid, gid, CurrentDir)) 
                    conn.commit()

                    
                for File in Files:
                    CurrentFile = os.path.join(Root, File)
                    stats = os.lstat(CurrentFile)
                    bits = oct(stats[0])[4:]
                    uid = stats[4]
                    gid = stats[5]
                    c.execute("INSERT INTO permissions VALUES (?,?,?,?)", 
                              (bits, uid, gid, CurrentFile)) 
                    conn.commit()

    conn.close()
    print('Complete.')
      

def Restore():
    global databae
    conn = sqlite3.connect(database)

    for line in conn.iterdump():
        try:
            split_string = line.split("'")
            if (os.path.exists(split_string[7])):
                bits, uid = split_string[1], split_string[3]
                gid, item = split_string[5], split_string[7]
                os.system('chmod ' + bits + ' ' + item)
                os.system('chown ' + uid + ' ' + item)
                os.system('chgrp ' + gid + ' ' + item)
                print('processed ' + item)
        except:
            pass        
    #conn.close()

            
if __name__ == '__main__':
    pass
