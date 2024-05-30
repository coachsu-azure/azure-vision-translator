#  參考文件
#  https://learn.microsoft.com/en-us/python/api/overview/azure/cognitiveservices-vision-computervision-readme?view=azure-python-previous
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

# 以下資訊可以從 Azure 電腦視覺服務取得(正式上線時不要直接把金鑰跟服務端點寫在程式碼裡)
C_KEY = '' # 填入金鑰
C_ENDPOINT = '' # 填入端點
IMAGE = '' # 影像

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
    
text_en = ImageAnalysis(IMAGE)
text_zh_Hant = Translator(text_en.text)
print(text_zh_Hant[0].translations[0].text)
