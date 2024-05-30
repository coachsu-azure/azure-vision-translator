# azure-vision-translator
Azure 容器作業：整合電腦視覺與翻譯工具的測試範例

# 測試環境設定
 1. [建議] 先建立虛擬環境
 2. 安裝需要的套件

    `pip install -r requirements.txt`
 
 # 測試單機執行程式(app.py)
 1. 依據需要修改app.py (例如，電腦視覺的金鑰、服務端點、影像來源；翻譯工具的區域、金鑰、服務端點)
 2. 執行app.py

    `python app.py`

 # 測試flask網頁服務(web.py)
 1. 依據需要修改web.py (例如，電腦視覺的金鑰、服務端點；翻譯工具的區域、金鑰、服務端點)
 2. 執行web.py

    `python web.py`
 3. 開啟瀏覽器並前往 http://127.0.0.1:8080?image=https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg