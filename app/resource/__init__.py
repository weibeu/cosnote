from mongoengine import connect


def initialize_mongo_connection(configs):
    connect(configs.MONGODB_DATABASE, host=configs.MONGODB_URI)
