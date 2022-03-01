import unittest

import yaml

from google_vision.rest_api import GoogleVisionRestAPI
from google_vision.vision_client import GoogleVisionClient
from response_handler.res_data_conversion import DataConversion
from response_handler.vision_res_data_wrapper import VisionResDataWrapper
from utils.file_utils import FileUtils
from logging import getLogger, config

logger = getLogger(__name__)


class RestAPITestCase(unittest.TestCase):

    def test_fail_case_1(self):
        file_name = "<file_path>.jpg"
        data_convert = self.__data_convert(file_name)
        self.assertEqual("<value>", data_convert.result["<item>"])


    def __data_convert(self, file_name):
        # google client api
        # content = FileUtils.load_image(file_name=file_name)
        # vision_client = GoogleVisionClient(content)
        # res_data = vision_client.text_detection()

        # rest api
        rest_api = GoogleVisionRestAPI(FileUtils.load_image_b64(file_name=file_name))
        res_data = rest_api.document_text_detection()
        wrapper = VisionResDataWrapper(res_data)
        data_convert = DataConversion(wrapper.txt_2_column_list_by_row, wrapper.description)
        data_convert.data_conversion()
        return data_convert


if __name__ == '__main__':
    config.dictConfig(yaml.load(open("logging.yaml").read(), Loader=yaml.SafeLoader))
    unittest.main()
