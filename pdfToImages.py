try:
    import collections.abc
except ImportError:
    pass
from wand.image import Image as wi

def convertToImages(path,outputName):
    pdf = wi(filename=path,resolution=300)
    pdfImage = pdf.convert("jpeg")
    i=1
    for img in pdfImage.sequence:
        page = wi(image=img)
        page.save(filename=outputName+str(i)+".jpg")
        i+=1
    print("Done.")


# CHANGE PATH NAME HERE
path = 'resources/sampleContract.pdf'
convertToImages(path,"imgs-")