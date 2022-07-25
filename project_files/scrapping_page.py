import urllib.error
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs


def fetch_webpage(web_address, log_obj):
    """
    To fetch the web address and return HTMl parsed object
    :param log_obj: logging object
    :param web_address: web url to be fetched and parsed
    :return: HTML parsed object
    """
    try:
        # redirecting to link.
        link = requests.get(web_address)
        link.encoding = 'utf-8'
        parsed_html = bs(link.text, "html.parser")
    except urllib.error.HTTPError as e:
        log_obj.Error(f"while fetching the{web_address} Error :" + str(e))
    return parsed_html


def scrap_data(product, log_obj):
    """
    Will scrap the data from the flipkart page of particular product

    :param log_obj: logging object to log the data
    :param product: product name for which the reviews' data needs to be collected.
    :return: list of Document objects
    """
    review_data = []
    try:
        # Searching for a product in flipkart website
        flask_url = "https://www.flipkart.com/search?q=" + product
        log_obj.info(f" product searching url {flask_url}")

        try:
            # Reading the fipakrt page
            uclient = uReq(flask_url)
            flipkart_page = uclient.read()
            uclient.close()
            log_obj.info(f"fetched web page should be of class type bytes: {type(flipkart_page)}")

        except urllib.error.HTTPError as e:
            log_obj.Error("while fetching the Prodict details :" + str(e))

        try:
            # Parsing the search products page into html page
            flipkart_html = bs(flipkart_page, "html.parser")
            log_obj.info(f"Parsed web page should be of class type BeautifulSoup: {type(flipkart_html)}")

            # retrieving the first page of the product
            big_boxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del big_boxes[0:3]  # deleting the first 3 objects of list
            box = big_boxes[0]
            product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
            product_html = fetch_webpage(product_link, log_obj)
            log_obj.info(f"fetched webpage of first product url: {product_link}")
            df_1 = product_html.find_all('div', {"class": "_16PBlm"})

            for i in range(len(df_1) - 1):
                name = df_1[i].find_all('div', {"class", 'row _3n8db9'})[0].p.text
                title = df_1[i].div.div.div.p.text
                rating = df_1[i].div.div.div.div.text
                comment = df_1[i].div.div.find_all('div', {'class': ""})[0].div.text
                document = {'name': name, 'rating': rating, 'title': title, 'comments': comment}
                review_data.append(document)

            # fetching and parsing the product web page
            prod_html = fetch_webpage(product_link, log_obj)

            # finding All reviews in page and moving to first page of the Reviews
            all_reviews_link = prod_html.find('div', {'class': "col JOpGWq"})

            # getting the web address of the all reviews.
            all_reviews = "https://www.flipkart.com" + all_reviews_link.find_all('a')[-1]['href']

            # fetch and parsing the web page of the all reviews
            r1 = fetch_webpage(all_reviews, log_obj)

            result = r1.find_all('div', {"class": "_1AtVbE col-12-12"})

            del result[0:3]
            for i in range(1, len(result) - 1):
                r1_name = result[i].find_all('div', {"class", 'row _3n8db9'})[0].p.text
                r1_rating = result[i].div.div.div.div.div.text
                r1_title = result[i].div.div.div.div.p.text
                r1_comments = result[i].div.div.div.find_all('div', {"class": ''})[0].text
                document = {'name': r1_name, 'rating': r1_rating, 'title': r1_title, 'comments': r1_comments}
                review_data.append(document)

            r1_results = result

            # moving to next page and extracting the data from that page
            rnext = r1_results[-1].find_all('a', {"class": "_1LKTO3"})
            log_obj.info("Pages Visited: ")

            while len(rnext) != 0:
                rnext = r1_results[-1].find_all('a', {"class": "_1LKTO3"})
                target_page = rnext[-1].text
                if target_page == "Next":

                    next_page = "https://www.flipkart.com" + rnext[-1]['href']

                    # fetching and parsing the next page
                    prod_html = fetch_webpage(next_page, log_obj)

                    r1_results = prod_html.find_all('div', {"class": "_1AtVbE col-12-12"})
                    log_obj.info(f'{next_page[-7:].replace("&", "")}')
                    print("=" * 120)
                    del r1_results[0:3]

                    try:
                        for i in range(1, len(r1_results) - 1):
                            r1_name = r1_results[i].find_all('div', {"class", 'row _3n8db9'})[0].p.text
                            r1_rating = r1_results[i].div.div.div.div.div.text
                            r1_title = r1_results[i].div.div.div.div.p.text
                            r1_comments = r1_results[i].div.div.div.find_all('div', {"class": ''})[0].text
                            document = {'name': r1_name,
                                        'rating': r1_rating,
                                        'title': r1_title,
                                        'comments': r1_comments
                                        }
                            review_data.append(document)

                    except IndexError as Index:
                        log_obj.error(f" Index Error Occurred: {Index}")
                        return review_data

                else:
                    break
        except None as n:
            log_obj.warning(f"no Reviews found for the product : {n}")

        return review_data
    except Exception as e:
        log_obj.error(f"Error While scraping the Data: {e}")
        return review_data

