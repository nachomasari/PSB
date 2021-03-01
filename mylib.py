import cv2
import os
import csv
import numpy as np
from google.colab import drive
import math

def load_images_from_folder(folder,h,w):
    images = []
    names = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(cv2.resize(img,(h,w)))
            #images.append(img)
            pos = filename.find(".")
            names.append(int(filename[:pos]))
    return [names,images]
	
def mount_data(folder,h,w):
  drive.mount('/content/drive')

  folder2 = folder + '/Concat_img'
  images = load_images_from_folder(folder2,h,w)
  pot = []
  fw = []
  age = []	
  with open(folder + "/harvest.txt") as tsv:
      for line in csv.reader(tsv, delimiter="\t"):
          if line[0] =='pot':
              continue
          pot.append(int(line[0]))
          fw.append(float(str.replace(line[2],',','.')))
	  age.append(int(line[14]))

  FW = []
  AGE = []
	
  data = [images[1],AGE,FW]

  for p in images[0]:
      if p in pot:
          FW.append(fw[pot.index(p)])
	  AGE.append(age[pot.index(p)])
  return data  

def Divide_in_classes(Y_orig,Y_orig2, interval):

  classes = math.ceil(max([max(Y_orig),max(Y_orig2)])/interval)
  n = Y_orig.shape[0]
  Y_cl = np.zeros([n,classes])
  for y in range(n):
    Y_cl[y,math.floor(Y_orig[y] / interval)] = 1

  n = Y_orig2.shape[0]
  Y_cl2 = np.zeros([n,classes])
  for y in range(n):
    Y_cl2[y,math.floor(Y_orig2[y] / interval)] = 1

  return Y_cl,Y_cl2,classes
  
