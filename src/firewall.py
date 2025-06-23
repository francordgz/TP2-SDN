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
''' Add your imports here ... '''

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ['HOME']

''' Add your global variables here ... '''

MAC_H1 = EthAddr("00:00:00:00:00:01")
MAC_H3 = EthAddr("00:00:00:00:00:03")

S2_DPID = 2


class Firewall(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        ''' Add your logic here ... '''
        if event.dpid == S2_DPID:
            log.info("Instalando reglas de bloqueo en s2")

            for src, dst in [(MAC_H1, MAC_H3), (MAC_H3, MAC_H1)]:
                msg = of.ofp_flow_mod()
                msg.match.dl_src = src
                msg.match.dl_dst = dst
                msg.actions = []  # Drop
                event.connection.send(msg)
                log.debug("Bloqueo instalado: %s -> %s", src, dst)


def launch():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)