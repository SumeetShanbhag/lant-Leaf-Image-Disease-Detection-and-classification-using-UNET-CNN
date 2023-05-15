# -*- coding: utf-8 -*-
"""DeepLearning_Project_preparingDataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11AUfT9HJHyO1gbrxsZ7AYxyQMkZ2o5Kp
"""

# Commented out IPython magic to ensure Python compatibility.
import os                       # for working with files
import numpy as np              # for numerical computationss
import pandas as pd             # for working with dataframes
import seaborn as sns
import torch                    # Pytorch module 
import matplotlib.pyplot as plt # for plotting informations on graph and images using tensors
import torch.nn as nn           # for creating  neural networks
from torch.utils.data import DataLoader # for dataloaders 
from PIL import Image           # for checking images
import torch.nn.functional as F # for functions for calculating loss
import torchvision.transforms as transforms   # for transforming images into tensors 
from torchvision.utils import make_grid       # for data checking
from torchvision.datasets import ImageFolder  # for working with classes and images
from torchsummary import summary              # for getting the summary of our model
import tensorflow as ts 
from  tensorflow import keras
import itertools
from sklearn.metrics import precision_score, accuracy_score, recall_score, confusion_matrix, ConfusionMatrixDisplay

# input dataset


train_dir = "/content/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train"
valid_dir = "/content/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/valid"
diseases = os.listdir(train_dir)

diseases

# show number of total classes 
print("Number of classes : " ,len(diseases))

# Number of images for each disease
nums_train = {}
nums_val = {}
for disease in diseases:
    nums_train[disease] = len(os.listdir(train_dir + '/' + disease))
    nums_val[disease] = len(os.listdir(valid_dir + '/' + disease))
img_per_class_train = pd.DataFrame(nums_train.values(), index=nums_train.keys(), columns=["no. of images"])
print('Train data distribution :')
img_per_class_train

plt.figure(figsize=(15,15))
plt.title('Train data distribution ',fontsize=30)
plt.xlabel('Number of image',fontsize=20)
plt.ylabel('Planet',fontsize=20)

keys = list(nums_train.keys())
# get values in the same order as keys, and parse percentage values
vals = list(nums_train.values())
sns.barplot(y=keys, x=vals)

# show number of images in train data
number_train = 0
for value in nums_train.values():
    number_train += value
print("The number of images for training : ",number_train)

plants=[]
diseases_unique=[]
for i in diseases:
  if(i.split('__'))[0] not in plants:
    plants.append(i.split('__')[0])
  if(i.split('___'))[1] != 'healthy':
    diseases_unique.append(i.split('___')[1])

# show names and number of plants
# Names
print('Plantes :',plants)
# Number of platns:
print('-'*100)
print('Number of plants : ',len(plants))

# show names and number of unique diseases
# Names
print('diseases :',diseases_unique)
# Number of unique diseases:
print('-'*100)
print('Number of unique diseases : ',len(diseases_unique))

def create_data_frame(path):
    list_plant=[]
    list_category=[]
    list_disease=[]
    list_path=[]
    list_plant_category=[]
    list_image_size=[]
    list_image_type=[]
    list_size=[]
    
    for path,directory,files in os.walk(path,topdown=False):
        for name in files:
            plant_category=category=path.split("/")[-1]
            plant=plant_category.split("___")[0]
            category=plant_category.split("___")[-1]
            disease=0 if category=="healthy" else 1
            full_path=path+"/"+name
            image_type=name.split(".")[1]
            size=os.path.getsize(full_path)
            with Image.open(full_path) as images:
               width,height=images.size
            list_plant.append(plant)
            list_category.append(category)
            list_disease.append(disease)
            list_path.append(full_path)
            list_plant_category.append(plant_category)
            list_image_size.append(str(width)+"x"+str(height))
            list_image_type.append(image_type)
            list_size.append(size)                                  
    data_info=pd.DataFrame.from_dict({"Plant":list_plant,"Category":list_category,"Disease":list_disease,
                           "Path":list_path,"Plant_Category":list_plant_category,"Image_size":list_image_size,"Image_type":list_image_type,"Size":list_size},orient="columns")

    image_count_info=pd.DataFrame(data_info.groupby(["Plant","Category","Plant_Category"]).size())
    image_count_info.rename(columns={0:"nb"},inplace=True)
    image_count_info=image_count_info.reset_index()
    return data_info,image_count_info

train_data_info,train_data_count=create_data_frame(train_dir)
valid_data_info,valid_data_count=create_data_frame(valid_dir)

def  class_data_distribution(class_data_count,class_data_info):
    list_plant_mod= ['Cherry' if x == 'Cherry_(including_sour)' else x for x in list(class_data_count.Plant.unique())]


    pi_chart_color_0 = ['#99ffcc', '#99ffff', '#99ffcc', '#99ffff','#99ffcc', '#99ffff','#99ffcc', '#99ffff','#99ffcc', '#99ffff','#99ffcc', '#99ffff','#99ffcc', '#99ffff',]
    pi_chart_color_1 = ['#ff999a','#ffcb99', '#fffe99','#99ffcc',
  '#99ffff','#ffcb99', '#99ffcc','#ff999a','#ffcb99','#fffe99','#99ffff', '#ff999a','#ffcb99','#fffe99','#99ffcc',
  '#99ffff','#fffe99','#99ffcc','#fffe99','#99ffff','#ffcb99','#fffe99','#99ffcc','#99ffff','#99ffcc','#99ffff','#fffe99','#99ffcc',
  '#ff999a','#ff9990','#ffb299','#ffc5b3','#ffece6','#ffedb3','#fff3cd','#d1ffcd','#cdffdf','#99ffff']
 

    plt.pie(class_data_count.nb, labels=class_data_count.Category,  startangle=90,frame=True,radius=1,rotatelabels=True,colors=pi_chart_color_1,wedgeprops=dict(width=0.9, edgecolor='w'),autopct='%1.f%%',pctdistance=0.90, textprops={'fontsize': 12})
    plt.pie(class_data_info.groupby(['Plant']).size(),labels=list_plant_mod,radius=0.75,startangle=90,labeldistance=0.3,rotatelabels=True,colors=pi_chart_color_0,wedgeprops=dict(width=0.9, edgecolor='w'),autopct='%1.f%%',pctdistance=0.90, textprops={'fontsize': 10})
    centre_circle = plt.Circle((0,0),0.5,color='black', fc='white',linewidth=0)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
 
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

plt.figure(figsize=(12,12))
class_data_distribution(train_data_count,train_data_info)

img_per_class_val = pd.DataFrame(nums_val.values(), index=nums_val.keys(), columns=["no. of images"])
print('Validation data distribution :')
img_per_class_val

plt.figure(figsize=(15,15))
plt.title('Validation data distribution ',fontsize=30)
plt.xlabel('Number of image',fontsize=20)
plt.ylabel('Planet',fontsize=20)

keys = list(nums_val.keys())
# get values in the same order as keys, and parse percentage values
vals = list(nums_val.values())
sns.barplot(y=keys, x=vals)

train_data =keras.utils.image_dataset_from_directory(train_dir ,
                                         image_size=(256, 256))
valid_data = keras.utils.image_dataset_from_directory(valid_dir,
                                        image_size=(256, 256))

# Function to display images in a grid with class names
def show_images(images, class_names, n_images_per_row=5):
    fig, axs = plt.subplots(nrows=int(np.ceil(len(images) / n_images_per_row)), ncols=n_images_per_row, figsize=(15, 30))
    axs = axs.flatten()
    for img, class_name, ax in zip(images, class_names, axs):
        ax.imshow(img)
        ax.set_title(class_name)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

# Load one image from each class
images = []
for disease in diseases:
    class_dir = os.path.join(train_dir, disease)
    img_name = os.listdir(class_dir)[0]  # Select the first image in the folder
    img_path = os.path.join(class_dir, img_name)
    img = Image.open(img_path)
    images.append(img)

# Display images in a grid with class names
show_images(images, diseases)
#print(np.shape(images[1]))

import cv2

def binary_segmentation(image, threshold=128, blur_kernel_size=(5, 5)):
    # Convert to LAB color space
    lab_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2LAB)
    
    # Apply Gaussian blur
    blurred_lab_image = cv2.GaussianBlur(lab_image, blur_kernel_size, 0)
    
    # Threshold on the B channel
    _, binary_b = cv2.threshold(blurred_lab_image[:, :, 2], threshold, 255, cv2.THRESH_BINARY)

    return Image.fromarray(binary_b)

images = []
for disease in diseases:
    disease_dir = os.path.join(train_dir, disease)
    image_path = os.path.join(disease_dir, os.listdir(disease_dir)[0])
    image = Image.open(image_path)
    images.append(image)

segmented_images = [binary_segmentation(image) for image in images]

fig, axes = plt.subplots(len(diseases), 2, figsize=(10, len(diseases) * 2))
for i, (original, segmented) in enumerate(zip(images, segmented_images)):
    axes[i, 0].imshow(original)
    axes[i, 0].axis('off')
    axes[i, 0].set_title(f'Original: {diseases[i]}')
    
    axes[i, 1].imshow(segmented, cmap='gray')
    axes[i, 1].axis('off')
    axes[i, 1].set_title(f'Segmented: {diseases[i]}')

plt.tight_layout()
plt.show()

from PIL import Image

!pip install --upgrade tensorflow

# Define the FCN model
def create_fcn(input_shape):
    model = ts.keras.models.Sequential([
        ts.keras.layers.Conv2D(64, 3, activation='relu', padding='same', input_shape=input_shape),
        ts.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
        ts.keras.layers.MaxPooling2D(),
        ts.keras.layers.Conv2D(128, 3, activation='relu', padding='same'),
        ts.keras.layers.Conv2D(128, 3, activation='relu', padding='same'),
        ts.keras.layers.MaxPooling2D(),
        ts.keras.layers.Conv2D(256, 3, activation='relu', padding='same'),
        ts.keras.layers.Conv2D(256, 3, activation='relu', padding='same'),
        ts.keras.layers.Conv2D(256, 3, activation='relu', padding='same'),
        ts.keras.layers.MaxPooling2D(),
        ts.keras.layers.Conv2D(512, 3, activation='relu', padding='same'),
        ts.keras.layers.Conv2D(512, 3, activation='relu', padding='same'),
        ts.keras.layers.Conv2D(512, 3, activation='relu', padding='same'),
        ts.keras.layers.MaxPooling2D(),
        ts.keras.layers.Conv2D(512, 3, activation='relu', padding='same'),
        ts.keras.layers.Conv2D(512, 3, activation='relu', padding='same'),
        ts.keras.layers.Conv2D(512, 3, activation='relu', padding='same'),
        ts.keras.layers.MaxPooling2D(),
        ts.keras.layers.Conv2D(4096, 7, activation='relu', padding='same'),
        ts.keras.layers.Dropout(0.5),
        ts.keras.layers.Conv2D(4096, 1, activation='relu', padding='same'),
        ts.keras.layers.Dropout(0.5),
        ts.keras.layers.Conv2D(1, 1, activation='sigmoid')
    ])
    return model

# Define the binary segmentation function using the FCN model
def binary_segmentation(image, model):
    # Convert the image to numpy array and resize to input shape
    np_image = np.array(image.resize((256, 256)))
    
    # Predict the segmentation mask using the FCN model
    mask = model.predict(np_image.reshape(1, 256, 256, 3))
    print(mask.shape)
    mask = mask.reshape(8, 8)
    
    # Threshold the mask to get binary segmentation
    binary_mask = (mask > 0.5).astype(np.uint8) * 255
    
    return Image.fromarray(binary_mask)

model = create_fcn((256, 256, 3))

# Segment the images using the FCN model
images = []
for disease in diseases:
    disease_dir = os.path.join(train_dir, disease)
    image_path = os.path.join(disease_dir, os.listdir(disease_dir)[0])
    image = Image.open(image_path)
    images.append(image)

segmented_images = [binary_segmentation(image, model) for image in images]

# Display the original and segmented

fig, axes = plt.subplots(len(diseases), 2, figsize=(10, len(diseases) * 2))
for i, (original, segmented) in enumerate(zip(images, segmented_images)):
    axes[i, 0].imshow(original)
    axes[i, 0].axis('off')
    axes[i, 0].set_title(f'Original: {diseases[i]}')
    
    axes[i, 1].imshow(segmented, cmap='gray')
    axes[i, 1].axis('off')
    axes[i, 1].set_title(f'Segmented: {diseases[i]}')

plt.tight_layout()
plt.show()