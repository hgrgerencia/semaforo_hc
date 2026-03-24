from pymongo import MongoClient
import pandas as pd
import uuid
import streamlit as st
from util.decoradores import try_except_decorator
from util.convert_to_df import convert_docs_to_df

# Conexión a MongoDB
client = MongoClient(st.secrets["MONGO_CLIENT"])
db_mongo = client['ribsdb']

# funcion para devolver una lista de las coleeciones en mi base de datos de mongodb
def obtener_colecciones():
    return db_mongo.list_collection_names()

class FactoryMongoDB:
    collection_name = ""
    sort_collection = ""
    def __init__(self, collection_name, sort_collection = ""):
        self.collection_name = collection_name
        self.sort_collection = sort_collection
    
    @try_except_decorator
    def get_another_collection(self, collection_name, sort = ""):
        docs = db_mongo[collection_name].find()
        if sort != "":
            docs = docs.sort(sort, 1)
        data = convert_docs_to_df(docs)
        return data
        
    @try_except_decorator
    def get_all_collection(self,direction=1):
        docs = db_mongo[self.collection_name].find().sort(self.sort_collection, direction)
        data = convert_docs_to_df(docs)
        return data

    @try_except_decorator
    def get_one_collection(self, id):
        docs = db_mongo[self.collection_name].find({"id": id})
        data = convert_docs_to_df(docs)
        return data

    @try_except_decorator
    def get_one_collection_by(self, field, value):
        docs = db_mongo[self.collection_name].find({field: value})
        data = convert_docs_to_df(docs)
        return data
    
    @try_except_decorator
    def get_one_another_collection(self, collection_name,id):
        docs = db_mongo[collection_name].find({"id": id})
        data = convert_docs_to_df(docs)
        return data
    @try_except_decorator
    def insert_one_collection(self, data):
        data["id"] = str(uuid.uuid4())
        result =   db_mongo[self.collection_name].insert_one(data)
        return result
    @try_except_decorator
    def delete_one_collection(self, id):
        result = db_mongo[self.collection_name].delete_one({"id": id})
        return result
    @try_except_decorator
    def update_one_collection(self, id, data):
        result = db_mongo[self.collection_name].update_one({"id": id}, {"$set": data})
        return result