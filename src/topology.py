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
        h1 = self.addHost('h1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', mac='00:00:00:00:00:04')

        # Add links between switches and hosts self . addLink ( s1 , s2 )
        self.addLink(s1, h1)
        self.addLink(s1, h2)
        self.addLink(s3, h3)
        self.addLink(s3, h4)
        self.addLink(s2, s3)
        self.addLink(s1, s2)

topos = {'customTopo': TopoTP2}