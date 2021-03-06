import json
import logging
import math
import pprint
from pprint import pformat

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from Parameters import page_add_leboncoin, url_leboncoin
from VirtualScraper import Scraper


class LebonCoin_Scraper(Scraper):
    def find_json_in_scripts(self, script_list):

        for script_item in script_list:
            if "window.__REDIAL_PROPS__" in script_item.text:
                self.logger.debug(
                    f"script_item window.__REDIAL_PROPS__ : {script_item.text} "
                )

                string_data = script_item.text.split("=", 1)[1]
                self.logger.debug(f"string_data : {pformat(string_data)} ")

                json_data = json.loads(string_data)[4]["data"]
                self.logger.debug(f"Raw JSON : {pformat(json_data)} ")

                return json_data

        logging.error("Non __REDIAL_PROPS__ on loaded Page")
        return None

    def get_appt_list(self, json_data):
        tmp_list_appt_1 = json_data["ads"]
        tmp_list_appt_2 = json_data["ads_alu"]
        tmp_list_appt = tmp_list_appt_1 + tmp_list_appt_2
        self.logger.debug(f"List appt : {pformat(tmp_list_appt)} ")

        # list_appt = list(filter(lambda x: x['publicationId'] is not None, list(tmp_list_appt)))

        return tmp_list_appt


if __name__ == "__main__":
    scraper = LebonCoin_Scraper(url_leboncoin, page_add_leboncoin)
    scraper.get_full_list_appt()
