from packageManager import *
from scrapFunctions import get_brand
from scrapFunctions import get_link

# final directory to save images and description
dbDir = "/Volumes/HARDDRIVE/project_scrap/database_images/"

# unlike the scraper_with_predict.py, here we are using "headful mode" of webdriver
# but it can be changed to "headless mode" by replacing this block of code of that of scraper_with_predict.py
# initiate web driver
driver = webdriver.Chrome(ChromeDriverManager().install())
# precise URL to scrap
search_path = "https://www.zalando.fr/femme/?q=robe&p=1"
# use headful mode
driver.get(search_path)


# used to track pages since the click function cracks sometimes
# and it's a more proper way
page_count = 1
# parameter of the iteration
max_page = 10

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

        # generate random new name for image
        r1 = random.randint(1, 200001)
        r2 = random.randint(200001, 500001)
        lower_upper_alphabet = string.ascii_letters
        l1 = random.choice(lower_upper_alphabet)
        l2 = random.choice(lower_upper_alphabet)
        img_name = f"{r1}_{l1}_{r2}_{l2}.jpg"
        txt_name = f"{r1}_{l1}_{r2}_{l2}.txt"
        img_path = os.path.join(dbDir, img_name)
        txt_path = os.path.join(dbDir, txt_name)

        # save the image as .jpg file
        with open(img_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)

        # save the description as .txt file
        file = open(txt_path, "w", encoding="utf-8")
        # prepare content and store in content_str
        try:
            content_str = f"{linkList[i][0]}\n{linkList[i][1]}\n{brandList[i][0]}\n{brandList[i][1]}"
        except IndexError:
            content_str = ""
        n = file.write(content_str)
        file.close()

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