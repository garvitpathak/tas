from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_topology():
    net = Mininet(controller=Controller, accessPoint=OVSKernelAP, link=TCLink)

    # Add controller
    c0 = net.addController('c0')

    # Add access points
    ap1 = net.addAccessPoint('ap1', ssid='adhocUoH_HT40+', mode='g', channel='1', position='10,10,0')
    ap2 = net.addAccessPoint('ap2', ssid='adhocUoH_HT40+', mode='g', channel='6', position='20,20,0')
    ap3 = net.addAccessPoint('ap3', ssid='adhocUoH_HT40+', mode='g', channel='11', position='30,30,0')

    # Add stations
    adhoc1 = net.addStation('adhoc1', position='5,5,0')
    adhoc2 = net.addStation('adhoc2', position='15,15,0')
    adhoc3 = net.addStation('adhoc3', position='25,25,0')
    adhoc4 = net.addStation('adhoc4', position='35,35,0')
    adhoc5 = net.addStation('adhoc5', position='45,45,0')
    adhoc6 = net.addStation('adhoc6', position='40,40,0')

    # Add links
    net.addLink(ap1, adhoc1)
    net.addLink(ap2, adhoc2)
    net.addLink(ap3, adhoc3)
    net.addLink(ap3, adhoc4)
    net.addLink(ap3, adhoc5)
    net.addLink(ap3, adhoc6)

    # Start the network
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])

    # Enable IPv6 on stations
    for adhoc in [adhoc1, adhoc2, adhoc3, adhoc4, adhoc5, adhoc6]:
        adhoc.cmd('ip -6 addr add dev {}-wlan0'.format(adhoc.name))

    return net

def configure_protocols(net):
    # Set up OLSR on specified adhoc hosts
    for adhoc in [net.get('adhoc2'), net.get('adhoc3'), net.get('adhoc4'), net.get('adhoc5')]:
        adhoc.cmd('echo olsr >> /etc/quagga/daemons')
        adhoc.cmd('service quagga restart')

    # Set up BATMAN on specified adhoc host
    net.get('adhoc6').cmd('echo batman_adv >> /etc/modules')

def initiate_icmp_stream(net):
    # Initiate ICMP stream between adhoc hosts
    adhoc1.cmd('ping6 -i 0.1 -c 30 %s' % adhoc2.IP())
    adhoc1.cmd('ping6 -i 0.1 -c 30 %s' % adhoc3.IP())

def initiate_tcp_transfers(net):
    # Initiate TCP transfers between adhoc hosts
    adhoc2.cmd('iperf -s &')
    adhoc3.cmd('iperf -s &')
    
    adhoc1.cmd('iperf -t 30 -c %s' % adhoc2.IP())
    adhoc1.cmd('iperf -t 30 -c %s' % adhoc3.IP())

def main():
    setLogLevel('info')

    # Create Mininet-WiFi network
    net = create_topology()

    # Configure adhoc protocols
    configure_protocols(net)

    # Initiate ICMP stream
    initiate_icmp_stream(net)

    # Initiate TCP transfers
    initiate_tcp_transfers(net)

    # Start Mininet-WiFi CLI
    CLI(net)

    # Stop Mininet-WiFi
    net.stop()

if __name__ == '__main__':
    main()
