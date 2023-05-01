# Importing Necessary modules
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pymongo
import csv
import mysql.connector as connector

# Taking input from the user
search_key = input("Enter Product Name : ").replace(" ", "")

# Generating the link to the filpkart page for the specific search key
flipcart_link = "https://www.flipkart.com/search?q=" + search_key

# Opening HTTP URLs
url_client = urlopen(flipcart_link)

# Reading the webpage
flipkart_page = url_client.read()

# Parsing the flipkart_page using html.parser
flipkart_html = bs(flipkart_page, 'html.parser')

# Storing all the products
all_products = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})

# Deleting unnecessary captures
del all_products[0:2]
del all_products[-1:-5:-1]

# Generatig Product Link
product_link = "https://www.flipkart.com" + \
    all_products[0].div.div.div.a['href']

# Downloading the dummy data of the webpage
product_request = requests.get(product_link)

# Parsing the product_request using html.parser
product_html = bs(product_request.text, 'html.parser')

# Storing all the reviews
reviews_list = product_html.findAll("div", {"class": "_16PBlm"})

# Deleting unnecessary capature
del reviews_list[-1]

# Creating a list to store data
data_list = []

# Storing all the review with name rating etc. in the form of dictionary in the data list
for i in reviews_list:
    # Name
    try:
        name = i.div.div.find("p", {"class": "_2sc7ZR _2V5EHH"}).text  # Name
    except:
        name = 'Flipkart_user'

    # Rating
    try:
        rating = i.div.div.find("div", {"class": "_3LWZlK _1BLPMq"}).text
    except:
        rating = "0"

    # Review
    try:
        review = i.div.div.find("p", {"class": "_2-N8zT"}).text
    except:
        review = "No Review"

    # Comment
    try:
        comment = i.div.div.find("div", {"class": ""}).text[:500]

    except:
        comment = "No Comment"

    data_list.append({
        "Name": name,
        "rating": rating,
        "review": review,
        "Comment": comment
    })

# Providing options to the user
print("Enter 1 to store data in csv file.")
print("Enter 2 to store data in MongoDB.")
print("Enter 3 to store data in MySQL.")
choice = input("Enter your choice: ")

try:
    choice = int(choice)
    match choice:
        case 1:
            # Storing the same data in respective csv file
            keys = data_list[0].keys()
            file_name = search_key + '.csv'
            with open(file_name, 'w', newline='', encoding='UTF-8') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(data_list)

            print(f"Data inserted into {file_name}")

        case 2:
            # Storing all the data in the MongoDB
            # Connecting to the mongo
            client = pymongo.MongoClient(
                "mongodb+srv://user1:user1@cluster0.zs8zanp.mongodb.net/?retryWrites=true&w=majority")

            # Creating a databse named review_scrapped_data
            db = client["review_scrapped_data"]

            # Creating respective collection for each search_key
            collection = db[search_key]

            # Inserting all the data at once using insert_many function
            collection.insert_many(data_list)

            print(
                f"Data inserted into MongoDB database = review_scrapped_data and collection = {search_key}")

        case 3:
            try:
                # Connecting to the MySQL
                db = connector.connect(host='localhost',
                                    port='3306',
                                    user='root',
                                    password='mysqlofarun')
                
                # Creating a cursor
                cur = db.cursor()

                # Creating a database
                query_db = "Create database if not exists review_scrapped_data"
                cur.execute(query_db)

                # Using the databse
                query_db = "use review_scrapped_data"
                cur.execute(query_db)

                # Creating a table
                query_table = "CREATE TABLE IF NOT EXISTS " + search_key + " (name varchar(30), rating varchar(1), review varchar(30), comment varchar(500))"
                cur.execute(query_table)

                # Storing data to the newly created table
                for i in data_list:
                    query = "INSERT INTO " + search_key + " VALUES (" + ", ".join("'" + str(value).replace("'", "''") + "'" for value in i.values()) + ")"
                    cur.execute(query)

                print(f"Data inserted into MySQL database = review_scrapped_data and table = {search_key}")

            except Exception as e:
                print(e)

        case _:
            print("Wrong input!")
except:
    print("An integer must be entered!")