from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI

def topology():
    net = Mininet(controller=Controller, switch=OVSSwitch)

    # Adding the controller
    c0 = net.addController('c0')

    # Adding the buildings
    building1 = net.addSwitch('s1') 
    building2 = net.addSwitch('s2') 
    building3 = net.addSwitch('s3')  

    # Adding the server room
    server1 = net.addSwitch('s4')  
    server2 = net.addSwitch('s5')  

    # Adding lecture rooms in each building
    lecture_room1 = net.addSwitch('s6')  
    lecture_room2 = net.addSwitch('s7')  
    lecture_room3 = net.addSwitch('s8')  
    # Adding PCs for each lecture room
    pc1 = net.addHost('H1', ip='100.0.0.1/16') 
    pc2 = net.addHost('H2', ip='100.0.0.2/16')  
    pc3 = net.addHost('H3', ip='200.0.0.1/16')  
    pc4 = net.addHost('H4', ip='200.0.0.2/16')  
    pc5 = net.addHost('H5', ip='300.0.0.1/16')  
    pc6 = net.addHost('H6', ip='300.0.0.2/16')  
    pc7 = net.addHost('H7', ip='400.0.0.1/16')  
    pc8 = net.addHost('H8', ip='400.0.0.2/16')  
    pc9 = net.addHost('H9', ip='500.0.0.1/16')  
    pc10 = net.addHost('H10', ip='500.0.0.2/16')  
    pc11 = net.addHost('H11', ip='600.0.0.1/16')  
    pc12 = net.addHost('H12', ip='600.0.0.2/16')  
    # Adding servers in the server room
    server_host1 = net.addHost('Server', ip='12.0.0.1/8') 
    udp_server = net.addHost('UDP', ip='41.0.0.1/8')  

    # Creating links
    net.addLink(building1, lecture_room1)
    net.addLink(building1, lecture_room2)
    net.addLink(building2, lecture_room3)
    net.addLink(building2, lecture_room1)
    net.addLink(building3, lecture_room2)
    net.addLink(building3, lecture_room3)

    net.addLink(lecture_room1, pc1)
    net.addLink(lecture_room1, pc2)
    net.addLink(lecture_room2, pc3)
    net.addLink(lecture_room2, pc4)
    net.addLink(lecture_room3, pc5)
    net.addLink(lecture_room3, pc6)
    net.addLink(lecture_room4, pc7)
    net.addLink(lecture_room4, pc8)
    net.addLink(lecture_room5, pc9)
    net.addLink(lecture_room5, pc10)
    net.addLink(lecture_room6, pc11)
    net.addLink(lecture_room6, pc12)

    net.addLink(server1, server_host1)
    net.addLink(server2, udp_server)

    # Connecting the buildings and server room
    net.addLink(building1, building2)
    net.addLink(building2, building3)
    net.addLink(building3, building1)

    net.addLink(building1, server1)
    net.addLink(building2, server1)
    net.addLink(building2, server2)
    net.addLink(building3, server2)

    net.build()
    c0.start()
    building1.start([c0])
    building2.start([c0])
    building3.start([c0])
    server1.start([c0])
    server2.start([c0])

    # Starting Mininet CLI for manual configuration if needed
    CLI(net)

    # Stopping the Mininet network
    net.stop()

if __name__ == '__main__':
    topology()
