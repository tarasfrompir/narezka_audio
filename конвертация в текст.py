#!/usr/bin/env python3

from os import path
import shutil # Подключаем модуль

# recognize speech using Wit.ai
WIT_AI_KEY = "FGDIOCBONK7QLHMPQHQLOUNS37V6BLMK"  # Wit.ai keys are 32-character uppercase alphan

#Подключаем модуль 
import os 

import speech_recognition as sr

#Каталог из которого будем брать изображения 
directory = './sound/wav'

#Получаем список файлов в переменную files 
files = os.listdir(directory)




# Sort file names with path
file_list = os.listdir(directory)
full_list = [os.path.join(directory, i) for i in file_list]
files = sorted(full_list, key = os.path.getmtime)


# rabota c papkoy wav v svoy golos
# udalyaem vse predidushie fayli в своем голосе для избежания проблем
shutil.rmtree('./myvoice/wav', ignore_errors=True)

# создаем директорию если она отсутствует
if not os.path.exists('./myvoice/wav'):
    os.makedirs('./myvoice/wav')
    
# rabota c papkoy etc v svoy golos
# udalyaem vse predidushie fayli в своем голосе для избежания проблем
shutil.rmtree('./myvoice/etc', ignore_errors=True)
# создаем директорию если она отсутствует
if not os.path.exists('./myvoice/etc'):
    os.makedirs('./myvoice/etc')
# kuda pishem raspoznaniy text
arctictxt = open('./myvoice/etc/txt.done.data', 'w')



# читаем текст книги
book = open('./textoffbook/book.txt', 'r')
textbook = book.read()

# nomer vihodnogo fayla
outnomer = 0

# поиск строки в тексте книги
def distance_2(text, pattern):
   "Calculates the Levenshtein distance between text and pattern."
   text_len, pattern_len = len(text), len(pattern)
   if text_len > 500:
        text_len = 500

   current_column = range(pattern_len+1)
   min_value = pattern_len
   end_pos = 0
   for i in range(1, text_len+1):
      previous_column, current_column = current_column, [0]*(pattern_len+1) # !!!
      for j in range(1,pattern_len+1):
         add, delete, change = previous_column[j]+1, current_column[j-1]+1, previous_column[j-1]
         if pattern[j-1] != text[i-1]:
            change += 1
         current_column[j] = min(add, delete, change)

      if min_value > current_column[pattern_len]: # !!!
         min_value = current_column[pattern_len]
         end_pos = i

   return min_value, end_pos

def distance_3(text, pattern):
   min_value, end_pos = distance_2(text, pattern)
   min_value, start_pos = distance_2(text[end_pos-1::-1], pattern[::-1])
   start_pos = end_pos - start_pos
   return min_value, start_pos, end_pos, text[start_pos:end_pos], pattern

# konec funkciy


# telo cikla
for file in files:
    # obtain path to "english.wav" in the same folder as this script
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), file)
    print (file)
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file


    try:
       # poluchaem otvet
        textout=""
        answerwit = r.recognize_google(audio, language="uk-UA")
        # poluchaem distanciyu levenshtayna
        mv, stpos, endpos, text, pattern= distance_3(u''+textbook, u''+answerwit) 
        # sohranenie tekcta i fayla
        start = (textbook.rfind(" ", 0, stpos))+1
        end = (textbook.find(" ", endpos))
        textout= textbook[start:end]
        print (answerwit)
        print (textout)
        # obrezaem knigu
        # cshivaem text
        # esli start s bolyshoy bukvy
        if textout[0:1].istitle():
            # esli konec na tochku to pishem text i fayl
            if textout[len(textout)-1:len(textout)]=="." or textout[len(textout)-1:len(textout)]=="?" or textout[len(textout)-1:len(textout)]=="!":
                # копирование файлов
                shutil.copy(r''+file, r''+'./myvoice/wav/arctic_'+str(outnomer)+'.wav')
                arctictxt.write('( arctic_'+str(outnomer)+' "'+textout+'" )'+ '\n')
                print ('( arctic_'+str(outnomer)+' "'+textout+'" )'+ '\n')
                textbook = textbook[end:len(textbook)]
                outnomer += 1
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
        answerwit = ""
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))
        answerwit =""

                

# zakrivaem fail    
arctictxt.close()
