import json
import re
import time

import requests

MAX_FL_ITERS = 8


class Parser:
    def __init__(self):
        self.json_regex = "\{.*?\}"

    def _find_last(self, obj, text):
        nums = [0]
        for i in range(MAX_FL_ITERS):
            if text.count(obj) > 2:
                fnd = text.find(obj, sorted(nums, reverse=True)[0] - 1)
            else:
                fnd = text.find(obj, sorted(nums, reverse=True)[0])
            if fnd != -1:
                nums.append(fnd)
            if fnd == sorted(nums, reverse=True)[0]:
                break
        return sorted(nums, reverse=True)[0] + 1

    def get_product_info(self, url):
        try:
            req = requests.get(url).text
            datalayer_list = req[req.find("dataLayer") + 12:req.find("</script>")].split(";")
            datalayer_jsons = []
            for dl_list in datalayer_list:
                if dl_list == "" and "stock_level" not in dl_list:
                    continue
                new_dl = dl_list[dl_list.find("{"):self._find_last("}", dl_list)]
                datalayer_jsons.append(json.loads(new_dl))
            nj = datalayer_jsons[-1]
            return {
                "status": "SUCCESS",
                "name": nj["pageview"]["data"].get("title"),
                "price_woVAT": nj["pageview"]["data"].get("czc_club_price_woVAT"),
                "price": nj["pageview"]["data"].get("discount_price_VAT"),
                "in_stock": True if nj["pageview"]["data"]["stock_level"] != 0 else False,
                "discount_value": nj["pageview"]["data"].get("discount_value"),
                "discount_percentage": nj["pageview"]["data"].get("discount_percentage")
            }
        except:
            return {
                "status": "ERROR",
                "message": "there was an error during data gathering phase please ensure that the identifier is right"
            }

    def get_seznam_info(self, url):
        try:
            req = requests.get(url).text
            jsons = re.findall(self.json_regex, req.strip())
            name_val = req.find('<span itemprop="name">') + 22
            name = req[name_val:req.find("</span>", name_val)]
            products = []
            total_price = 0
            for i in jsons:
                try:
                    prod = json.loads(i)
                    if prod.get("price") is None or prod.get("name") is None:
                        continue
                    products.append(prod)
                except ValueError as e:
                    continue
            products = sorted(products, key=lambda d: d["position"])
            for i in products:
                total_price += i["price"]
            return {
                "name": name,
                "total_price": total_price,
                "products": [i for i in products if i.pop("id") is not None]
            }
        except:
            return {
                "status": "ERROR",
                "message": "there was an error during data gathering phase please ensure that the identifier is right"
            }


if __name__ == '__main__':
    p = Parser()
    start = time.perf_counter()
    # print(p.get_seznam_info("https://www.czc.cz/9todcb1sbshncb4hg8qnfafbtg/seznam"))
    # print(p.get_product_info("https://www.czc.cz/sony-ps5-bezdratovy-ovladac-dualsense-cosmic-red/318356/produkt"))
    print(time.perf_counter() - start)
