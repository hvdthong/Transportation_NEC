'''
Created on 20 Jul 2015

@author: vdthoang
'''
import json

from main.writeFile import write_file

def bus_services(path, name):
    #used to extract information from bus service
    with open(path + '/' + name) as data_file:    
        data = json.load(data_file)
    
    # get the types of bus services 
    list_types = []    
    list_types.append(data['types']['0'])
    list_types.append(data['types']['1'])
    list_types.append(data['types']['2'])
    
    print (list_types)
    
    # get the services number of bus
    list_services = []
    services = data['services']
    
    for service in services:
        no = service['no']
        route = service['routes']
        type_bus = int(service['type'])
        operator = service['operator']
        name = service['name']
        
        if (type_bus == 0):
            type_ = 'Trunk Bus Services'
        elif (type_bus == 1):
            type_ = 'Feeder Bus Services'
        elif (type_bus == 2):
            type_ = 'Nite Bus Services'
        else:
            print ('wrong with the type of bus -- break')
            break
        
        list_services.append(str(no) + '\t' + str(route) + '\t' + str(type_) + '\t' + str(operator) + '\t' + str(name))
        print (str(no) + '\t' + str(route) + '\t' + str(type_) + '\t' + str(operator) + '\t' + str(name))
    print (len(list_services))
    
def bus_stop(path, name):
    #used to extract information from bus stop
    with open(path + '/' + name) as data_file:    
        data = json.load(data_file)
    
#     print (data)
    list_stop = []
    for stop in data:
        no = stop['no']
        name = stop['name']
        list_stop.append(str(no) + '\t' + name)
        print (str(no) + '\t' + name)
    print (len(list_stop))
    
    write_file(path, 'bus_stop', list_stop) #extract texts and write it on csv file
    
def bus_stop_services(path, name):
    #used to extract information from bus service stop
    with open(path + '/' + name) as data_file:    
        data = json.load(data_file)
    
#     print (data)
    list_write = []
    for service in data:
        #print (each)
        list_service = data[str(service)]
#         print (str(service) + '\t' + str(list_service))
        
        for value in list_service:
            print (str(service) + '\t' + str(value))
            list_write.append(str(service) + '\t' + str(value))
            
    write_file(path, 'bus_stop_service', list_write) #extract texts and write it on csv file
            
if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums'
    
    #===========================================================================
    # name = 'bus-services.json'    
    # bus_services(path, name)
    #===========================================================================
    
    #===========================================================================
    # name = 'bus-stop.json'    
    # bus_stop(path, name)
    #===========================================================================
    
    name = 'bus-stop-services.json'    
    bus_stop_services(path, name)
