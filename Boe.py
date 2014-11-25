#!/usr/bin/python
# -*- coding: utf-8 -*-
#Created on Tue Nov 25 11:11:53 2014 by mercaderd

from xml.etree import ElementTree
from email.mime.text import MIMEText
import urllib2
import time
import smtplib
import sys

class Boe(object):
    def __init__(self):
        super(Boe, self).__init__()        
        self.urlbase='http://www.boe.es/diario_boe/xml.php?id=BOE-S-'
        self.contenido=[]
        
    def updateinfo(self):        
        self.contenido=[];
        url=self.urlbase+time.strftime('%Y%m%d')
        response = urllib2.urlopen(url)
        if response: html = response.read()
        if html: document=ElementTree.fromstring(html)
        secciones = document.findall( 'diario/seccion' )
        if secciones:        
            for seccion in secciones:
                if seccion.attrib['num']=='2B':
                    departamentos=seccion;

        if departamentos is not None:        
            for departamento in departamentos:
                self.contenido.append(departamento.attrib['nombre']+'\n')
                for concurso in departamento:
                    self.contenido.append( '\t' + concurso.attrib['nombre']+'\n')
                    for item in concurso:
                        self.contenido.append('\t\t' + item[0].text + '\n') 
                        self.contenido.append('\t\t' + 'http://www.boe.es'+item[1].text + '\n\n')
        return len(self.contenido)
    
    def savetofile(self, filename='boehoy.txt'):
        if len(self.contenido) > 0:        
            file=open(filename,'w')
            if file:
                for line in self.contenido:                
                    file.write(line.encode('utf-8'))
                file.close()
                return 1
     
  
    def sendbyemail(self,user,password,fromemail,toemail,serverurl='smtp.mail.yahoo.com',serverport=587):
        if len(self.contenido) > 0:        
                        
            email=MIMEText("".join(self.contenido).encode('utf-8'))
	    email['Subject']='BOE ' + time.strftime('%d/%m/%Y')
	    email['From']=fromemail
	    email['To']=toemail
	    try:        
                server = smtplib.SMTP(serverurl, 587)
                if server:
                    server.starttls()
                    server.login(user,password)
                    server.sendmail(fromemail, toemail, email.as_string())
                    server.close()
                    return 1
            except:
                return 0
        
            

    

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: boe user password fromemail toemail"
        sys.exit(1)
    boetoday=Boe()
    if boetoday.updateinfo():
        boetoday.savetofile()
        if not boetoday.sendbyemail(user=sys.argv[1], password=sys.argv[2],fromemail=sys.argv[3],toemail=sys.argv[4]): print "Error sending email"
