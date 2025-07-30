import logging

# シンプルな logger 設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class TrackedText:
    """テキスト操作時にログを出力するシンプルクラス"""
    def __init__(self, text: str):
        self.text = text
        logger.info(f"Initialized with text: {self.text}")

    def set_text(self, new_text: str):
        logger.info(f"Text changed from '{self.text}' to '{new_text}'")
        self.text = new_text

    def display(self):
        logger.info(f"Displaying text: {self.text}")
        print(self.text)

    def error(self):
        try:
            raise ValueError("Intentional error")
        except Exception as e:
            logger.error(f"Error occurred: {e}")