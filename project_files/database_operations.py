import pymongo


class MongoDB_operations:

    def __init__(self, url_cloud, db_name):
        # Creating Cloud Connection
        self.client = pymongo.MongoClient(url_cloud)
        self.db_name = db_name

    def check_if_DB_exists(self, log_obj):
        """
        Description: To check if the Database exists or not

        :param log_obj: log object to grb the information or errors.
        :return: Boolean value
        """
        if self.db_name in self.client.list_database_names():
            log_obj.info(f"{self.db_name}  Already exists ")

            collection = self.client[self.db_name] # connecting to Existing Database
            review_collection = collection[str(self.db_name+'_reviews')] # connecting to cursor.
            data = list(review_collection.find())
            return True, data

        flipkart = self.client[self.db_name]  # DB creation
        review_collection = flipkart[self.db_name+ '_reviews']
        return False, review_collection

    def push_to_mongo_cloud(self, cursor, data_to_insert, log_obj):
        """
        will push the Data to the cloud
        :param log_obj: logging object to log the data.
        :param data_to_insert: List of documents that need to be stored in mongoDB cloud.
        :param cursor: mongodb cursor object to perform CRUD operations.

        :return: boolean value if the data inserted successfully
        """
        pushed_obj = cursor.insert_many(data_to_insert).inserted_ids
        if len(pushed_obj) == len(data_to_insert):
            log_obj.info(f'Pushed the Data: Successfull')
            return True
        else:
            log_obj.info(f'Pushed the Data: Failed')
            return False
