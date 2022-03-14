import getpass
import sys
import urllib

import requests
from bs4 import BeautifulSoup
Password = getpass.getpass()
Username=sys.argv[1]
IzenAbizenak=sys.argv[2]

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

