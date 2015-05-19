# INCIBEBotDetect

Summary
-------

Script to periodically check if there is an infected maching in you LAN.
The service used to deted if there is any bot in your LAN is the one pressented by INCIBE ( https://www.incibe.es/empresas/herramientas/servicio_antibotnet).
If the servie retunrs a result indicating there is a bot in your enterprise LAN it will send you an alert email.

![alt tag](https://www.incibe.es/extfrontinteco/img/Image/empresas/herramientas/esquema_antibotnet.png)

Installation
------------

This script needs the following python libraries:
- pyYaml
- smtplib
- pycurl

Install in your environment before trying to execute.

Configuration
-------------

Open file _config.yaml_ and edit the parameters at your need:

```yaml
server: smtp.gmail.com
port: 587
subject: Botnet Alarm!
source: user@domain.com
destination: user@email.com
username: user@gmail.com
password: 123456
```

Set up a **cron job** to execute this scrip periodically. For example once per day at 08:00 AM:
```
0 8 * * * cd /home/user/Tools/antibotnet/ && ./botnetdetect.py > /dev/null
```

