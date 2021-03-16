import torch
import os
import json
import csv
import lmdb
from tqdm.auto import tqdm


#create lmdb database:



##Load config file:
with open("/data/cold/config.json","r") as file:
    config = json.load(file)
    cold_data = config["cold_storage"]
    datapath = config["data_storage"]
    train_percent = config["percent_train"]

env = lmdb.open(datapath,map_size=1e12)



file_list = [name for name in os.listdir(cold_data) if os.path.isfile(os.path.join(cold_data,name))]
for i in tqdm(range(len(file_list))):
    cold_path = os.path.join(cold_data,file_list[i])
    with open(cold_path,"r") as file:
        data = json.load(file)
        with env.begin(write=True) as txn:
            for j in range(len(data)):
                for k in (range(len(data[j]))):
                    key = str(i)+str('.')+str(j)+str('.')+str(k)

                    
                    def truncate(ldata):
                        return list(map(lambda x: round(x, 8), ldata))

                    zz = list(map(lambda x: truncate(x) if isinstance(x, list) else x, data[j][k]))
                    zz = json.dumps(zz)

                    txn.put(key.encode(),zz.encode())





