#!/usr/bin/python
import os
import sqlite3

database = '/permissions.db'
exclusionlist = ['media', 'dev', 'tmp', 'cdrom', 'rofs', 'mnt', 'proc', 'sys']

def gather():
    global database
    global exclusionlist
    conn = sqlite3.connect(database)
    c = conn.cursor()

    print('Building database...')

    c.execute('''CREATE TABLE permissions (bits text, uid text, gid text, item text)''')
    conn.commit()

    for i in os.listdir('/'):
        if not (i in ExclusionList):       
            for Root, Dirs, Files in os.walk('/' + i):
                for Dir in Dirs:
                    CurrentDir = os.path.join(Root, Dir)
                    stats = os.lstat(CurrentDir)
                    bits = oct(stats[0])[-3:]
                    uid = stats[4]
                    gid = stats[5]
                    c.execute("INSERT INTO permissions VALUES (?,?,?,?)", 
                              (bits, uid, gid, CurrentDir)) 
                    conn.commit()

                    
                for File in Files:
                    CurrentFile = os.path.join(Root, File)
                    stats = os.lstat(CurrentFile)
                    bits = oct(stats[0])[-3:]
                    uid = stats[4]
                    gid = stats[5]
                    c.execute("INSERT INTO permissions VALUES (?,?,?,?)", 
                              (bits, uid, gid, CurrentFile)) 
                    conn.commit()

    conn.close()
    print('Complete.')
      

def restore():
    global databae
    conn = sqlite3.connect(database)

    for line in conn.iterdump():
        try:
            split_string = line.split("'")
            if (os.path.exists(split_string[7])):
                bits = split_string[1]
                uid = split_string[3]
                gid = split_string[5]
                item = split_string[7]
                print(bits, uid, gid, item)
                os.chmod(item, bits)
                os.chown(item, uid, gid)
                print('processed ' + item)
        except:
            pass         
    #conn.close()

            
if __name__ == '__main__':
    args = sys.argv[1:]
    if (len(args) > 0):
        for i in args:
            if (i == 'gather'):
                gather()
            if (i == 'restore'):
                restore()
