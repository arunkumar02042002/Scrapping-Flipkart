# Importing Necessary modules
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pymongo
import csv

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
    #Name
    try:
        name = i.div.div.find("p", {"class": "_2sc7ZR _2V5EHH"}).text  # Name
    except:
        name='Flipkart_user'
    
    #Rating
    try:
        rating = i.div.div.find("div", {"class": "_3LWZlK _1BLPMq"}).text
    except:
        rating = "0"

    #Review
    try:
        review = i.div.div.find("p", {"class": "_2-N8zT"}).text
    except:
        review = "No Review"
    
    # Comment
    try:
        comment = i.div.div.find("div", {"class": ""}).text

    except:
        comment = "No Comment"
    
    data_list.append({
        "Name": name,
        "rating": rating,
        "review": review,  
        "Comment": comment
    })

# Storing the same data in respective csv file
keys = data_list[0].keys()
file_name = search_key + '.csv'
with open(file_name, 'w', newline='', encoding='UTF-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data_list)

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
