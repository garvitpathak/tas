#!/usr/bin/python
from mininet.node import Controller
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet

def topology():
    net = Mininet(controller=Controller, link=TCLink)

    # Add controller
    c0 = net.addController('c0')

    # Add switches
    s1 = net.addSwitch('s1')

    # Add access points
    ap1 = net.addSwitch('ap1')

    # Add links
    net.addLink(ap1, s1)

    # Add stations
    for i in range(1, 6):
        sta = net.addStation('sta%s' % i, ip='192.168.0.%s/24' % i)

    # Start the network
    net.build()
    c0.start()
    s1.start([c0])

    # Set the wireless nodes
    net.configureWifiNodes()

    # Start the CLI
    net.start()
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
