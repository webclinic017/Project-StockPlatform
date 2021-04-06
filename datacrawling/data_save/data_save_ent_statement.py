import pymongo
import traceback
import json
import time
from tqdm import tqdm
from tqdm import trange

def main():
    try:
        client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.kjrlb.mongodb.net/test_db_stock?retryWrites=true&w=majority")
        db = client.test_db_stock ## db name 
        print('MongoDB Connected.')

        inputfile="../json_file/find_state_removedmissingvalue.json"
        f = open(inputfile, 'r',encoding='UTF8')
        lines = f.readlines()

        for line in tqdm(lines):  
            line=json.loads(line)
            db.stockparam.insert_one(line)

    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('MongoDB Closed.')

if __name__ == "__main__":
    main()