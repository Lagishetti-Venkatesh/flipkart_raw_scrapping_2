from project_files.scrapping_page import scrap_data
from project_files.application_logging import application_logger
from project_files.database_operations import MongoDB_operations


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def scrap_the_data(product):
    """
    Will scrap the data from main page
    :param product: product name that you want to fetch data for.

    :return: collected data will be returned as a list of dictionaries / documents.
    """

    # creating Log object
    log_file = application_logger(product)
    log_obj = log_file.get_logger()

    # Creating Cloud Connection
    cloud_db_url = "mongodb+srv://VAMSHI:Venkat79@cluster0.eyco4.mongodb.net/?retryWrites=true&w=majority"

    # creating Data base object
    data_base = MongoDB_operations(cloud_db_url, product)

    try:
        # if db exists returns True and data else returns False and collection curosor.
        db_exists, collection = data_base.check_if_DB_exists(log_obj)

        if not db_exists:
            # scrapping the product data form the flipkart website
            data = scrap_data(product, log_obj)

            # pushing the Data to mongoDB
            success = data_base.push_to_mongo_cloud(collection, data, log_obj)
            log_obj.info(f"pushing the Collected data into mongoDb cloud : {success}")

            log_obj.info(f"Number of reviews collected {len(data)}")

            return data
        else:

            return collection

    except Exception as e:
        log_obj.error(f"while Running main code: {e}")

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
