import numpy as np
import cv2
import requests 
import io
import json
from matplotlib import pyplot as plt

# CHANGE REGION HERE
region = "westus"
URL = "https://"+region+".api.cognitive.microsoft.com/vision/v2.0/ocr"

HEADERS = {
    'Content-Type': 'application/octet-stream',
    # FILL SUBSCRIPTION KEY HERE
    'Ocp-Apim-Subscription-Key': "YOUR_SUBSCRIPTION_KEY"
}

def getImageData(image):
    buf = io.BytesIO()
    plt.imsave(buf, image, format='png')
    img_data = buf.getvalue()
    return img_data

def saveToJSON(result,filename):
    with open(filename, 'w') as outfile:  
        json.dump(result, outfile)
    print("Done.")

def getOCRFromImage(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img_data = getImageData(img)
    r = requests.post(URL,data=img_data,headers=HEADERS) 
    result = r.json()
    return result

def getStructuredText(data):

    structured_text = {}  
    structured_text['regions'] = [] 

    regions = data["regions"]

    for region in regions:

        regionToAdd = {}
        regionToAdd['lines'] = []

        lines = region["lines"]
        for l in lines:
            
            line = ""
            words = l["words"]
            for w in words:
                line += w["text"]
                line += " "

            regionToAdd['lines'].append(line)
        
        structured_text['regions'].append(regionToAdd)
            
    print(structured_text)
    return structured_text


path = 'imgs-2.jpg'
data = getOCRFromImage(path)
text = getStructuredText(data)
saveToJSON(text,"imgs-2.json")
