#link-https://www.youtube.com/watch?v=AkY2TpvDGUo
#the project is based on image processing
import cv2
import numpy as np
import time #preinstalled -to provide camera some time ,for camera setup before code executed
print("before")
cap=cv2.VideoCapture(0) #video capture object called from cv2 library
# to indicate which camera should be used this object is used
print("after")
time.sleep(2)#initial camera output is dark so 2 seconds provided so that camera setup is done 

background=0# variable to store the background which will be displayed when we have the cloak in front of it

for i in range(30):# now capturing of background
    ret,background=cap.read()# 30 iterations to capture the background by videoCapture object
    # 30 frames because we want to have the best and clear image of the background
    # if ret is false that means camera is not opening and we need to forcefully open using isOpen()

while(cap.isOpened()):# till captured object is opened and running this while loop will run
    ret,img=cap.read()# we will do image processing on these frames
    if not ret:# when we close the sindow for capture ret returns false
        break;# i will break this loop
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #converting the color space of the captured image from RGB to HSV
    #RGB is linear color space of R,G and B matrix
    #HSV-Hue Saturation Value,also k/a HSB where B-Brightness
    #We are using HSV over RGB because in RGB all the three values R,G and B depend on Color and Brightness of color
    #In HSV only Hue depends on color rest 2 saturation and value are independent of color
    # in HSV hue is the colors on the disc shaped and depending on angle on that circle we have different color choices
    #in open cv there are 8 bits to store color therefr 2^8 colors but we need 360 degree angles to get differnt colors-problem with open cv
    #so in opencv to counter this the disk size is halved and and there is increase in variation with each and every angle
    lower_red=np.array([0,120,70])#hsv values angle for red is 0 to 30 degree but we took 0 to 10 because 10 to 30 contains very lighter shade of red and this could categorise my skin as red as well and hamper
    upper_red=np.array([10,255,255])#first is hue second is saturation and third is value
    #saturation is darkness of the color-below 120 it would go for pink color
    #value or brightness- below 70 brightnss would be very low
    #255 is max value of saturation and brightness since 8 bits
    mask1=cv2.inRange(hsv,lower_red,upper_red)#this would check the hsv frame and segregating/separating the cloak part of the frame and check if there is an object with color in this range
    lower_red=np.array([170,120,70])# red color is in 2 regions of disk 0 to 30 and then 170 to 180
    upper_red=np.array([180,255,255])
    mask2=cv2.inRange(hsv,lower_red,upper_red)

    mask1=mask1+mask2 # overloading the + operator here for 'OR' function-bitwise or
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2)#noise removal
    #morphology functions -they are used for morphological transformations basically
    #morph functions are used for noise removal(check opencv doc for more details)
    #MORPH_OPEN is the morph function we used and 3rd argument is kernel-matrix of 3 by 3 dimensions with all ones in it
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8),iterations=1)
    #MORPH_DILATE to increase the smoothness of the image

    mask2=cv2.bitwise_not(mask1)#except the cloak rest of the background will be in mask2
    res1=cv2.bitwise_and(background,background,mask=mask1)#used for segmentation of the color
    #and between background and mask1 (differentiating between cloak color and background)
    res2=cv2.bitwise_and(img,img,mask=mask2)#used to substitute the cloak part
    #background is img to be displayed when we have cloak over our body and img is image to be displayed when we have no cloak i.e to substitute the cloak part
    final_output=cv2.addWeighted(res1,1,res2,1,0)# superimposed result of the above two
    #the equation use for superimpose alpha(=1) *res1 +beta(=1)*res2+gamma(=0)
    #i.e. linear addition of two images
    cv2.imshow('Swapnil magic cloak',final_output)
    k=cv2.waitKey(10)
    if k==27:#escape key
        break;

cap.release()
cv2.destroyAllWindows()
















