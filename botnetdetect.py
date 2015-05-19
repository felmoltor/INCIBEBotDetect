#!/usr/bin/python
# Author: Felipe Molina (@felmoltor)
# Date: 19/05/2015
# Summary: This scripts checks with the antibotnet service of INCIBE if there is an infected host inside your lan
# Links:
#   * https://www.incibe.es/empresas/herramientas/servicio_antibotnet
#   * https://www.incibe.es/extfrontinteco/img/File/empresas/incibe_sab_api_publica_empresas.pdf

import yaml
import json
import pycurl
import smtplib
from io import BytesIO

cfg=yaml.load(open("config.yaml","r"))

def sendAlert(msg):
    mailmsg = "Subject: %s\n\n%s" % (cfg["subject"],msg)

    # The actual mail send
    server = smtplib.SMTP("%s:%s" % (cfg["server"],cfg["port"]))
    server.starttls()
    server.login(cfg["username"],cfg["password"])
    server.sendmail(cfg["source"],cfg["destination"], msg)
    server.quit()

def callINCIBE():
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL,"https://antibotnet.osi.es/api/wscheckip/es")
    c.setopt(c.HTTPHEADER,["X_INTECO_WS_Request_Source: api",])
    c.setopt(c.WRITEDATA,buffer)
    c.perform()
    j = buffer.getvalue()
    jl = json.loads(j.decode('iso-8859-1'))
    return jl


############
### MAIN ###
############

result = callINCIBE()
mailmsg = ""
if result["error"] == '':
    if len(result["evidences"]) > 0:
        # There is evidences of infection
        # Send alert email
        mailmsg += "======== %s =========" % result["ip"]
        for evidence in result["evidences"]:
            mailmsg += "------------------"
            mailmsg += "Name: %s" % evidence["name"] 
            mailmsg += "ThreatCode: %s" % evidence["threatCode"]
            mailmsg += "Description found in: %s" % evidence["descriptionUrl"]
            mailmsg += "Affected OS:  "
            for os in evidence["operatingSystems"]:
                mailmsg += " - %s (Disinfect solution in %s)" % (os["operatingSystem"],os["disinfectUrl"])
        sendAlert(mailmsg)
    else:
        print "%s is not infected" % result["ip"]
        # sendAlert("%s is not infected" % result["ip"])
else:
    print "There was an error contacting with the service"
    print "Error: %s" % result["error"]
