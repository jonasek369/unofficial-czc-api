import json
import re
import time

import requests
import validators


class Parser:
    def __init__(self):
        self.session = requests.session()
        self.json_regex = "\{.*?\}"
        self.PRODUCT_MEMBERS_TO_REMOVE = [
            "worker",
            "http_session_id",
            "userLoggedin",
        ]

    @staticmethod
    def url_from_id(pid):
        return f"https://www.czc.cz/a/{pid}/produkt"

    @staticmethod
    def data_find(data, start, end, cut_star=True, addstart=0, addend=0):
        findstart = 0 if start is None or start is False else data.find(start)
        findend = len(data) if end is None or end is False else data.find(end)

        if cut_star and start is not None:
            return data[findstart + len(start) + addstart:findend + addend]
        else:
            return data[findstart + addstart:findend + addend]

    def parse_product(self, product_id):
        if isinstance(product_id, (float, int)):
            url = self.url_from_id(product_id)
        elif validators.url(product_id) and product_id.startswith("https://www.czc.cz/"):
            url = product_id
        else:
            url = self.url_from_id(product_id)
        req = self.session.get(url).text
        datalayer_start = self.data_find(req, "dataLayer = ", None, True)  # req[req.find("dataLayer"):]
        datalayer_lists = self.data_find(datalayer_start, None, "</script>", addend=-1).split(";")
        selected = ""
        for i in datalayer_lists:
            if i[0] == "e":
                selected = i
                break
        if not selected:
            return "ERROR: NO expone DataLayer"

        to_json = json.loads(selected[20:len(selected) - 1])

        return {
            key: val for key, val in to_json["data"].items() if key not in self.PRODUCT_MEMBERS_TO_REMOVE
        }

    def parse_seznam(self, seznam_id):
        if validators.url(seznam_id) and seznam_id.startswith("https://www.czc.cz/"):
            url = seznam_id
        else:
            url = f"https://www.czc.cz/{seznam_id}/seznam"
        req = self.session.get(url).text
        name_val = req.find('<span itemprop="name">') + 22
        name = req[name_val:req.find("</span>", name_val)]
        jsons = re.findall(self.json_regex, req.strip())
        product_jsons = []
        for _json in jsons:
            if '"price"' in _json:
                product_jsons.append(json.loads(_json))
        return {
            "name": name,
            "total_price": sum([i["price"] for i in product_jsons]),
            "prducts": product_jsons
        }
