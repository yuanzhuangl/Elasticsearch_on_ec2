import os

arrival_time = input("Please input range of time(), separated by commas : ")
arrival_time = arrival_time.split(",")
query_time = 0

with open ("result_in_stoptimes",'w'):
    os.system("""
    curl -XPOST "http://ec2-54-202-79-198.us-west-2.compute.amazonaws.com:9200/bustracks/stoptimes/_search?pretty " -d'
    {
        "query": {
            "range": {
                "arrival_time": {
                    "gte":  \"""" +str(arrival_time[0].strip())+ """\",
                    "lt":   \"""" +str(arrival_time[1].strip())+ """\"
                }
            }

        }

    }'>>result_in_stoptimes
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
with open("result_for_b",'w') as f:
    for i in Bus_name:
        f.write(i)
    tmp = "\n\n\n************************************************************************************************************\n" \
          "the query time is : " + str(query_time) + "ms." \
          "\n************************************************************************************************************"
    f.write(tmp)
