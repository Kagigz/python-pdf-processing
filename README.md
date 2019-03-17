# Python PDF Processing

*-- Work in progress --* 


This repo contains 4 files:
1. **pdfToImages.py**: converts PDF files to images
2. **imagesOCR.py**: performs OCR on a set of images with the [Azure Computer Vision API](https://azure.microsoft.com/en-en/services/cognitive-services/computer-vision/#text), then stores the results in json files
3. **OCRinterpretation.py**: interprets the results from the json files and generates new json files with the pdf's structure
4. **pdfProcessing.py**: takes care of the whole pipeline described above

## Installations

- Install [GhostScript](https://www.ghostscript.com/download/gsdnld.html) on Windows
- Install [ImageMagick](https://imagemagick.org/script/download.php#windows) on Windows
- Install Wand: `pip install wand`

## How to use

Clone or download this repo, then use either the sample files or your own. If you chose to use your own, change the path names accordingly.
/!\ If you use your own files, try first with a small number of pages. Converting pdf to images takes a while.

If you wish to use the OCR capabilities, [set up a Computer Vision API service on Azure](https://ms.portal.azure.com/?l=en.en-us#create/Microsoft.CognitiveServicesComputerVision) and fill in your subscription key and region in *imagesOCR.py* and/or *pdfProcessing.py*. 

Once everything is ready, execute the files and watch the magic happen: 
`python .\filename.py`
