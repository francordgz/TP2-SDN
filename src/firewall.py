'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import json
''' Add your imports here ... '''

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ['HOME']

''' Add your global variables here ... '''
DPID_FIREWALL_SWITCH = 1

NOMBRE_ARCHIVO_CONFIGURACION = os.path.join(
    os.path.dirname(__file__),
    "..", "config.json"
)


def cargar_reglas(nombre_archivo):
    with open(nombre_archivo) as file:
        config = json.load(file)
    return config.get("reglas", [])


def crear_regla_drop(dl_src=None, dl_dst=None):
    log.debug("Creo regla de drop para: dl_src=%s, dl_dst=%s", dl_src, dl_dst)
    msg = of.ofp_flow_mod()
    msg.match.dl_src = EthAddr(dl_src) if dl_src else None
    msg.match.dl_dst = EthAddr(dl_dst) if dl_dst else None
    msg.actions = []  # Drop
    return msg


class Firewall(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        ''' Add your logic here ... '''
        if event.dpid == DPID_FIREWALL_SWITCH:
            log.info("Instalando reglas de bloqueo en s" + str(DPID_FIREWALL_SWITCH))

            for regla in cargar_reglas(NOMBRE_ARCHIVO_CONFIGURACION):
                msg = crear_regla_drop(dl_src=regla.get("dl_src"), dl_dst=regla.get("dl_dst"))
                event.connection.send(msg)


def launch():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)