from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from re import sub # regex

#########################
#########################

# top selling graphics cards on new egg, append &PageSize=96 to the URL for the max results
newegg_url = 'https://www.newegg.com/p/pl?Submit=Pers&sid=38&ste=53&Tid=6662&Depa=1&Category=38&pmid=D8A08728-5A92-4E99-A693-7B1DF3A23BE3&fbid=1&bosid=48&di=14-487-418%2c14-932-213%2c14-137-442%2c14-126-263%2c14-137-377%2c14-132-084%2c14-487-456%2c14-126-336%2c14-150-820%2c14-932-208%2c14-202-351%2c14-137-118%2c14-487-465%2c14-137-351%2c14-137-340%2c14-487-460%2c14-126-330%2c14-202-333&k=graphics%20card&PageSize=96'

# connecting to the URL and saving it to a var
uClient = uReq(newegg_url)
page_html = uClient.read()
uClient.close()

# run the page through BS4
page_soup = soup(page_html, "html.parser")

#grabs item divs
containers = page_soup.findAll("div", {"class":"item-container"})

# save to a CSV file
filename = "newegg_products.csv"
f = open(filename, "w")
# set the column headers
headers = "brand, rating, reviews, product_name, price_was, price_cur, shipping_cost\n"
f.write(headers)

# iterate over the items and extract information
for container in containers:
    # grab the brand
    brand = container.find("a",{"class":"item-brand"}).img['title']
    # grab the title of the item
    title = container.find("a",{"class":"item-title"}).text
    # grab the rating
    try:
        rating = container.find("i",{"class":"rating"}).get('class')[1].replace("rating-", "") + ' / 5'
    except AttributeError:
        rating = "No Rating"
        pass
    # grab the review count
    try:
        rating_count = container.find("span",{"class":"item-rating-num"}).text.replace("(","").replace(")","")
    except AttributeError:
        rating_count = '0'
        pass
    # grab past price
    try:
        past_price = "$" + container.find("span",{"class":"price-was-data"}).text.replace("," , "")
    except AttributeError:
        past_price = ""
        pass
    # grab current price
    # remove the unicode characters, the |\n from the beginning, and any commas
    current_price = container.find("li",{"class":"price-current"}).text.encode('ascii', 'ignore').decode('utf8').strip().replace('|\n',"").replace("," , "")
    # remove the '(## offers)' from the price
    current_price = sub(r'\([^()]*\)', '', current_price)
    # grab the cost of the shipping, remove the shipping word and remove free
    shipping = container.find("li",{"class":"price-ship"}).text.strip().replace(" Shipping", "").replace("Free", "$0.00")

    print("================================")
    print("brand: " + brand)
    print("title: " + title)
    print("rating: " + rating)
    print("reviews: " + rating_count)
    print("price_was: " + str(past_price))
    print("price_cur: " + str(current_price))
    print("shipping: " + shipping)
    print("================================\r\n")

    # write each product into a csv
    f.write(brand + ", "+ rating + ", " + rating_count + ", " +  title.replace("," , "|") + ", " + str(past_price) + ", " + str(current_price) + ", " + shipping + "\n")

# print how many items were exported
print("Exported " + str(len(containers)) + " products to a CSV")