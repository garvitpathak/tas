#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import random

def topology():
    net = Mininet(controller=Controller, accessPoint=OVSKernelAP, switch=OVSKernelSwitch, link=TCLink)

    # Access Points
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='10,35,0')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='6', position='50,35,0')
    ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='g', channel='11', position='90,35,0')
    ap4 = net.addAccessPoint('ap4', ssid='ap4-ssid', mode='g', channel='1', position='10,10,0')
    ap5 = net.addAccessPoint('ap5', ssid='ap5-ssid', mode='g', channel='6', position='40,10,0')

    # Mobile Stations
    sta1 = net.addStation('sta1', ip='10.0.0.1')
    sta2 = net.addStation('sta2', ip='10.0.0.2')
    sta3 = net.addStation('sta3', ip='10.0.0.3')
    sta4 = net.addStation('sta4', ip='10.0.0.4')
    sta5 = net.addStation('sta5', ip='10.0.0.5')

    net.configureWifiNodes()

    net.plotGraph(max_x=200, max_y=35)

    # Mobility sequence and coordinates
    mobility_sequence = [
        ('sta1', 'Entrance', 10, 20, 'min_v=1, max_v=5'),
        ('sta2', 'Entrance', 30, 60, 'min_v=5, max_v=5'),
        ('sta3', 'Exit', 25, 60, 'min_v=7, max_v=7'),
        ('sta4', 'Exit', 10, 20, 'min_v=1, max_v=10'),
        ('sta5', 'Exit', 15, 20, 'min_v=5, max_v=5')
    ]

    for mob_name, start_loc, start_time, end_time, moving_speed in mobility_sequence:
        net.mobility(mob_name, start_loc, start_time, end_location=end_loc, end_time=end_time, moving_speed=moving_speed)

    print "* Running CLI"
    CLI(net)
    print "* Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
