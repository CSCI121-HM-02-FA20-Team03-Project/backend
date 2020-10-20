import cv2 
class Preprocess:
    def invertImageColor(originalImage):
        grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)    
        blackAndWhiteImage = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY_INV)

        return blackAndWhiteImage

    def resizeImage(image):
        scale_percent = image.shape[0]/100 # percent of original size

        width = int(image.shape[1] * (1/scale_percent))
        height = int(image.shape[0] * (1/scale_percent))
        
        # dsize
        dsize = (width, height)

        # resize image
        output = cv2.resize(image, dsize)

        return output

# if __name__ == '__main__':
#     originalImage = cv2.imread('image_here.png', cv2.IMREAD_UNCHANGED)
   
#     resizedImage = resizeImage(originalImage)
#     convertedImage = invertImageColor(resizedImage)
