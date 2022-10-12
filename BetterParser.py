import json
import time

import requests
import validators


class Parser:
    def __init__(self):
        self.session = requests.session()
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
        elif not validators.url(product_id):
            if not product_id.startswith("https://www.czc.cz/"):
                return "ERROR: INVALID URL"
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
            return "ERROR: NO exponeaDataLayer"

        to_json = json.loads(selected[20:len(selected) - 1])

        return {
            key: val for key,val in to_json["data"].items() if key not in self.PRODUCT_MEMBERS_TO_REMOVE
        }

    def __del__(self):
        self.session.close()


parser = Parser()
start = time.perf_counter()
print(parser.parse_product(356642))
end = time.perf_counter()
print((end - start) * 1000, "ms")
