from flask import Flask, request
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

# 以下資訊可以從 Azure 電腦視覺服務取得(正式上線時不要直接把金鑰跟服務端點寫在程式碼裡)
C_KEY = '' # 填入金鑰
C_ENDPOINT = '' # 填入端點

# 以下資訊可以從 Azure 翻譯服務取得(正式上線時不要直接把金鑰跟服務端點寫在程式碼裡)
T_REGION = '' # 填入位置/區域
T_KEY = '' # 填入金鑰
T_ENDPOINT = '' # 填入文字翻譯的 Web API

def ImageAnalysis(image):
    client = ComputerVisionClient(
        endpoint=C_ENDPOINT,
        credentials=CognitiveServicesCredentials(C_KEY)
    )
    analysis = client.describe_image(url=image, max_candidates=1, language="en")

    return analysis.captions[0]

def Translator(target):
    text_translator = TextTranslationClient(
        endpoint=T_ENDPOINT,
        credential=TranslatorCredential(T_KEY, T_REGION)
    )
    targets = []
    targets.append(InputTextItem(text=target))

    responses = text_translator.translate(content=targets, to=["zh-hant"], from_parameter="en")
    
    return responses

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def object_detection():
    IMAGE = request.args.get('image')

    text_en = ImageAnalysis(IMAGE)
    text_zh_Hant = Translator(text_en.text)
    return text_zh_Hant[0].translations[0].text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
