import json
import re
import random
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth

class Scraper:
    __urls = ["http://192.168.178.193/status.html","http://192.168.178.112/status.html","http://192.168.178.138/status.html"]

    def __fetch(url: str, username: str, password: str):
        response = requests.get(url, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            return response.text
        else:
            raise(f"Failed to fetch the URL. Status code: {response.status_code}")

    def __insert_elem(ret, serial_number: int = 0, curr: int = 0, day: int = 0, total: int = 0):
            ret.append({
                'serial_number': serial_number,
                'curYieldW': curr,
                'dailyYieldW': day,
                'totalYieldW': total
            })

    def __parse(website: str) -> {int, int, int, int}:
        variable_names = ['webdata_sn', 'webdata_now_p','webdata_today_e','webdata_total_e']

        soup = BeautifulSoup(website, 'html.parser')
        script_tags = soup.find_all('script')

        values = []

        for variable in variable_names:
            # Regex pattern to match the variable
            pattern = re.compile(rf'{variable} = \"([0-9]*[.]*[0-9]*)\s*\"\s*;')
            for script in script_tags:
                if script.string:
                    match = pattern.search(script.string)
                    if match:
                        value = match.group(1)
                        if value.find(".") != -1:
                            value = float(value)
                            value = value * 1000
                        # Return the value as int
                        values.append(int(value))
                        break

        return tuple(values)

    def get_all(debug: bool = False):
        ret = []

        if debug:
            Scraper.__insert_elem(ret, 1234398572, random.randint(10, 200), 16000, 180000)
            Scraper.__insert_elem(ret, 1234398573, random.randint(10, 200), 17000, 190000)
            Scraper.__insert_elem(ret, 1234398574, random.randint(10, 200), 18000, 200000)
            return ret


        username = "admin"
        password = "admin"
        for url in Scraper.__urls: 
            try:
                res = Scraper.__fetch(url, username, password)
            except:
                continue

            serial_number, cur, day, total = Scraper.__parse(res)
            Scraper.__insert_elem(ret, serial_number, cur, day, total)

        return ret


if __name__ == "__main__":
    values = Scraper.get_all(True)
    print(values)