import os

query_time = 0
name_stop = input("Please input the name of the stop: ")
with open("result_in_stops",'w'):
    os.system("""
                    curl -XGET "http://ec2-54-202-79-198.us-west-2.compute.amazonaws.com:9200/bustracks/stops/_search?pretty" -d'
                    {
                        "query":{
                            "match_phrase":{
                                "name_stop":\"""" + name_stop + """\"
                            }
                        }
                    }' >>result_in_stops
            """)
stop_id = []
with open("result_in_stops",'r') as f:
    for line in f:
        if line.find("stop_id") != -1 :
            tmp_stop_id = line.split(":")[1].replace('"','').replace(',','').strip()
            stop_id.append(str(tmp_stop_id))
        if line.find("took") != -1 :
            query_time += int(line.split(":")[1].strip().replace('"','').replace(',',''))
stop_id = set(stop_id)
with open("result_in_stoptimes",'w'):
    for s_id in stop_id:
        os.system("""
                curl -XPOST "http://ec2-54-202-79-198.us-west-2.compute.amazonaws.com:9200/bustracks/stoptimes/_search?pretty " -d'
                {
                    "query": {
                        "match": {
                             "stop_id": """+ s_id +"""
                        }
                }
        }' >>result_in_stoptimes
        """)


trip_id = []
with open("result_in_stoptimes",'r') as f:
    for line in f:
        if line.find("trip_id") != -1 :
            tmp_trip_id = line.split(":")[1].replace('"','').replace(',','').strip()
            if (tmp_trip_id in trip_id) == False:
                trip_id.append(str(tmp_trip_id))
        if line.find("took") != -1 :
            query_time += int(line.split(":")[1].strip().replace('"', '').replace(',', ''))
trip_id = set(trip_id)
with open("result_in_trips",'w'):
    for t_id in trip_id:
        os.system("""
                curl -XPOST "http://ec2-54-202-79-198.us-west-2.compute.amazonaws.com:9200/bustracks/trips/_search?pretty " -d'
                {
                    "query": {
                        "match": {
                             "trip_id": " """+ t_id +""" "
                        }
                }
        }' >>result_in_trips
        """)

Bus_name = []
with open("result_in_trips",'r') as f1:
    for line in f1:
        if line.find("trip_headsign") != -1 :
            tmp_trip_headsign = line.split(":")[1].replace('"','').replace(',','').strip()
            Bus_name.append(str(tmp_trip_headsign) + "\n")
        if line.find("took") != -1 :
            query_time += int(line.split(":")[1].strip().replace('"', '').replace(',', ''))
Bus_name = set(Bus_name)
with open("result_for_a",'w') as f:
    for i in Bus_name:
        f.write(i)
    tmp = "\n\n\n************************************************************************************************************\n" \
          "the query time is : " + str(query_time) + "ms." \
          "\n************************************************************************************************************"
    f.write(tmp)
