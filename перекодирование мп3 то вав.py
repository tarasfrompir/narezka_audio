#!/usr/bin/env python3

#Подключаем модуль 
import os
import subprocess
import shutil

#Каталог из которого будем брать fayli 
directory = './sound/narezka'

# udalyaem vse predidushie fayli
shutil.rmtree('./sound/wav', ignore_errors=True)
# создаем директорию если она отсутствует
if not os.path.exists('./sound/wav'):
    os.makedirs('./sound/wav')

#Получаем список файлов в переменную files 
files = os.listdir(directory)
# dlyaskritiya processa
CREATE_NO_WINDOW = 0x08000000


name = 0

for file in files:
    name +=1
    subprocess.call(['ffmpeg', '-i', directory+'/'+file, './sound/wav/output'+str(name)+'.wav'], creationflags=CREATE_NO_WINDOW)



