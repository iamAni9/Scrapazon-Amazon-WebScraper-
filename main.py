import scraping

header = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
url = "https://www.amazon.com/s?k=games&crid=6ANQQDZT3SM3&sprefix=gam%2Caps%2C363&ref=nb_sb_noss_2"

data = scraping.web_scraping(url, header)

with open("data_new.json", "w") as file:
    file.write(data)

