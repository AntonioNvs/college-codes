import os
import csv
import math
import time
import numpy as np
import pandas as pd
import concurrent, multiprocessing
import skimage.io as io
import matplotlib.pyplot as plt

from PIL import Image
from skimage import data

def read_image(image_path):
    image = Image.open(image_path).convert("L")

    if image.size[0] % 8 != 0 or image.size[1] % 8 != 0:
        new_w = image.size[1] - image.size[1] % 8
        new_h =image.size[0] - image.size[0] % 8
        image = image.resize((new_h,new_w))

    image = np.array(image).astype(np.uint8)

    return image


def divide_image(image):
    size_part = math.ceil(image.shape[1] / 6)

    return [image[:,i:i+size_part] for i in range(0, image.shape[1], size_part)]


def apply_filter(image, kernel):
    m, n = image.shape
    km, kn = kernel.shape
    result = np.zeros((m-km+1, n-kn+1))
    for i in range(m-km+1):
        for j in range(n-kn+1):
            result[i, j] = np.sum(image[i:i+km, j:j+kn] * kernel)
    return result

def cart_to_polar(dx,dy):
  m,n = dx.shape
  mag = np.zeros((m, n))
  angle = np.zeros((m, n))

  for i in range(m):
    for j in range(n):
      mag[i,j] = math.sqrt(dx[i,j]**2+dy[i,j]**2)
      angle[i,j] = math.degrees(math.atan2(dy[i,j],dx[i,j]))
      if angle[i,j] < 0:
        angle[i,j] = 180 + angle[i,j]
      if angle[i,j] == 180:
        angle[i,j] = 0

  return mag,angle

def derivate_image(image):
    # Defina o kernel para derivada em relação às linhas (vetor coluna)
    row_kernel = np.array([[-1], [0], [1]])

    # Defina o kernel para derivada em relação às colunas (vetor linha)
    col_kernel = np.array([[-1, 0, 1]])

    # Aplique a convolução para calcular as derivadas
    m,n = image.shape
    dx = np.zeros((m, n))
    dy = np.zeros((m, n))

    dx[:,1:n-1] = apply_filter(image, col_kernel)
    dy[1:m-1,:] = apply_filter(image, row_kernel)

    return cart_to_polar(dx, dy)

def lala(mag,ang):
  m,n = mag.shape
  hist = np.zeros(9)
  for i in range(m):
    for j in range(n):
      idx_1 = int(ang[i,j] / 20)
      idx_2 = (math.ceil(ang[i,j] / 20)) % 9
      if idx_1 == idx_2:
        hist[idx_1] += mag[i,j]
      else:
        hist[idx_1] += mag[i,j]*(1 - ((ang[i,j] - idx_1*20)/20))
        hist[idx_2] += mag[i,j]*((ang[i,j] - idx_1*20)/20)
  return hist.tolist()

def hist_of_gradient(mag,ang):
  m,n = mag.shape
  lista = []
  for i in range(0,m, 8):
    for j in range(0,n,8):
      lista += lala(mag[i:i+8,j:j+8],ang[i:i+8,j:j+8])
  return lista


def execute(filenames):
    for filename in filenames:
      print(f"{len(dataset)} de {len(files)*6}")
      img = read_image(f"CAPTCHA-10k/treinamento/{filename}")
      
      parts = divide_image(img)

      label = filename.replace(".jpg", "")
      captcha = labels[label]

      for i, part in enumerate(parts):
          mag, ang = derivate_image(part)

          dataset.append([captcha[i]] + hist_of_gradient(mag, ang))

      os.system("cls")

if __name__ == "__main__": 
  labels = {}
  with open("labels.csv", "r") as src:
    for line in src.read().split("\n"):
      if len(line) < 1: continue 
      key, value = line.split(",")

      labels[key] = value.strip()

  dataset = []

  files = list(os.listdir("CAPTCHA-10k/treinamento"))[:20]

  workers = multiprocessing.cpu_count()
  print(f"Número de cores: {workers}")
  time.sleep(1)

  args = np.array_split(files, workers)
  
  time.sleep(10)

  with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
      futures = [executor.submit(execute, arg) for arg in args]

      concurrent.futures.wait(futures)
  
  df = pd.DataFrame(dataset)
  df.to_csv("data.csv")


