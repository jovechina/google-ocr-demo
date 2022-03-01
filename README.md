# google-ocr-demo
    demo code for using google vision api
    - [google rest api](google_vision/rest_api.py)
        call by API mode (https://vision.googleapis.com/v1/images:annotate)
        Authenticating by API key
    
    - [google vision client](google_vision/vision_client.py)
        call by Google vision client mode (ImageAnnotatorClient) 
        Authenticating as a service account
