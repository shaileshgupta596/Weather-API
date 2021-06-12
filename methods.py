from math import radians, cos, sin, asin, sqrt
import statistics
def haversine(lat1 ,lon1 ,lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return round(c * r)

def extendlist(list1,list2,list3):
    list1.extend(list2)
    list1.extend(list3)
    return list1

def tfhours(list1):
    h = statistics.median(list1)
    return round(h,2)

def sthours(list1):
    #list1=[32.5, 32.5, 32.3, 31.8, 31.5, 30.9, 30.8, 30.3, 30.0, 30.8, 32.0, 33.6, 35.4, 36.7, 37.7, 38.2, 38.4, 38.2, 36.6, 36.1, 35.1, 34.5, 33.9, 33.6]
    #list2=[32.3, 32.3, 32.2, 31.6, 31.3, 30.6, 30.5, 30.2, 29.8, 30.7, 31.8, 33.5, 35.2, 36.5, 37.5, 38.1, 38.2, 38.0, 36.4, 35.8, 34.9, 34.2, 33.5, 33.2]
    #list3=[31.8, 31.8, 31.7, 31.2, 30.9, 30.3, 29.9, 29.7, 29.3, 30.2, 31.4, 33.1, 34.9, 36.2, 37.2, 37.9, 38.1, 37.8, 36.2, 35.7, 34.6, 34.0, 33.4, 32.9]
    return round(statistics.median(list1),2)

def preferlocCondition(temp24,temp72):
    for i in temp24:
        for j in temp72:
            if abs(i-j)>20:
                return 0
    return 1



