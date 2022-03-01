import base64
import io
import os
from logging import getLogger

logger = getLogger(__name__)


class FileUtils:

    @staticmethod
    def load_image(file_name):
        logger.debug("load_image started")
        logger.debug("image file %s process start:", file_name)
        with io.open(file_name, 'rb') as img:
            content = img.read()
        logger.debug("load_image completed")
        return content

    @staticmethod
    def load_image_b64(file_name):
        return base64.b64encode(FileUtils.load_image(file_name))

    @staticmethod
    def save_json(file_name, json_content):
        logger.debug("save_json started")
        filename = os.path.splitext(file_name)[0] + ".json"
        logger.debug("filename: %s", filename)
        with open(filename, "w", encoding='utf-8') as outfile:
            outfile.write(json_content)
            # json.dump(self.ocr_result, outfile)
        logger.debug("save_json completed")
