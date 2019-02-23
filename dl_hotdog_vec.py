# -*- coding: utf-8 -*-
"""DL_HotDog_vec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nyu0Du2dRIUhraiHEv_CWvVBKoufEixx
"""

!pip install fastai

# %reload_ext autoreload
# %autoreload 2
# %matplotlib inline

from fastai import *
from fastai.vision import *
from os import rmdir
from shutil import rmtree
from PIL import Image
from os import remove

#Definimos nombres de la carpetas donde estará nuestras imagenes.
folders = ['hotdog','hamburguesa','pizza','sanduche']
files = ['hotdog.txt','hamburguesa.txt','pizza.txt','sanduche.txt']

#Vamos a proceder a crear la ruta donde queremos que se almacene las imagenes.
path = Path('data')
dest = ''
existe =false

#Se descarga de forma automatizada las imagenes
#Arriba se crea una lista con nuestras categorias a descargar
for folder in folders:
  dest = path/folder
  print(dest)
  existe = os.path.isfile(dest)
  if existe :
    rmtree(dest)
  dest.mkdir(parents=True, exist_ok=True)
  for file in files:
    print(file)
    if file[:-4] == folder:
      download_images(path/file, dest, max_pics=200)

classes = ['hotdog','hamburguesa','pizza','sanduche']

path

#Se pretende eliminar toda imagen que da error para no incluirlo
# en el databunch de entrenamiento.
for folder in folders:
  directorio = path/folder
  for dirName, subdirList, fileList in os.walk(directorio):
      print('Directorio encontrado: %s' % dirName)
      for fname in fileList:
          print('\t%s' % fname)
          try:
            Image.open(directorio/fname)
          except OSError as err:
            print("OS error: {0}".format(err))
            remove(directorio/fname)

np.random.seed(42)
data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,
        ds_tfms=get_transforms(), size=224, num_workers=4).normalize(imagenet_stats)

data.classes

data.show_batch(rows=3, figsize=(7,8))

data.classes, data.c, len(data.train_ds), len(data.valid_ds)

learn = create_cnn(data, models.resnet34, metrics=error_rate)

learn.fit_one_cycle(4)

learn.save('stage-1')

learn.unfreeze()

learn.lr_find()

learn.recorder.plot()

learn.fit_one_cycle(2, max_lr=slice(3e-5,3e-4))

learn.save('stage-2')

learn.load('stage-2');

interp = ClassificationInterpretation.from_learner(learn)

interp.plot_confusion_matrix()

data.classes

#Se crea directorio para imagenes de validacion
destV = path/"validation"
print(destV)
destV.mkdir(parents=True, exist_ok=True)

img = open_image(destV/'hotdog1.jpg')
img

learn.export()

learn = load_learner(path)

pred_class,pred_idx,outputs = learn.predict(img)
print('La categoria es:')
pred_class

img = open_image(destV/'pizza1.jpg')
img

pred_class,pred_idx,outputs = learn.predict(img)
print('La categoria es:')
pred_class

img = open_image(destV/'colombiana.jpg')
img

pred_class,pred_idx,outputs = learn.predict(img)
print('La categoria es:')
pred_class

img = open_image(destV/'burgerking.jpg')
img

pred_class,pred_idx,outputs = learn.predict(img)
print('La categoria es:')
pred_class

#SIIIUUUUUUUUUUUUUUUUUUUUU :)

img = open_image(destV/'gyehotdog.jpg')
img

pred_class,pred_idx,outputs = learn.predict(img)
print('La categoria es:')
pred_class

