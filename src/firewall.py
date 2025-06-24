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
from pox.lib.addresses import IPAddr
from collections import namedtuple
import pox.lib.packet as pkt
import os
import json

log = core.getLogger()

DPID_FIREWALL_SWITCH = 1

NOMBRE_ARCHIVO_CONFIGURACION = os.path.join(
    os.path.dirname(__file__),
    "..", "config.json"
)


def obtener_dl_type(version_ip):
    '''
    Returns the dl_type based on the version of the protocol.
    '''
    if version_ip == "4":
        return pkt.ethernet.IP_TYPE  # IPv4
    elif version_ip == "6":
        return pkt.ethernet.IPV6_TYPE  # IPv6
    else:
        return None


def cargar_reglas(nombre_archivo):
    with open(nombre_archivo) as file:
        config = json.load(file)
    return config.get("reglas", [])


def obtener_protocolo_transporte(protocolo_transporte):
    if protocolo_transporte == "TCP":
        return pkt.ipv4.TCP_PROTOCOL
    elif protocolo_transporte == "UDP":
        return pkt.ipv4.UDP_PROTOCOL
    else:
        return None


def crear_regla_drop(dl_src=None, dl_dst=None, src_ip=None, dst_ip=None,
                     version_ip=None, protocolo_transporte=None, dst_port=None,
                     src_port=None):
    log.debug("Creo regla de drop para: dl_src=%s, dl_dst=%s, version_ip=%s, protocolo_transporte=%s, dst_port=%s",
              dl_src, dl_dst, version_ip, protocolo_transporte, dst_port)
    msg = of.ofp_flow_mod()
    msg.match.dl_src = EthAddr(dl_src) if dl_src else None
    msg.match.dl_dst = EthAddr(dl_dst) if dl_dst else None
    msg.match.nw_src = IPAddr(src_ip) if src_ip else None
    msg.match.nw_dst = IPAddr(dst_ip) if dst_ip else None
    msg.match.dl_type = obtener_dl_type(version_ip) if version_ip else None
    msg.match.nw_proto = obtener_protocolo_transporte(protocolo_transporte) if protocolo_transporte else None
    msg.match.tp_dst = int(dst_port) if dst_port else None
    msg.match.tp_src = int(src_port) if src_port else None
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
                msg = crear_regla_drop(dl_src=regla.get("src_mac"),
                                       dl_dst=regla.get("dst_mac"),
                                       src_ip=regla.get("src_ip"),
                                       dst_ip=regla.get("dst_ip"),
                                       version_ip=regla.get("ip_version"),
                                       protocolo_transporte=regla.get("transport_protocol"),
                                       dst_port=regla.get("dst_port"),
                                       src_port=regla.get("src_port"))
                event.connection.send(msg)


def launch():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
