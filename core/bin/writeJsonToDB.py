# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
import os
import json
from core.initialize import globals
from core.initialize import system
from core.initialize import mongoConnect

def loadAllFPtoDB(mongo_connector_module):
    for filepath in system.getAllFilePath(globals.get_value("Fingerprint_Path")):
        mongo_connector_module.insert_json_to_collection(filepath,"FingerPrint")

def loadAllPoctoDB(mongo_connector_module):
    for filepath in system.getAllFilePath(globals.get_value("Poc_Path")):
        mongo_connector_module.insert_json_to_collection(filepath,"Poc")

def initialize():
    read=read_config()
    if not read.get('initialized'):
        mongo_connector_module = mongoConnect.MongoConnector(host='localhost', port=27017, db_name='module')
        mongo_connector_module.connect()
        mongoModuledb = mongo_connector_module.get_database('module')
        if mongoModuledb is not None:
            loadAllFPtoDB(mongo_connector_module)
            loadAllPoctoDB(mongo_connector_module)
            read["initialized"] = True;write_config(read)
        mongo_connector_module.close()

def reset():
    read=read_config()
    if  read.get('initialized'):
        mongo_connector_module = mongoConnect.MongoConnector(host='localhost', port=27017, db_name='module')
        mongo_connector_module.connect()
        mongo_connector_module.delete_database("module")
        read["initialized"] = False;write_config(read)
        mongo_connector_module.close()

def read_config():
    if not os.path.exists(globals.get_value("CONFIG_FILE_PATH")):
        return {"initialized": False}
    with open(globals.get_value("CONFIG_FILE_PATH"), 'r', encoding='utf-8') as config_file:
        return json.load(config_file)

def write_config(config):
    with open(globals.get_value("CONFIG_FILE_PATH"), 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, indent=4)