#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time
import sys

ergebnisCount = 0
connectionErrorCount = 0


def getAuth(s):
    j = i = s.find("ARGUMENTS") + 10
    while(s[i] != ","):
        i += 1
    return s[j:i]


def getCookie(s):
    split = s.split(";")
    cnsc = split[0].replace(" ", "")
    KWQ = split[2][9:]
    return cnsc + "; " + KWQ


while True:
    try:
        print(datetime.datetime.today())
        if datetime.datetime.today().weekday() != 5 and datetime.datetime.today().weekday() != 6 and 8 < datetime.datetime.today().hour < 22:
            payload = {
                "usrname": "mk65seji",
                "pass": "*!/9got2fF$0w=SqiI%6",
                "APPNAME": "CampusNet",
                "PRGNAME": "LOGINCHECK",
                "ARGUMENTS": "clino,usrname,pass,menuno,menu_type,browser,platform",
                "clino": "000000000000001",
                "menuno": "000299",
                "menu_type": "classic",
                "browser": "",
                "platform": ""
            }
            login = requests.post("https://almaweb.uni-leipzig.de/scripts/mgrqispi.dll", data=payload)
            if "REFRESH" not in login.headers:
                time.sleep(1800)
                continue
            else:
                print("Erfolgreich eingeloggt.")
            if login.status_code == 200:
                data = {
                    "APPNAME": "CampusNet",
                    "PRGNAME": "EXAMRESULTS",
                    "ARGUMENTS": getAuth(login.headers["REFRESH"]) + ",-N000472,"
                }

                header = {
                    "Accept": "text/html",
                    "Accept-Encoding": "identity",
                    "Cookie": getCookie(login.headers["Set-cookie"])
                }
                results = requests.get("https://almaweb.uni-leipzig.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=EXAMRESULTS&ARGUMENTS="+getAuth(login.headers["REFRESH"])+",-N000472,", headers=header)
                logout = requests.get("https://almaweb.uni-leipzig.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=LOGOUT&ARGUMENTS=" + getAuth(login.headers["REFRESH"]) + ",-N001", headers=header)
                if logout.status_code == 200:
                    print("Erfolgreich ausgeloggt.")
                if results.status_code == 200:
                    soup = BeautifulSoup(results.content, "html.parser")
                    scrape = soup.find("table", {"class": "nb list"})
                    print("Anzahl Prüfungsergebnisse: " + str(str(scrape).count('<tr class="tbdata">')))
                    if str(scrape).count('<tr class="tbdata">') != ergebnisCount:
                        me = "mail@mkobrow.de"
                        you = "max.kobrow@gmail.com"

                        msg = MIMEMultipart('alternative')
                        msg["Subject"] = "Neue Noten im Almaweb!"
                        msg["From"] = me
                        msg["To"] = you

                        text = "Neue Noten!"
                        html = """\
                        <html>
                            <body>
                        """ + str(scrape) + """\
                            </body>
                        </html>
                        """
                        part1 = MIMEText(text, 'plain')
                        part2 = MIMEText(html, 'html')

                        msg.attach(part1)
                        msg.attach(part2)

                        server = smtplib.SMTP('smtp.strato.de: 587')
                        server.starttls()
                        server.login(me, "Momaxox1999")
                        server.sendmail(me, you, msg.as_string())
                        server.quit()
                        ergebnisCount = str(scrape).count('<tr class="tbdata">')
                else:
                    print("Fehler bei der Verbindung für Results. Status Code: " + str(results.status_code))
            else:
                print("Fehler bei der Verbindung für Login. Status Code: " + str(login.status_code))
        else:
            print("Am Wochenende und nachts wird nicht abgefragt.")
            print("\n")
        connectionErrorCount = 0
        time.sleep(1800)
    except KeyboardInterrupt:
        exit()
    except KeyError as e:
        print(e)
        print(login.headers)
        me = "mail@mkobrow.de"
        you = "max.kobrow@gmail.com"

        msg = MIMEMultipart('alternative')
        msg["Subject"] = "KeyError im Almaweb Scrape"
        msg["From"] = me
        msg["To"] = you

        text = "Fehler ist aufgetreten! " + str(sys.exc_info()[0])
        html = """\
                                        <html>
                                            <body>
                                                Fehler im Almaweb Scrape:
                                        """ + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + """\
                                            </body>
                                        </html>
                                        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        server = smtplib.SMTP('smtp.strato.de: 587')
        server.starttls()
        server.login(me, "Momaxox1999")
        server.sendmail(me, you, msg.as_string())
        server.quit()
        time.sleep(1800)
        continue
    except ConnectionError:
        connectionErrorCount += 1
        if connectionErrorCount == 4:
            print("Unerwarteter Fehler: " + str(sys.exc_info()[0]))
            me = "mail@mkobrow.de"
            you = "max.kobrow@gmail.com"

            msg = MIMEMultipart('alternative')
            msg["Subject"] = "4. Connection Error"
            msg["From"] = me
            msg["To"] = you

            text = "Fehler ist aufgetreten! " + str(sys.exc_info()[0])
            html = """\
                                            <html>
                                                <body>
                                                    Fehler im Almaweb Scrape:
                                            """ + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + """\
                                                </body>
                                            </html>
                                            """
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            msg.attach(part1)
            msg.attach(part2)

            server = smtplib.SMTP('smtp.strato.de: 587')
            server.starttls()
            server.login(me, "Momaxox1999")
            server.sendmail(me, you, msg.as_string())
            server.quit()
            time.sleep(1800)
            continue
    except:
        print("Unerwarteter Fehler: " + str(sys.exc_info()[0]))
        me = "mail@mkobrow.de"
        you = "max.kobrow@gmail.com"

        msg = MIMEMultipart('alternative')
        msg["Subject"] = "Fehler im Programm!"
        msg["From"] = me
        msg["To"] = you

        text = "Fehler ist aufgetreten! " + str(sys.exc_info()[0])
        html = """\
                                <html>
                                    <body>
                                        Fehler im Almaweb Scrape:
                                """ + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + """\
                                    </body>
                                </html>
                                """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        server = smtplib.SMTP('smtp.strato.de: 587')
        server.starttls()
        server.login(me, "Momaxox1999")
        server.sendmail(me, you, msg.as_string())
        server.quit()
        time.sleep(1800)
        continue