import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
import os
import cv2
import shutil
import tensorflow as tf
from tensorflow import keras
from Inception import InceptionUnit
from ResNet import ResidualUnit
from Xception import XceptionUnit
from model import ResNet, GoogleNet, Xception
import multiprocessing as mp
# from model import get_model
try:
    os.mkdir("./Notices")
except FileExistsError:
    pass

try:
    os.mkdir("./notNotices")
except FileExistsError:
    pass

def resize(img):
    old_image_width, old_image_height, channels = img.shape
    color = (0,0,0)
    if old_image_width>old_image_height:
        result= np.full((old_image_width,old_image_width, channels), color, dtype=np.uint8)
        yc = (old_image_width-old_image_height)//2
        #temp=result[:, yc:yc+old_image_height,:]
        #print("a",temp.shape)
        result[:, yc:yc+old_image_height,:] = img 
        #return result
    elif old_image_width<old_image_height:
        result= np.full((old_image_height,old_image_height, channels), color, dtype=np.uint8)
        xc = (old_image_height-old_image_width)//2
        #temp= result[xc:xc+old_image_width,:,:]
        #print("b",temp.shape)
        result[xc:xc+old_image_width,:,:] = img 
        #return result
    else:
        result=img
    a=cv2.resize(result,(224,224))
    return a


def applyCNN():
    dirList = os.listdir("./subimage/")
    for dirn in dirList:
        fileList = os.listdir("./subimage/"+dirn+"/")
        imgList = []
        finalImage = []
        for file in fileList:
            # img = tf.keras.utils.load_img(f"./subimage/{dir}/{file}", grayscale=False, color_mode="grayscale")
            img = cv2.imread(f"./subimage/{dirn}/{file}")
            temp=img.copy()
            img = resize(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = np.array(img, dtype=np.float32)
            img = img.reshape(224, 224, 1)
            img = img / 255.0
            imgList.append(img)
            finalImage.append(file)
        imgList = np.array(imgList)
        print("Image shape: ", imgList.shape)

        model = Xception()
        model = keras.models.load_model('./source/models/model_xception_1.h5', custom_objects={'XceptionUnit': XceptionUnit})
        pred = model.predict(imgList,workers=mp.cpu_count(), use_multiprocessing=True)
        # pred = model.predict(imgList)
        print("Pred shape: ", pred.shape)

        for i in range(len(pred)):
            if pred[i][0] < pred[i][1] or abs(pred[i][0] - pred[i][1]) < 0.1:
                print("Notice is for Tender")
                print(f"{dirn}/{finalImage[i]}")
                # cv2.imwrite("./Tender/"+finalImage[i],temp)
                try: 
                    os.mkdir(path=f"./Notices/{dirn}")
                except FileExistsError:
                    pass
                shutil.copy(f"./subimage/{dirn}/{finalImage[i]}", f"./Notices/{dirn}/{finalImage[i]}")
            else:
                print("Notice is not tender")
                print(f"{dirn}/{finalImage[i]}")
                try: 
                    os.mkdir(path=f"./notNotices/{dirn}")
                except FileExistsError:
                    pass
                shutil.copy(f"./subimage/{dirn}/{finalImage[i]}", f"./notNotices/{dirn}/{finalImage[i]}")

        # if pred[0][0] < pred[0][1]:
        #     # filename = str(output_path.joinpath(page.split(".")[0] + "_" + str(count) + '.png'))
        #     try: 
        #         os.mkdir(path=f"./Notices/{dirn}")
        #     except FileExistsError:
        #         pass
        #     filename="./Notices/"+dirn+"/"+file
        #     cv2.imwrite(filename, temp)
        #     # print(dirn)
        #     print(f"{file} is Notice")
        # else:
        #     # print(dirn)
        #     try: 
        #         os.mkdir(path=f"./notNotices/{dirn}")
        #     except FileExistsError:
        #         pass
        #     filename="./notNotices/"+dirn+"/"+file
        #     cv2.imwrite(filename, temp)
        #     print(f"{file} is not Notice")
      




def applyCNN1():
    dirList = os.listdir("./subimage/")
    for dir in dirList:
        fileList = os.listdir("./subimage/"+dir+"/")
        for file in fileList:
            img = tf.keras.utils.load_img(f"./subimage/{dir}/{file}", grayscale=False, color_mode="grayscale")
            
            img = np.array(img, dtype=np.float32)
            temp=img.copy()
            img=cv2.resize(img, (224,224))
            img = img.reshape(1, 224, 224, 1)
            img = img / 255.0
            # print(img.shape)
            model = Xception()
            model = keras.models.load_model('./source/models/model_xception_1.h5', custom_objects={'XceptionUnit': XceptionUnit})
            pred = model.predict(img)
            # print(pred)
            if pred[0][0] < pred[0][1]:
                print("Notice is for Tender")
                print(f"{dir}/{file}")
                cv2.imwrite("./Tender/"+file,temp)
            else:
                print("Notice is not tender")
                print(f"{dir}/{file}")
                cv2.imwrite("./notTender/"+file, temp)

if __name__ == '__main__':
    applyCNN()
