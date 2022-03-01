import json
from google.cloud import vision
from google.cloud.vision_v1 import AnnotateImageResponse
from logging import getLogger

logger = getLogger(__name__)


class GoogleVisionClient:
    """
    Call google vision by vision client
    authorization by google service account
    """
    image = None
    client = None

    def __init__(self, content):
        self.image = vision.Image(content=content)
        self.client = vision.ImageAnnotatorClient()
        crop_hints_params = vision.CropHintsParams(aspect_ratios=[0.8, 1, 1.2])
        self.image_context = vision.ImageContext(crop_hints_params=crop_hints_params, language_hints=["ja"])

    def text_detection_to_json(self):
        try:
            response = self.text_detection()
            response_json = AnnotateImageResponse.to_json(response)
            response = json.loads(response_json)
            logger.debug(response['fullTextAnnotation']['text'])
            return json.dumps(response['textAnnotations'], indent=4, ensure_ascii=False)

        except Exception as e:
            print("exception in {0}, {1}".format("text_detection_to_json", e))
            raise (e)

    def text_detection(self):
        try:
            return self.client.text_detection(image=self.image, image_context=self.image_context)
        except Exception as e:
            print("exception in {0}, {1}".format("text_detection", e))
            raise (e)

    def document_text_detection_to_json(self):
        try:
            response = self.document_text_detection()
            response_json = AnnotateImageResponse.to_json(response)
            response = json.loads(response_json)
            # logger.debug(response['fullTextAnnotation']['text'])
            return json.dumps(response['textAnnotations'], indent=4, ensure_ascii=False)
        except Exception as e:
            print("exception in {0}, {1}".format("document_text_detection_to_json", e))
            raise (e)

    def document_text_detection(self):
        try:
            return self.client.document_text_detection(image=self.image, image_context=self.image_context)
        except Exception as e:
            print("exception in {0}, {1}".format("document_text_detection", e))
            raise (e)
