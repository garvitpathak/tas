from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP, OVSKernelSwitch, Station
from mininet.util import custom, customClass, waitListening

def topology():
    "Create a network."
    net = Mininet(controller=Controller, accessPoint=OVSKernelAP, switch=OVSKernelSwitch)

    print("*** Creating nodes")
    ap_list = []
    sta_list = []

    # Create access points
    for i in range(1, 6):
        ap = net.addAccessPoint('AP{}'.format(i), ssid='studentID', mode='g', channel='1', passwd='studentID',
                                encrypt='wpa2', failMode='standalone', range=35)
        ap_list.append(ap)

    # Create stations with mobility
    for i in range(1, 6):
        sta = net.addStation('STA{}'.format(i), ip='10.0.0.{}/24'.format(i), encrypt='wpa2', failMode='standalone')
        sta_list.append(sta)

        # Set mobility parameters
        mobility_params = {
            'stations': sta,
            'mode': 'station',
            'max_x': 100,
            'min_x': 0,
            'max_y': 100,
            'min_y': 0,
            'min_v': 1,
            'max_v': 10
        }

        if i == 1:
            mobility_params.update({'start_x': 0, 'start_y': 0, 'end_x': 100, 'end_y': 100, 'time': '10s-20s'})
        elif i == 2:
            mobility_params.update({'start_x': 0, 'start_y': 0, 'end_x': 100, 'end_y': 100, 'time': '30s-60s'})
        elif i == 3:
            mobility_params.update({'start_x': 100, 'start_y': 100, 'end_x': 0, 'end_y': 0, 'time': '25s-60s'})
        elif i == 4:
            mobility_params.update({'start_x': 100, 'start_y': 100, 'end_x': 0, 'end_y': 0, 'time': '10s-20s'})
        elif i == 5:
            mobility_params.update({'start_x': 100, 'start_y': 100, 'end_x': 0, 'end_y': 0, 'time': '15s-20s'})

        net.plotGraph(max_x=120, max_y=120)

        net.startMobility(**mobility_params)

    print("*** Configuring wifi nodes")
    for ap in ap_list:
        ap.setIP('192.168.0.{}'.format(ap_list.index(ap) + 1), intf='ap-wlan0')

    print("*** Starting network")
    net.build()
    net.start()

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
