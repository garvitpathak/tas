from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

def create_topology():
    net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink)

    # Add controller
    c0 = net.addController('c0')

    # Add access points
    ap_list = []
    for i in range(1, 6):
        ap = net.addBaseStation(f'AP{i}', ssid=f'studentID', mode='g', failMode='standalone', encryption='wpa2')
        ap_list.append(ap)

    # Add stations
    sta1 = net.addStation('STA1', ip='10.0.0.1/24', position='5,5')
    sta2 = net.addStation('STA2', ip='10.0.0.2/24', position='10,5')
    sta3 = net.addStation('STA3', ip='10.0.0.3/24', position='15,5')
    sta4 = net.addStation('STA4', ip='10.0.0.4/24', position='20,5')
    sta5 = net.addStation('STA5', ip='10.0.0.5/24', position='25,5')

    # Add links
    for ap in ap_list:
        net.addLink(ap, sta1)
        net.addLink(ap, sta2)

    net.build()
    c0.start()
    for ap in ap_list:
        ap.start([c0])

    # Mobility settings
    sta1.cmd('mobilityd --fixed')
    sta2.cmd('mobilityd --fixed')
    sta3.cmd('mobilityd --start 25 --min-speed 7 --max-speed 7 --waypoints "5,5 25,5"')
    sta4.cmd('mobilityd --start 10 --min-speed 1 --max-speed 10 --waypoints "25,5 5,5"')
    sta5.cmd('mobilityd --start 15 --min-speed 5 --max-speed 5 --waypoints "25,5 5,5"')

    CLI(net)

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()
