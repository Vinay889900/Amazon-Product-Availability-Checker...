import requests
from bs4 import BeautifulSoup

def check_amazon_availability(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(product_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        title_element = soup.find("span", {"id": "productTitle"})
        availability_element = soup.find("div", {"id": "availability"})

        if not title_element:
            print("Product title not found.")
            return

        title = title_element.get_text(strip=True)

        if not availability_element:
            print(f"Availability information for '{title}' not found.")
            return

        availability = availability_element.get_text(strip=True).lower()

        if "out of stock" in availability:
            print(f"{title} is currently out of stock on Amazon.")
        elif "in stock" in availability:
            print(f"{title} is available on Amazon.")
        else:
            print(f"Could not determine the availability of '{title}' on Amazon. Availability text: {availability}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

if __name__ == "__main__":
    product_url = "https://www.amazon.com/dp/B09G3HRMVB"  # Replace with your product URL
    check_amazon_availability(product_url)
