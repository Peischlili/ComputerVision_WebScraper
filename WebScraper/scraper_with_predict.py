from packageManager import *
#from prediction import init_model
from prediction import predict_cat
from scrapFunctions import get_brand
from scrapFunctions import get_link

# set temporary image buffer folder and final directory
tmpDir = "/Users/peisch/code/WebScraper/test_scrap/tmp_images/"
dbDir = "/Users/peisch/code/WebScraper/test_scrap/database_images/"

# if it's your first time to execute the model and
# you don't have a saved Yolo3 model, please decomment this line to create model with trained weight
# the imported init_model function should also be decommented
#init_model("your/path/to/the/weights", "the/path/to/save/new/model")

# connect to web driver in headless mode
options = ChromeOptions()
options.headless = True
driver = webdriver.Chrome(chrome_options=options)
URI = "https://www.zalando.fr/femme/?q=robe"
driver.get(URI)

# used to track page number of scraping process
# starting from 1
page_count = 1
# parameter of the iteration : stopping criterium
max_page = 5

while page_count < max_page:
    # for each page call these functions to get 2 lists
    linkList = get_link(driver)
    brandList = get_brand(driver)

    for i in range(len(linkList)):
        # make browser shift to individual image link
        new_link = linkList[i][0]
        # from a url save content as bytes
        image_content = requests.get(new_link).content
        # convert bytes to _io.BytesIO
        image_file = io.BytesIO(image_content)
        # convert _io.BytesIO to PIL.Image.Image (readable by human)
        image = Image.open(image_file).convert('RGB')
        # set file_path to save file :
        image_name = "current_img.jpg"
        image_path = os.path.join(tmpDir, image_name)

        # create (override) the buffer file (so we have only 1 file in directory)
        with open(image_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        # create a txt file to store info
        txt_name = "current_img.txt"
        txt_path = os.path.join(tmpDir, txt_name)
        file = open(txt_path, "w", encoding="utf-8")
        # prepare content and store in content_str
        content_str = f"{linkList[i][0]}\n{linkList[i][1]}\n{brandList[i][0]}\n{brandList[i][1]}"
        n = file.write(content_str)
        file.close()

        # load saved model and predict if category searched present
        result = predict_cat('/Users/peisch/code/WebScraper/model.h5', image_path)
        # positive: generate new name for image and its attribute txt and save to permanent location
        if result[0][0] == 'Dress':
            # generate random new name for image
            r1 = random.randint(1, 20001)
            r2 = random.randint(20001, 50001)
            lower_upper_alphabet = string.ascii_letters
            l1 = random.choice(lower_upper_alphabet)
            l2 = random.choice(lower_upper_alphabet)
            new_img_name = f"{r1}_{l1}_{r2}_{l2}.jpg"
            new_txt_name = f"{r1}_{l1}_{r2}_{l2}.txt"
            # Move a file by renaming it's path
            new_img_path = os.path.join(dbDir, new_img_name)
            new_txt_path = os.path.join(dbDir, new_txt_name)
            os.rename(image_path, new_img_path)
            os.rename(txt_path, new_txt_path)
        # pause between each image
        time.sleep(2)

    # after iterations over the whole page, go to the next one
    page_count += 1

    # go to the next page (another way is to let driver get https://www.zalando.fr/femme/?q=robe&p=2)
    # unless it reaches certain page numbers: set that to 400 for example
    new_page_link = f"https://www.zalando.fr/femme/?q=robe&p={page_count}"
    driver.get(new_page_link)
    driver.implicitly_wait(2)

# I/O safety; make the navigator quit
driver.quit()