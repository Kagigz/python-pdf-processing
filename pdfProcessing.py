try:
    import collections.abc
except ImportError:
    pass
from wand.image import Image as wi
import numpy as np
import cv2
import requests 
import io
from matplotlib import pyplot as plt
import json
import re

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


def getData(path):
    f = open(path,"r")
    json_data = f.read()
    data = json.loads(json_data)
    f.close()
    return data

def saveToJSON(result,filename):
    with open(filename, 'w') as outfile:  
        json.dump(result, outfile)
    print("Done.")


def getDocumentStructure(numberOfPages,jsonFileName,pattern,titleDetection):

    documentJSON = {}
    documentJSON['pages'] = []

    for i in range(1,numberOfPages+1):
        
        page = {}
        page['id'] = i
        page['paragraphs'] = []
        
        path = jsonFileName + str(i) + ".json"
        data = getData(path)
        regions = data['regions']
        
        number = ""
        title = ""

        paragraph = {
            'number': '',
            'title': '',
            'text': ''
        }

        detectTitle = False
        textDetected = False

        for r in regions:
            for l in r['lines']:

                if re.search(pattern,l):
                    paragraph['number'] = number
                    number = l
                    detectTitle = True

                if detectTitle:

                    if(titleDetection):
                        paragraph['title'] = title

                    if(textDetected):
                        page['paragraphs'].append(paragraph)
                        title = l
                        if(not(titleDetection)):
                            title = ""
                        paragraph = {
                        'number': number,
                        'title': title,
                        'text': ""
                        }
                    
                    detectTitle = False

                if not(re.search(pattern,l)) and not(detectTitle and titleDetection):
                    paragraph['text'] += l
                    textDetected = True
        
        page['paragraphs'].append(paragraph)
        documentJSON['pages'].append(page)
    
    return documentJSON


def convertToImages(path,outputName):
    pdf = wi(filename=path,resolution=300)
    pdfImage = pdf.convert("jpeg")
    i=1
    for img in pdfImage.sequence:
        page = wi(image=img)
        page.save(filename=outputName+str(i)+".jpg")
        i+=1
    print("Done.")


path = 'resources/sampleContract.pdf'
fileNames = "imgs-"
numberOfPages = 3
resultFile = "document.json"
# CHANGE HERE THE SEGMENTATION STYLE OF YOUR DOCUMENT
segmentationStyle = r"^\d\."
# IF YOUR DOCUMENT HAS TITLES AFTER SEGMENTATION, CHANGE THIS VALUE TO TRUE
titles = False

# CONVERT TO IMAGES
convertToImages(path,fileNames)

# PERFORM OCR
for i in range(1,numberOfPages+1):
    imgpath = fileNames+str(i)+'.jpg'
    data = getOCRFromImage(imgpath)
    text = getStructuredText(data)
    saveToJSON(text,fileNames+str(i)+'.json')


# GET DOCUMENT STRUCTURE
documentJSON = getDocumentStructure(numberOfPages,fileNames,segmentationStyle,titles)
saveToJSON(documentJSON,resultFile)

