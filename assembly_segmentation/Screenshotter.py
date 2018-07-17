import cv2
import numpy
from PIL import Image, ImageDraw

def cropper(nodes):

    # read image as RGB and add alpha (transparency)
    im = Image.open("crop.png").convert("RGBA")

    # convert to numpy (for convenience)
    imArray = numpy.asarray(im)

    # create mask
    polygon = nodes
    print(nodes)
    maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
    ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
    mask = numpy.array(maskIm)

    # assemble new image (uint8: 0-255)
    newImArray = numpy.empty(imArray.shape,dtype='uint8')

    # colors (three first columns, RGB)
    newImArray[:,:,:3] = imArray[:,:,:3]

    # transparency (4th column)
    newImArray[:,:,3] = mask*255

    # back to Image from numpy
    newIm = Image.fromarray(newImArray, "RGBA")
    newIm.save("out.png")

def run():
    
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Photo Capture",  cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Photo Capture", 1500, 700)
    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("Photo Capture", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        #if k%256 == 27:
            # ESC pressed
            # print("Closing...")
            # break
        if k%256 == 32:
            # SPACE pressed
            img_name = ("crop.png")
            cv2.imwrite(img_name, frame)
            #print("{} written!".format(img_name))
            break

    cam.release()

    cv2.destroyAllWindows()

    #cropper()