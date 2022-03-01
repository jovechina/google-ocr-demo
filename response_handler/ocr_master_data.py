from logging import getLogger

logger = getLogger(__name__)


class OcrMasterData:
    @staticmethod
    def mistake_words_mapping():
        mistake_words_list = {
            "ITEM CORET": "ITEM CORRECT",
        }
        return mistake_words_list

