import requests

def check_for_working(proxy):
    print(f"using {proxy}........")
    url = "https://www.google.com"
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            print("Proxy is working:", proxy)
            return True
        else:
            print("Proxy is not working:", proxy)
            return False
    except:
        print("Proxy Not Working")
        return False

def proxies():
    working_proxies = []
    with open("proxies.txt", "r") as file:
        for proxy in file:
            check = check_for_working(proxy)
            if check:
                working_proxies.append(proxy)

    return working_proxies

# if __name__ == "__main__":
def get_proxies():
    p = proxies()
    with open("proxies.txt", "w") as file:
        for proxy in p:
                file.write(proxy)
    return p
