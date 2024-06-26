#!/usr/bin/env python

import sys
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.node import RemoteController
from mn_wifi.node import OVSKernelAP
import random 
import time
import subprocess

def count_connected_stations(ap):
    result = subprocess.run(f"iw dev {ap}-wlan1 station dump | grep Station | wc -l", shell=True, stdout=subprocess.PIPE)
    count = int(result.stdout)
    print(f"{ap} has {count} stations connected.")

def topology():
    "Create a network."
    net = Mininet_wifi(controller=RemoteController, link=wmediumd, accessPoint=OVSKernelAP, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', wlans=2, ssid='ssid', position='50,50,0', ip='10.0.0.1/24', range=50)
    ap2 = net.addAccessPoint('ap2', wlans=2, ssid='ssid', position='50,150,0', ip='10.0.0.2/24', range=50)
    ap3 = net.addAccessPoint('ap3', wlans=2, ssid='ssid', position='150,50,0', ip='10.0.0.3/24', range=50)
    ap4 = net.addAccessPoint('ap4', wlans=2, ssid='ssid', position='150,150,0', ip='10.0.0.4/24', range=50)
    ap5 = net.addAccessPoint('ap5', wlans=2, ssid='ssid', position='100,100,0', ip='10.0.0.5/24', range=50)

    stations = []
    for i in range(1, 11):
        x = random.randint(0, 200)
        y = random.randint(0, 200)
        sta = net.addStation('sta%d' % i, ip='10.0.0.%d/24' % (10 + i), position='%d,%d,0' % (x, y), range=20)
        stations.append(sta)

    info("*** Adding controller\n")
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating Stations\n")
    net.addLink(ap1, intf='ap1-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap2, intf='ap2-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap3, intf='ap3-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap4, intf='ap4-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap5, intf='ap5-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)

    net.plotGraph(max_x=200, max_y=200)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])
    ap4.start([c0])
    ap5.start([c0])
    
    
    # Wait a bit for the stations to connect
    time.sleep(5)

     
    info("*** Checking connected stations\n")
    count_connected_stations('ap1')
    count_connected_stations('ap2')
    count_connected_stations('ap3')
    count_connected_stations('ap4')
    count_connected_stations('ap5')
     
     
    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
