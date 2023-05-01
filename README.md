# Scrapping-Flipkart
This Python project scrapes reviews of a product from Flipkart and provides three options to store the data: in a CSV file, MongoDB, or MySQL. It takes the user's input for the product name, generates a search link on Flipkart, and then scrapes the reviews for the first product in the search results.
It then stores the review data in a list of dictionaries with keys for name, rating, review, and comment.
It then provides the user with options to choose where to store the data, either in a CSV file, a MongoDB database, or a MySQL database.
If the user chooses to store the data in a CSV file, the script creates a CSV file with the product name as the filename and writes the review data to the file.
If the user chooses to store the data in MongoDB, the script connects to a MongoDB server, creates a new database named review_scrapped_data, creates a collection with the product name, and inserts the review data into the collection.
If the user chooses to store the data in MySQL, the script connects to a local MySQL server, creates a new database named review_scrapped_data if it does not already exist, creates a table with the product name if it does not already exist, and inserts the review data into the table.
The script handles exceptions if the user inputs the wrong type of data.
