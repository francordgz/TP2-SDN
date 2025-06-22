from mininet.topo import Topo

class TopoTP2 (Topo):
    def __init__ (self):
        # Initialize topology
        Topo.__init__(self)

        # Create switch
        s1 = self.addSwitch('switch_1')
        s2 = self.addSwitch('switch_2')
        s3 = self.addSwitch('switch_3')

        # Create hosts
        h1 = self.addHost ('host_1')
        h2 = self.addHost ('host_2')
        h3 = self.addHost ('host_3')
        h4 = self.addHost ('host_4')

        # Add links between switches and hosts self . addLink ( s1 , s2 )
        self.addLink(s1, h1)
        self.addLink(s1, h2)
        self.addLink(s3, h3)
        self.addLink(s3, h4)
        self.addLink(s2, s3)
        self.addLink(s1, s2)

topos = {'customTopo': TopoTP2}