from suds.client import Client

client = Client("http://vocab.ndg.nerc.ac.uk/axis2/services/vocab?wsdl")
#http://vocab.ndg.nerc.ac.uk/list/C771/1
import sqlite3
mydatabase="./vocablists"
connection=sqlite3.connect(mydatabase)
cursor=connection.cursor()


ret = client.service.whatLists()
for tlist in ret.codeTableType:
    #print tlist
    cursor.execute('INSERT INTO lists VALUES( ?, ?)', (tlist.listKey, tlist.listLongName))


#print list2name('http://vocab.ndg.nerc.ac.uk/list/L221/15')


#cursor.execute('CREATE TABLE mytable (Id INTEGER PRIMARY KEY, Date TEXT, Entry TEXT)')

connection.commit()
cursor.close()
quit()
