import getpass
import sys
import urllib

import requests
from bs4 import BeautifulSoup
from pip import main

#Password = getpass.getpass()
Password = "Tornillazo3"
Username=sys.argv[1]
IzenAbizenak=sys.argv[2].upper()

def lehen_eskaera():
    # LEHEN ESKAERA:
    metodoa = 'GET'
    uria = "https://egela.ehu.eus/login/index.php"
    goiburuak = {'Host': 'egela.ehu.eus'}


    erantzuna = requests.request(metodoa, uria,headers=goiburuak, allow_redirects=False)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("Lehen eskaera: "+str(kodea) + " " + deskribapena)
    edukia = erantzuna.content

    Cookia = erantzuna.headers['Set-Cookie'].split(";")[0]
    print("Cookie: "+Cookia)

    soup = BeautifulSoup(edukia, 'html.parser' )
    logint=soup.find('input',{'name': 'logintoken'})
    logintoken = logint["value"]
    print("Logintoken: "+logintoken)

    action=soup.find('form')
    Location=action["action"]
    print("Location: " +Location)
    return (Location, Cookia, logintoken)



def bigarren_eskaera(Location, Cookia, logintoken):
    # BIGARREN ESKAERA:
    metodoa = 'POST'
    uria = Location
    goiburuak = {'Host': 'egela.ehu.eus',
                 'Cookie': Cookia,
                  'Content-Type': "application/x-www-form-urlencoded" }
    edukia = {'logintoken':logintoken, 'username':Username, 'password': Password}
    edukia_encoded = urllib.parse.urlencode(edukia)
    erantzuna2 = requests.request(metodoa, uria, data=edukia_encoded,headers=goiburuak, allow_redirects=False)

    kodea = erantzuna2.status_code
    deskribapena = erantzuna2.reason
    print("Bigarren eskaera: "+str(kodea) + " " + deskribapena)
    edukia = erantzuna2.content

    Cookia2 = erantzuna2.headers['Set-Cookie'].split(";")[0]

    locationTestSession = erantzuna2.headers['Location'].split("?testsession=")[1]

    return (Cookia2, locationTestSession)



def hirugarren_eskaera(cookie, testsession):
    metodoa = 'GET'
    uria = "https://egela.ehu.eus/login/index.php?testsession="+testsession
    goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': cookie, 'Content-Type': 'application/x-www-form-urlencoded'}


    erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("Hirugarren eskaera: " + str(kodea) + " " + deskribapena)
    location = erantzuna.headers['Location']
    return (location)

def laugarren_eskaera(cookie, location):
    metodoa = 'GET'
    uria = location
    goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': cookie, 'Content-Type': 'application/x-www-form-urlencoded'}

    erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("Laugarren eskaera: " + str(kodea) + " " + deskribapena)

    edukia=erantzuna.content
    soup = BeautifulSoup(edukia, 'html.parser')
    usern = str(soup.find('span', {'class': 'usertext mr-1'}))
    bigarrenZatia=usern.split(">")[1]
    izena=bigarrenZatia.split("<")[0]

    bilaketa=soup.find('div', {'data-courseid': '57996'})
    a=str(bilaketa.find('a'))

    nextUriESKUINA=a.split('href="')[1]
    newUri=nextUriESKUINA.split('">')[0]


    return(izena, newUri)

def sartuWebSistemakIrakasgaira(uri, cookie):
    metodoa = 'GET'
    uria = uri
    goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': cookie, 'Content-Type': 'application/x-www-form-urlencoded'}

    erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("WebSistemak eskaera: " + str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    soup = BeautifulSoup(edukia, 'html.parser')

    print(soup)

if __name__ == '__main__':
    listaLehenEskaera=lehen_eskaera()
    location=listaLehenEskaera[0]
    cookie=listaLehenEskaera[1]
    loginToken=listaLehenEskaera[2]
    listaBigarrenEskaera=bigarren_eskaera(location,cookie,loginToken)
    cookie2=listaBigarrenEskaera[0]
    tSession=listaBigarrenEskaera[1]
    azkenLocation=hirugarren_eskaera(cookie2,tSession)
    izena=laugarren_eskaera(cookie2, azkenLocation)[0]
    uriWebSis=laugarren_eskaera(cookie2, azkenLocation)[1]
    print("Momentu honetan eGelan sartuta dago sistema, erabiltzaile izena: "+izena)
    print("EGOKIA AL DA? KONPROBATZEN...")

    if (izena==IzenAbizenak):
        print("BAI!! EGOKIA DA, ERABILTZAILEA "+IzenAbizenak+" da!!")
        #tekla sakatu arte ez aurrera joan--->HORI FALTA DA
    else:
        print("Ez")
        sys.exit(0)

    print("WEB SISTEMAK irakasgaira sartzen...")
    sartuWebSistemakIrakasgaira(uriWebSis,cookie2)