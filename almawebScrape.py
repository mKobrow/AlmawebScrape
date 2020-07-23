#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import datetime
import time
import sys
from random import randint

import config

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
    sleeptime = randint(config.refreshTime["upper"], config.refreshTime["lower"])
    try:
        print(datetime.datetime.today())
        if datetime.datetime.today().weekday() != 5 and datetime.datetime.today().weekday() != 6 and 8 < datetime.datetime.today().hour < 22:
            payload = {
                "usrname": config.almaweb["user"],
                "pass": config.almaweb["password"],
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
                time.sleep(sleeptime)
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
                        msg = MIMEMultipart('alternative')
                        msg["Subject"] = "Neue Noten im Almaweb!"
                        msg["From"] = str(Header(config.email["FromName"] + "<" + config.email["From"] + ">"))
                        msg["To"] = config.email["To"]

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

                        server = smtplib.SMTP(config.email["FromSMTP"])
                        server.starttls()
                        server.login(config.email["From"], config.email["FromPassword"])
                        server.sendmail(config.email["From"], config.email["To"], msg.as_string())
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
        time.sleep(sleeptime)
    except KeyboardInterrupt:
        exit()
    except KeyError as e:
        print(e)
        print(login.headers)

        msg = MIMEMultipart('alternative')
        msg["Subject"] = "KeyError im Almaweb Scrape"
        msg["From"] = str(Header(config.email["FromName"] + "<" + config.email["From"] + ">"))
        msg["To"] = config.email["To"]

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

        server = smtplib.SMTP(config.email["FromSMTP"])
        server.starttls()
        server.login(config.email["From"], config.email["FromPassword"])
        server.sendmail(config.email["From"], config.email["To"], msg.as_string())
        server.quit()
        time.sleep(sleeptime)
        continue
    except ConnectionError:
        connectionErrorCount += 1
        if connectionErrorCount == 4:
            print("Unerwarteter Fehler: " + str(sys.exc_info()[0]))

            msg = MIMEMultipart('alternative')
            msg["Subject"] = "4. Connection Error"
            msg["From"] = str(Header(config.email["FromName"] + "<" + config.email["From"] + ">"))
            msg["To"] = config.email["To"]

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

            server = smtplib.SMTP(config.email["FromSMTP"])
            server.starttls()
            server.login(config.email["From"], config.email["FromPassword"])
            server.sendmail(config.email["From"], config.email["To"], msg.as_string())
            server.quit()
            time.sleep(sleeptime)
            continue
    except:
        print("Unerwarteter Fehler: " + str(sys.exc_info()[0]))

        msg = MIMEMultipart('alternative')
        msg["Subject"] = "Fehler im Programm!"
        msg["From"] = str(Header(config.email["FromName"] + "<" + config.email["From"] + ">"))
        msg["To"] = config.email["To"]

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

        server = smtplib.SMTP(config.email["FromSMTP"])
        server.starttls()
        server.login(config.email["From"], config.email["FromPassword"])
        server.sendmail(config.email["From"], config.email["To"], msg.as_string())
        server.quit()
        time.sleep(sleeptime)
        continue
