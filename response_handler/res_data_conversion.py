from logging import getLogger
import re
from pykakasi import kakasi
import jaconv

logger = getLogger(__name__)


class DataConversion:
    def __init__(self, row_list, description):
        self.kks = kakasi()
        self.data = row_list
        self.description = description
        self.result = {}

    def data_conversion(self):
        self.fetch_by_field_name()

    def fetch_by_field_name(self):
        """
        fetch value data from pre-defined label
        assume one contain one label
            remove "break" of not last label in case more than one labels in same row
        """
        breakflag = 0
        for rn in range(len(self.data)):
            # post code　
            if "〒" in self.data[rn]:
                post_code = self.data[rn]
                post_code = post_code.partition("〒")[2]
                breakflag += 1
                self.result_update("post_code", post_code)
            # ITEM2
            # ITEM3
            # ITEM4

            # when all item completed, exit the loop
            if breakflag == 1:
                break

    def result_update(self, str_key, str_value):
        result = self.result
        logger.debug("result to be update, key: {}, value: {}".format(str_key, str_value))
        if str_value:
            if not result.__contains__(str_key):
                result.update({str_key: str_value})
            elif str_value != result[str_key]:
                if str_value:
                    result.update({str_key: str_value})
        self.result = result
