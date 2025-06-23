from mininet.topo import Topo


class TopoTP2 (Topo):
    def __init__(self, cantidad_switches):

        if cantidad_switches < 1:
            print("Error: La cantidad de switches debe ser al menos 1.")
            return

        Topo.__init__(self)

        # Crear hosts
        h1 = self.addHost('h1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', mac='00:00:00:00:00:04')

        # Crear switch
        s1 = self.addSwitch('s1')

        switches = [s1]
        for i in range(2, cantidad_switches + 1):
            s = self.addSwitch('s' + str(i))
            switches.append(s)

        # Add links between switches and hosts self . addLink ( s1 , s2 )
        self.addLink(s1, h1)
        self.addLink(s1, h2)

        for i in range(1, cantidad_switches):
            self.addLink(switches[i - 1], switches[i])

        self.addLink(switches[-1], h3)
        self.addLink(switches[-1], h4)


topos = {'customTopo': TopoTP2}
