import pymongo
from elasticsearch import Elasticsearch


def insertElasticsearch(record):
    es = Elasticsearch([{'host': '192.168.1.112', 'port': 9200}])
    es.index(index="rent591", doc_type="rent", body=record)


def insertMongodb(record):
    body = record
    client = pymongo.MongoClient('mongodb://192.168.1.112:27017/')
    db = client["rent591"]
    Collection = db["rent"]
    Collection.insert_one(body)