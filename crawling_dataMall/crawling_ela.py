__author__ = 'vdthoang'
import pandas as pd
import elasticsearch as es
from elasticsearch import helpers
from time import time


# In[2]:
def retrieve(query, es_cluster, es_index, doc_type):
    resp = helpers.scan(client=es_cluster, query=query, scroll="25m"
                        , index=es_index, doc_type=doc_type, size=100, timeout="25m")
    results = []
    count = 0
    t0 = time()

    for hit in resp:
        results.append(hit['_source'])
        count += 1
        # print hit["_source"]
        if count % 1000 == 0:
            print "Processing %d records takes %f secs" % (count, time() - t0)

    df = pd.DataFrame.from_dict(dict([(i, x) for i, x in enumerate(results)]), orient='index')
    print "Done processing %d records, which took %f secs" % (count, time() - t0)
    return df


###############################################################
###############################################################
# download data from dataMall
es_cluster = es.Elasticsearch(['10.0.109.37:9200', '10.0.109.38:9200', '10.0.109.39:9200', '10.0.109.40:9200', '10.0.109.41:9200'], timeout=25, max_retries=10, retry_on_timeout=True)
query = {"query": {"bool": {"must": [{"range": {"timestamp": {"gt": "1461513600","lte": "1461556800"}}}],"must_not": [ ],"should": [ ]}}}
hop_df = retrieve(query, es_cluster, "datamall_bus_arrival_2016", "arrTime")
hop_df.to_json(("datamall_bus_arrival_2016.json"), orient="records")
hop_df.to_pickle(("datamall_bus_arrival_2016.dat"))

