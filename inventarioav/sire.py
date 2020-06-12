from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
import requests
import re
from textwrap import shorten
from urllib.parse import quote
import xml.etree.ElementTree as ET

SIRE_USER = "sire.audiovisuales@uca.es"
SIRE_PASSWORD = "budider72"

session = Session()
session.auth = HTTPBasicAuth(SIRE_USER, SIRE_PASSWORD)
client = Client('https://sire.uca.es/sire/wsdl/sire.wsdl', transport=Transport(session=session))
if client is not None:
    listaCentros = client.service.listaCentros
    print(listaCentros)
else:
    print ("No puedo acceder a Sire")