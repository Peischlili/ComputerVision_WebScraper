## Computer Vision Web Scraper

This web scraper is an academic project containing 3 main parts:

* An object-detection model trained to detect dresses
* This object-detection model is used in scraping webpages each time it detects a dress, and fill a database with informations concerning the object detected (price, image, brand, etc.)
* Once the database filled, a neural network model is used and troncated at the last fully connected layer to act as a recommender. It takes an image as input, and outputs closest vector: the attributes of most similar image in our database (brand, price, etc.)

#### Methodologies:
###### Model training for detection:
  2 models involved: FasterRCNN with PyTorch and Yolov3
  * /FasterRCNN_training: trained with 30,000 images, within PyTorch under Google Colab env 
  * /Yolo3_training: trained with 17,000 images, under framework of Darknet under Google Colab env
  * Summary: FasterRCNN more accurate in terms of positive cases, but a lot slower to train

###### Scraping with detection model:
  * /WebScraper: 
  * Taking consideration the detection speed advantage of Yolov3 (22 milliseconds vs several seconds compared to FasterRCNN), the choice of model was made to Yolov3 for scraping part. The main website to build a database is zalando.fr and a dataset of 17,000 images was build thanks to the scraper_with_predict.py

###### Similarity research:
  * /WebScraper/similaritySearch was built with open source package faiss-cpu (since the project is not on the cloud for the moment, otherwise faiss-gpu will have computation capability advantage). 
  * with saved index and last layer long vectors, the search_index function finds k nearest neighbors in built dataset from our scrapped images.

###### Web application
  * /WebScraper/app.py
  * A simple web application was built with python Flask package, containing maining app.py and index.html, controling routes and views and displaying nearest neighbors
