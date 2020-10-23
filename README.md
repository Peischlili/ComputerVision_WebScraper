## Computer Vision Web Scraper

This web scraper is an academic project containing 3 main parts:

* An object-detection model trained to detect dresses
* This object-detection model is used in scraping webpages each time it detects a dress, and fill a database with informations concerning the object detected (price, image, brand, etc.)
* Once the database filled, a neural network model is used and troncated at the last fully connected layer to act as a recommender. It takes an image as input, and outputs closest vector: the attributes of most similar image in our database (brand, price, etc.)

