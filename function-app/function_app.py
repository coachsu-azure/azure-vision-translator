"""
    Azure AI 電腦視覺與翻譯工具(Function App 版)
"""
import logging
import azure.functions as func
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# 以下資訊可以從 Azure 電腦視覺服務取得(正式上線時不要直接把金鑰跟服務端點寫在程式碼裡)
# 填入金鑰
VISION_KEY = ''
# 填入端點
VISION_ENDPOINT = ''

# 以下資訊可以從 Azure 翻譯工具服務取得(正式上線時不要直接把金鑰跟服務端點寫在程式碼裡)
# 填入金鑰
TRANSLATOR_KEY=''
# 填入位置/區域
TRANSLATOR_REGION=''
# 填入文字翻譯的 Web API
TRANSLATOR_ENDPOINT=''

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

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_image_analysis")
def http_image_analysis(req: func.HttpRequest) -> func.HttpResponse:
    """
        Azure Functions HTTP trigger.
    """
    logging.info('Python HTTP trigger function processed a request.')

    image = req.params.get('image')
    if not image:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            image = req_body.get('image')

    if image:
        text_en = image_analysis(image)
        text_zh_hant = translator(text_en.text)
        return func.HttpResponse(
            f"<html><head><meta charset=\"utf-8\"></head><body>{text_zh_hant[0].translations[0].text}<br><img src='{image}' style=\"border: 1px solid #000; max-width:640px; max-height:640px;\"></body></html>", 
            headers={"Content-Type": "text/html"},
            status_code=200)
    else:
        return func.HttpResponse(
             "Please pass an image URL in the request body",
             status_code=200
        )
