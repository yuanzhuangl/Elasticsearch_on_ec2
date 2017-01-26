import os

route_id = input("Please input the route id : ")
trip_headsign = input("Please input the bus name : ")

query_time = 0

with open ("result_in_trips",'w'):
    os.system("""
    curl -XGET "http://ec2-54-202-79-198.us-west-2.compute.amazonaws.com:9200/bustracks/trips/_search?pretty" -d'
    { "query" : {
            "bool" : {
                "must" : {
                    "match_phrase" : {
                        "route_id": \"""" +str(route_id.strip())+ """\"
                    }
                },
                "must" : {
                    "match_phrase" : {
                        "trip_headsign": \"""" +str(trip_headsign.strip())+ """\"
                    }
                }
            }
        }
    }' >>result_in_trips
    """)


trip_id = []
with open("result_in_trips",'r') as f:
    for line in f:
        if line.find("trip_id") != -1 :
            tmp_trip_id = line.split(":")[1].replace('"','').replace(',','').strip()



            if (tmp_trip_id in trip_id) == False:
                trip_id.append(str(tmp_trip_id))
        if line.find("took") != -1 :
            query_time += int(line.split(":")[1].strip().replace('"', '').replace(',', ''))
trip_id = set(trip_id)

with open("result_in_stoptimes",'w'):
    for t_id in trip_id:
        os.system("""
                curl -XPOST "http://ec2-54-202-79-198.us-west-2.compute.amazonaws.com:9200/bustracks/stoptimes/_search?pretty " -d'
                {
                    "query": {
                        "match_phrase": {
                             "trip_id": " """+ t_id +""" "
                        }
                }
        }' >>result_in_stoptimes
        """)

stop_and_sequence = []
with open("result_in_stoptimes",'r') as f:
    n = -1
    for line in f:
        if line.find("trip_id") != -1 :
            tmp = ''
            tmp += str(line.split(":")[1].replace('"','').replace(',','').strip()) + ": "
        if line.find("stop_id") != -1 :
            tmp += str(line.split(":")[1].replace('"','').replace(',','').strip()) + "  "
        if line.find("stop_sequence") != -1 :
            tmp += str(line.split(":")[1].replace('"', '').replace(',', '').strip()) + "\n"
            stop_and_sequence.append(tmp)
        if line.find("took") != -1 :
            query_time += int(line.split(":")[1].strip().replace('"', '').replace(',', ''))
# stop_id_and_sequence = set(stop_and_sequence)
# print(stop_id_and_sequence)



with open("result_in_stops",'w'):
    for item in stop_and_sequence:
        stop_id = item.split(":")[1].split("  ")[0]
        os.system("""
                curl -XPOST "http://ec2-54-202-79-198.us-west-2.compute.amazonaws.com:9200/bustracks/stops/_search?pretty " -d'
                {
                    "query": {
                        "match": {
                             "stop_id": """+ stop_id +"""
                        }
                }
        }' >>result_in_stops
        """)
with open("result_in_stops",'r') as f1:
    for line in f1:
        if line.find("stop_id") != -1 :
            stop_id = ''
            name_stop = ''
            stop_id = str(line.split(":")[1].replace('"','').replace(',','').strip())
        if line.find("name_stop") != -1 :
            name_stop = str(line.split(":")[1].replace('"','').replace(',','').strip())
            for i in range(0,len(stop_and_sequence)):
                stop_and_sequence[i] = stop_and_sequence[i].replace(stop_id,name_stop)
        if line.find("took") != -1 :
            query_time += int(line.split(":")[1].strip().replace('"', '').replace(',', ''))

with open("result_for_c",'w') as f:
    for i in stop_and_sequence:
        f.write(i)
    tmp = "\n\n\n************************************************************************************************************\n" \
          "the query time is : " + str(query_time) + "ms." \
          "\n************************************************************************************************************"
    f.write(tmp)