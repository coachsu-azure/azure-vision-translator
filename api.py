"""
    Azure AI 電腦視覺與翻譯工具(API 版)
"""
import os
import pathlib
from dotenv import load_dotenv
from flask import Flask, request
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# 如果.env存在，讀取.env檔案
env_path = pathlib.Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)

# 取得環境變數
VISION_KEY = os.getenv('VISION_KEY')
VISION_ENDPOINT = os.getenv('VISION_ENDPOINT')
TRANSLATOR_KEY = os.getenv('TRANSLATOR_KEY')
TRANSLATOR_REGION = os.getenv('TRANSLATOR_REGION')
TRANSLATOR_ENDPOINT = os.getenv('TRANSLATOR_ENDPOINT')

def image_analysis(image):
    """
        圖片分析(英文描述)
    """
    client = ComputerVisionClient(
        endpoint=VISION_ENDPOINT,
        credentials=CognitiveServicesCredentials(VISION_KEY)
    )
    analysis = client.describe_image(url=image, max_candidates=1, language="en")

    return analysis.captions[0]

def translator(target):
    """
        翻譯(英文翻譯成繁體中文)
    """
    text_translator = TextTranslationClient(
        endpoint=TRANSLATOR_ENDPOINT,
        credential=TranslatorCredential(TRANSLATOR_KEY, TRANSLATOR_REGION)
    )
    targets = []
    targets.append(InputTextItem(text=target))

    responses = text_translator.translate(content=targets, to=["zh-hant"], from_parameter="en")

    return responses

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def object_detection():
    """
        image: 影像 URL
    """
    image = request.args.get('image')

    text_en = image_analysis(image)
    text_zh_hant = translator(text_en.text)
    return text_zh_hant[0].translations[0].text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
