import os

query_time = 0
with open("result_in_stoptimes",'w'):
    os.system("""
                    curl -XGET "http://ec2-54-202-79-198.us-west-2.compute.amazonaws.com:9200/bustracks/stoptimes/_search?pretty" -d'
                    {
                      "aggs": {
                        "stop_id": {
                          "terms": {
                            "field": "stop_id",
                            "size": 3
                          },
                          "aggs": {}
                        }
                      },
                      "size": 0
                    }' >>result_in_stoptimes
            """)
bus_id = []
with open("result_in_stoptimes",'r') as f:
    for line in f:
        if line.find("key") != -1 :
            tmp_bus_id = line.split(":")[1].replace(',','').strip()
            bus_id.append(str(tmp_bus_id))
        if line.find("took") != -1 :
            query_time += int(line.split(":")[1].strip().replace(',', ''))
bus_id = set(bus_id)
with open("result_in_stops",'w'):
    for b_id in bus_id:
        os.system("""
                curl -XPOST "http://ec2-54-202-79-198.us-west-2.compute.amazonaws.com:9200/bustracks/stops/_search?pretty " -d'
                {
                    "query": {
                        "match": {
                             "stop_id":"""+ b_id +"""
                        }
                }
        }' >>result_in_stops
        """)
with open("result_in_stops","r") as f1:
    with open("result_for_d",'w') as f2:
        f2.write("the top 3 busiest bus is: \n")
        for line in f1:
            if line.find("name_stop") != -1 :
                f2.write(str(line.split(":")[1].strip().replace('"','').replace(',',''))+ "\n")
        f2.write( "\n\n\n************************************************************************************************************\n" \
              "the query time is : " + str(query_time) + "ms." \
              "\n************************************************************************************************************")