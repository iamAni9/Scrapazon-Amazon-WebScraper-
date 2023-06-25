from flask import Flask, render_template, request, send_file
import scraping
import json

app = Flask(__name__)
app.static_folder = 'templates'

@app.route('/')
def index():
    return render_template('index.html', show_download=False, message="")

@app.route('/scrape', methods=['POST'])
def scrape():
    header_input = request.form['header']
    url = request.form['url']
    proxy_list = request.form['proxy_list']

    header = ({'User-Agent': header_input,'Accept-Language': 'en-US, en;q=0.5'})

    with open("proxies.txt", "w") as file:
        file.write(proxy_list)
    
    # Call the web_scraping function
    data = scraping.web_scraping(url, header)

    # Save data to a file
    with open("templates/scraping_data.json", "w") as file:
        file.write(data)

    with open("templates/scraping_data.json", 'r') as file:
        data = json.load(file)
        if len(data) == 0:
            return render_template('index.html', message="Scraping Failed, Try Again with new Proxies.....", show_download=True)
        else:
            # return send_file("scraping_data.json", as_attachment=True)
            return render_template('index.html', message="Success, you can download the file", show_download=True)

if __name__ == '__main__':
    app.run(debug=True)
