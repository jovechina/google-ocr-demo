import json
import re
from logging import getLogger
from google.cloud.vision_v1 import AnnotateImageResponse
from functools import cmp_to_key
from response_handler.ocr_master_data import OcrMasterData

logger = getLogger(__name__)


class VisionResDataWrapper:
    # txt list response from response Google blocks
    txt_list = None

    # txt list with vertices from response Google blocks
    txt_list_w_vertices = None

    # txt list response from Google textAnnotations
    ta_txt_list = None

    # txt list with vertices which response from Google textAnnotations
    ta_txt_list_w_vertices = None

    # line width(x-coordinate)
    line_width = None

    # txt list of ocr result by row
    txt_list_by_row = None

    # txt list of ocr result by row - left half as one row and right row as another row
    # right rows is appended behind left rows
    txt_2_column_list_by_row = None

    def __init__(self, res_data):

        if isinstance(res_data, str):
            logger.debug("json load executed")
            res_data = json.loads(res_data)
        elif isinstance(res_data, AnnotateImageResponse):
            res_data = json.loads(AnnotateImageResponse.to_json(res_data))

        self.res_data = res_data
        self.description = res_data["fullTextAnnotation"]["text"].replace("\n", "")
        self.text_annotations = self.res_data["textAnnotations"]
        self.fix_mistake_words()
        self.conversion()

    def fix_mistake_words(self, txt=None):
        """
        modify identified wrong words in description
        """
        masking_list = OcrMasterData.mistake_words_mapping()
        if not txt:
            logger.debug("modify self.description with masking list")
            for k in masking_list.keys():
                if k in self.description:
                    self.description = self.description.replace(k, masking_list[k])
        if txt:
            for k in masking_list.keys():
                if k in txt:
                    txt = txt.replace(k, masking_list[k])
        return txt

    def conversion(self):
        # load text and boundingPloy from blocks
        self.txt_list, self.txt_list_w_vertices = self.extract_txt_from_blocks()
        logger.debug("txt_list:%s", self.txt_list)
        logger.debug("txt_list_w_vertices:%s", self.txt_list_w_vertices)

        # load text and vertices from txtAnnotation
        self.ta_txt_list, self.ta_txt_list_w_vertices = self.extract_txt_from_txt_annotation()
        logger.debug("ta_txt_list:%s", self.ta_txt_list)
        logger.debug("ta_txt_list_w_vertices:%s", self.ta_txt_list_w_vertices)

        # convert txt to row lines
        self.txt_list_by_row, self.txt_2_column_list_by_row = self.convert_txt_list_to_line(self.ta_txt_list_w_vertices)
        logger.debug("txt_list_by_row:%s", self.txt_list_by_row)
        logger.debug("txt_2_column_list_by_row:%s", self.txt_2_column_list_by_row)

    def extract_txt_from_blocks(self):
        """
        extract text and vertices from block
        :return: text list, text list with vertices
        """
        txt_list = []
        txt_list_w_vertices = []
        max_width = 0
        for block in self.blocks:
            for paragraph in block["paragraphs"]:
                for words in paragraph["words"]:
                    for symbols in words["symbols"]:
                        text = symbols["text"]
                        if type(text) == str:
                            text = self.fix_mistake_words(text)
                        try:
                            bounding_box = symbols["boundingBox"]["vertices"]
                            max_width = max_width if bounding_box[3]["x"] < max_width else bounding_box[3][1]
                        except Exception:
                            continue
                        txt_list.append(text)
                        txt_list_w_vertices.append([text, bounding_box])
        logger.debug("max_width: %s", max_width)
        self.line_width = max_width
        return txt_list, txt_list_w_vertices

    def extract_txt_from_txt_annotation(self):
        """
        extract text and vertices from textAnnotations
        :return: text list, text list with vertices
        """
        txt_input = self.text_annotations
        txt_list = []
        txt_list_w_vertices = []
        max_width = 0
        for item in txt_input:
            if len(item["description"]) > 50:
                continue
            if len(re.compile("[一-龥 ぁ-ん ァ-ン a-z A-Z 0-9 〒 \-]").findall(item["description"])):
                item["description"] = self.fix_mistake_words(str(item["description"]))
                txt_list.append(item["description"])
                txt_list_w_vertices.append(
                    [item["description"], item["boundingPoly"]['vertices']])
                max_width = max_width if item["boundingPoly"]['vertices'][3]["x"] < max_width else \
                    item["boundingPoly"]['vertices'][3]["x"]

        logger.debug("max_width: %s", max_width)
        self.line_width = max_width
        txt_list_w_vertices = sorted(txt_list_w_vertices, key=cmp_to_key(compare))
        return txt_list, txt_list_w_vertices

    def convert_txt_list_to_line(self, txt_list):
        """
        restructure txt list by lines/rows
        :param: txt_list with vertices
        :return: txt list by row
        """
        # sort list with by row, assume one line y coordinate gap within 6.

        line_list = [[]]
        line_list_left = [[]]
        line_list_right = [[]]
        x_coordinate_prev = 0
        line_number = 0
        middle_width = self.line_width // 2
        for item in txt_list:
            text = item[0]
            x_coordinate = item[1][0]["x"]
            if x_coordinate < x_coordinate_prev:
                line_number += 1
                line_list.append([])
                line_list_right.append([])
                line_list_left.append([])
            line_list[line_number].append(text)
            if x_coordinate <= middle_width:
                line_list_left[line_number].append(text)
            else:
                line_list_right[line_number].append(text)
            x_coordinate_prev = x_coordinate

        tmp_2_column_list = line_list_left + line_list_right
        txt_2_column_list = []
        for row in tmp_2_column_list:
            if row:
                p = re.compile("[一-龥 ぁ-ん ァ-ン a-z A-Z 0-9 〒 \-]")
                row = "".join(p.findall("".join(row)))
                # logger.debug("row: %s", row)
                if len(re.compile("[一-龥]").findall(row)):
                    row = self.fix_mistake_words(row)
                    txt_2_column_list.append(row)
        return line_list, txt_2_column_list


def compare(item1, item2):
    if item1[1][0]['y'] + 6 > item2[1][0]['y']:
        return 1
    else:
        return -1
