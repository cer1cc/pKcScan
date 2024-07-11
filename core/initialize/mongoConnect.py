# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
from core.library import pymongo
from core.library import pymongo_MongoClient
import json
from core.initialize.printf import printfa

class MongoConnector:
    def __init__(self, host='localhost', port=27017, username=None, password=None, db_name=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        try:
            if self.username and self.password:
                self.client = pymongo_MongoClient(
                    f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/")
            else:
                self.client = pymongo_MongoClient(f"mongodb://{self.host}:{self.port}/")
            if self.db_name:
                self.db = self.client[self.db_name]
                # printfa(f"连接到数据库: {self.db_name}", "message")
            else:
                printfa(f"Connected to MongoDB at {self.host}:{self.port}", "info")
        except Exception as e:
            printfa(f"Error connecting to database: {e}", "warn")
            self.initialize_database()

    def initialize_database(self):
        try:
            self.client = pymongo_MongoClient(host=self.host, port=self.port)
            self.db = self.client[self.db_name]
            # 创建集合
            self.db.create_collection('FingerPrint')
            self.db.create_collection('Poc')
            printfa("Initialized database and collections successfully", "info")
        except Exception as e:
            printfa(f"Error during database initialization: {e}", "warn")
            self.client = None
            self.db = None

    def get_database(self, db_name):
        if not self.client:
            printfa("Not connected to MongoDB", "warn")
            return None
        return self.client[db_name]

    def close(self):
        if self.client:
            self.client.close()
            printfa("Connection to MongoDB closed", "info")

    def insert_json_to_collection(self, file_path, collection_name):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                collection = self.db[collection_name]
                if isinstance(data, list):
                    collection.insert_many(data)
                else:
                    collection.insert_one(data)
            printfa(f"Inserted data from {file_path} to collection: {collection_name}", "info")
        except Exception as e:
            printfa(f"Error inserting data to collection: {e}", "error")

    def delete_database(self, db_name):
        """
        删除指定的数据库
        :param db_name: 要删除的数据库名称
        """
        try:
            if self.client:
                self.client.drop_database(db_name)
                printfa(f"数据库 {db_name} 已删除", "message")
            else:
                printfa("Database client is not initialized", "warn")
        except Exception as e:
            printfa(f"Error deleting database: {e}", "warn")
    
# 示例用法
if __name__ == "__main__":
    mongo_connector = MongoConnector(host='localhost', port=27017, db_name='Poc')
    mongo_connector.connect()

    # 获取数据库对象
    db = mongo_connector.get_database('Poc')

    # 进行数据库操作
    if db:
        print("Collections:", db.list_collection_names())

    # 关闭连接
    mongo_connector.close()
