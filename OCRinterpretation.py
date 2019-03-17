import json
import re

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


numberOfPages = 3
jsonFileName = "imgs-"
filename = "document.json"

# CHANGE HERE THE SEGMENTATION STYLE OF YOUR DOCUMENT
segmentationStyle = r"^\d\."
# IF YOUR DOCUMENT HAS TITLES AFTER SEGMENTATION, CHANGE THIS VALUE TO TRUE
titles = False

documentJSON = getDocumentStructure(numberOfPages,jsonFileName,segmentationStyle,titles)
saveToJSON(documentJSON,filename)