import requests
import json
from utils.env_variables import Endpoint, Headers

from logging import getLogger

logger = getLogger(__name__)


class GoogleVisionRestAPI:
    """
    Call google vision Rest API with google API Key authorization
    """
    image = None

    def __init__(self, image):
        self.image = image

    def document_text_detection(self):
        return self.__detection(detection_type="DOCUMENT_TEXT_DETECTION")

    def text_detection(self):
        return self.__detection(detection_type="TEXT_DETECTION")

    def __detection(self, detection_type):
        logger.debug("google %s started", detection_type)
        # define request data
        data = {
            "requests": [
                {
                    "image": {
                        "content": self.image.decode('utf-8')
                    },
                    "features": [
                        {
                            "type": detection_type
                        }
                    ],
                    "imageContext": {
                        "languageHints": "ja",
                        "cropHintsParams": {
                            "aspectRatios": [
                                0.8,
                                1,
                                1.2
                            ]
                        }
                    }
                }
            ]
        }
        response = requests.post(
            url=Endpoint.google_api,
            json=data,
            headers=Headers.content_headers_google
        )
        logger.debug("Google Vision API response Code: %s", response.status_code)
        logger.debug("Google %s completed", detection_type)
        res_data = json.loads(response.text)
        return res_data["responses"][0]
