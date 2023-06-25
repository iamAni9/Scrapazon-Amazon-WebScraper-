from bs4 import BeautifulSoup
import requests
import json
import proxy

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_stars(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available


# if __name__ == '__main__':
def web_scraping(url, headers):

    # Adding the user agent 
    # HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    HEADERS = headers
    
    # Change the URL accordingly
    # URL = "https://www.amazon.com/s?k=gta+5&crid=218FNTAHVUHLW&sprefix=gta+5%2Caps%2C506&ref=nb_sb_noss_1"
    URL = url
    
    proxy_list = proxy.get_proxies()
    
    if len(proxy_list) == 0:
        print("Empty list")
    else: 
        links = ""
        for p in proxy_list:
            print(f"using {p} proxy........")
            try:
                # webpage = requests.get(URL, headers=HEADERS, proxies=p)
                webpage = requests.get(URL, headers=HEADERS, proxies={"http": p, "https": p}, timeout=5)
                if webpage.status_code == 200:
                    print("Website Data")
                    soup = BeautifulSoup(webpage.content, "html.parser")
                    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
                    break  
                else:
                    print("Proxy not working for scraping")
            except:
                print("Not Working")
                pass
            
        # For storing the links
        links_list = []

        # Looping for extracting links from Tag Objects
        for link in links:
                links_list.append(link.get('href'))

        d = {"title":[], "price":[], "stars":[], "reviews":[],"availability":[]}
        
        # # Looping for extracting product details from each link 
        
        for link in links_list:
                for p in proxy_list:
                    try:
                        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS, proxies={"http": p, "https": p}, timeout=5)
                        if new_webpage.status_code == 200:
                            print("Scraping products data")
                            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
                            # Function calls to display all necessary product information
                            d['title'].append(get_title(new_soup))
                            d['price'].append(get_price(new_soup))
                            d['stars'].append(get_stars(new_soup))
                            d['reviews'].append(get_review_count(new_soup))
                            d['availability'].append(get_availability(new_soup))
                            break
                        else:
                            print("Failed to scrap product data")
                    except:
                        print("Proxy failed to scrap product data")
                        pass

        print(d)
    
        # Creating a list to store each product as a separate dictionary
        products = []

        # Getting the number of products based on the 'title' key
        num_products = len(d['title'])

        # Looping through the range of products to storing them in new list in product by product sequence
        for i in range(num_products):
            product = {
                "title": d["title"][i],
                "price": d["price"][i],
                "stars": d["stars"][i],
                "reviews": d["reviews"][i],
                "availability": d["availability"][i]
            }
            products.append(product)

        # Converting the list of products to JSON format
        json_data = json.dumps(products)

        return json_data

        # # Writing the JSON data to a file
        # with open("data.json", "w") as file:
        #     file.write(json_data)