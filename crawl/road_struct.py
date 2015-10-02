'''
Created on 28 Jul 2015

@author: vdthoang
'''
from main.loadFile import load_file
from main.writeFile import write_file

def road_service(path, name):
    list_ = load_file(path, name)
    list_service = []
    for each in list_:
        split = each.split('\t')
        if (split[0] not in list_service):
            list_service.append(split[0])
    
    print (list_service)
    print (len(list_service))
    return list_service

def road_service_street(path, name):
    list_ = load_file(path, name)
    list_service = []
    for each in list_:
        split = each.split('\t')
        if (split[2] not in list_service and split[1] == 'subhead2'):
            list_service.append(split[2])
    
    print (list_service)
    print (len(list_service))
    return list_service

def road_structure(path, name):
    ## make the structure of roads and bus stops  
    
    list_ = load_file(path, name)
    list_headRoute = []
    
    list_all_routes = []
    list_route_head = []
    for line in list_: 
        split = line.split('\t')
        if (split[1] == 'subhead2'):
            list_headRoute.append(split[0] + '\t' + split[2])
                        
            if (len(list_route_head) > 0):
                list_all_routes.append(list_route_head)
                list_route_head = []            
        elif (split[1] == 'route'):
            list_route_head.append(split[2])
    
    ## catch the last element of routes
    if (len(list_route_head) > 0):
        list_all_routes.append(list_route_head)
        list_route_head = [] 
            
    print (len(list_headRoute))
    print (len(list_all_routes))
    
    list_struct = []
    for index in range(0, len(list_headRoute)):
        for route in list_all_routes[index]:
            list_struct.append(list_headRoute[index] + '\t' + route)
            print (list_headRoute[index] + '\t' + route)
    return list_struct
    
if __name__ == '__main__':
    ## construct the road's structure 
    
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name = 'bus_service_road.csv'
#     road_service(path, name)
#     road_service_street(path, name)

    write_file(path, 'bus_service_road_struct', road_structure(path, name))