__author__ = 'Andrei'

import pymssql
import json

Conn = pymssql.connect(host = 'localhost', user = 'sa', password = 'Ericsson27', database = 'TESTURI')

Curs = Conn.cursor()

Curs.execute("Select top 10000 * from dbo.[Gross Pay Analysis]")

Outfile = open("C:\\Direct\\bulk\\Output.csv","w")



#row =  Curs.fetchone()
StrIn = ''
for row in Curs:
    StrIn = str(row)
    StrIn.replace("(","")
    StrIn.replace(")","")
    StrIn = StrIn[1:-2]
    print(StrIn,file=Outfile)
Outfile.close()