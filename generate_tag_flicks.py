# Libraries used for fun.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pygal

file_name = 'elms-transceiver.log'

endpoint_m = []
timestamp_m = []
rssi_m = []
tagmac_m = []
motion = []

# Read the log file for data generation.
def read_file(file_name):
    with open(file_name) as f:
        lineList = f.readlines()
    return lineList

# Extract data from the log.
def get_the_beacon(beacon):

    collector = beacon.replace('[','').replace(']','').replace('{','').replace('}','').replace('"','')
    if  "rssi" in collector.split(':') or "tagMac" in collector.split(':'):
        collector = collector.split(':')[1]
    elif "readTimestamp" in collector.split(':') :
            collector = collector.split('T')[2][:8]
    return collector

# Generate csv file for the given data.
def generate_dataset(lineList):
    endpoint = []
    timestamp = []
    rssi = []
    tagmac = []
    for llist in range(len(lineList)):
        beacon = lineList[llist]
        flag = 1

        if len(beacon.split('beacons')) == 2 :
            ePoint = beacon.split('beacons')[1].split(']')[1].split(',')
            beacon = beacon.split('beacons')[1].split(']')[0].split(',')
            
            if "battery" not in beacon[2]:
                for beacon_data in range(0,len(beacon)):
                    check = beacon[beacon_data].replace('[','').replace(']','').replace('{','').replace('}','').replace('"','')
                    
                    if "isMotion" in check.split(':') and "true" in check.split(':') :
                        motion.append("true")
                        flag = 0

                    if "readTimestamp" in check.split(':') :
                        endpoint.append(ePoint[1].split(':')[1].replace('"',''))
                        timestamp += [get_the_beacon(beacon[beacon_data])]
                    elif  "rssi" in check.split(':'):
                        rssi.append(get_the_beacon(beacon[beacon_data]))
                    elif "tagMac" in check.split(':'):
                        tagmac.append(hex(int(get_the_beacon(beacon[beacon_data]))))

                        if(flag):
                            motion.append("false")
                        else:
                            flag = 1

    return endpoint, timestamp, rssi, tagmac

# Gnerate Csv file for the endpoint provided.
def generate_csv(endpoint, timestamp, rssi, tagmac):
    beacon_ep = pd.DataFrame({'Endpoint': endpoint,'readTimestamp': timestamp, 'rssi': rssi,"tagMac": tagmac,"isMotion": motion})
    beacon_ep.to_csv(file_name.split('.log')[0]+'.csv', index=False)

# Open Csv file.
def open_csv(file_name):
    beacon_csv = pd.read_csv(file_name)
    return beacon_csv

#@Bruce : fun Stuff
def generate_index_html(endpoint):
    fw = open("index.html","w+")

    with open("top_header.txt") as f:
        header = f.readlines()
        fw.writelines(header)
        
    fw.writelines("\n")
    for ePoint in  endpoint:
        fw.writelines('\t\t<option value ="'+str(ePoint)+'.svg"'+'>'+str(ePoint)+"</option>\n")

    with open("bottom_header.txt") as f:
        header = f.readlines()
        fw.writelines(header)

    fw.close()

# Render graph for the endpoint's tagmacs.
def generate_rssi_for_endpoint(beacon_csv):
    tags = beacon_csv['tagMac'].unique()
    for tag in tags : 
        ep_beacon = beacon_csv[beacon_csv['tagMac'] == tag]
        endPoint = ep_beacon['Endpoint'].unique()
        line_chart = pygal.Line(print_labels=True)
        line_chart.title = "tagMac: "+tag
        for i in endPoint:
            line_chart.add(str(i[:8]),ep_beacon[ep_beacon['Endpoint'] == i]['rssi'])
            line_chart.interpolate = 'cubic'
            line_chart.render_to_file(tag+'.svg')
    generate_index_html(tags)

if __name__ == '__main__' :

    link = read_file(file_name)
    endpoint_m, timestamp_m, rssi_m, tagmac_m = generate_dataset(link)
    generate_csv(endpoint_m, timestamp_m, rssi_m, tagmac_m )
    beacon_csv = open_csv(file_name.split('.log')[0]+'.csv')
    beacon = beacon_csv[beacon_csv['isMotion'] == False]
    generate_rssi_for_endpoint(beacon)
