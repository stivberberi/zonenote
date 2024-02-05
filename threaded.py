from threading import Thread
from queue import Queue, Empty
import time

import speech_recognition as sr
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pynput.keyboard import Key, Listener
from pynput import mouse
from Recording_class import conversion_file
from pydub import AudioSegment
import easygui as g
import time
import datetime
import threading
import os

def create_folder(directory_name):
  directory = "./{}/".format(directory_name)
  try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
          directory=directory+"_copy"
          os.makedirs(directory)
          
  except OSError:
        print ('there is an error in creating directory. ' +  directory)
  return directory

#start a recording
def record():
    fs=44100
    duration = 10  # seconds, only only recorded 5 seconds?
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    print("Recording Start")

    sd.default.samplerate = fs
    sd.default.channels = 2

    myrecording = sd.rec(duration * fs, dtype='int16')
    'need to wait for the recording to finish'
    time.sleep(9)
    print("One Second Left")
    time.sleep(1)
    print("Recording End")
    return myrecording

#save a Numpy file
def store_numpy_1(myrecording):##sth wrong here?
    file_name = "Temporary1.npy"
    np.save(file_name, myrecording)
    return file_name

def store_numpy_2(myrecording): 
    file_name = "Temporary2.npy"
    np.save(file_name, myrecording)
    return file_name

#access a saved Numpy file
def access_numpy_1():
  #if A == True:
  Numpy_file = np.load("Temporary1.npy")
  return Numpy_file

def access_numpy_2():
  #if A == False:
  Numpy_file = np.load("Temporary2.npy")
  return Numpy_file

#convert the Numpy file into a wav file'
def convert(A_numpy_file,wav_file_name,object_name):
  currentDT = datetime.datetime.now()
  file_name_2 = "_%s.%s.%s" % (currentDT.minute, currentDT.second, str(currentDT.microsecond)[:2])
  file_name_2 = wav_file_name+ file_name_2 + ".wav"
  write(file_name_2, 44100, A_numpy_file)
  object_name.append_wav_file_list(file_name_2)
  print("Analyzing speech...")
  return file_name_2

#use text to speech to convert the wav file to text'
def text_to_speech(wav_file_name,text_file_name,object_name):
  r = sr.Recognizer()
  record= sr.AudioFile(wav_file_name)
  try:
    with record as source:
      r.adjust_for_ambient_noise(source)
      audio = r.record(source)  
    text=r.recognize_google(audio)
    print("You said : {}".format(text))
    object_name.append_text(text)
    
    #write the text into the file
    
  except:
    text="[There is a period where the speech is unrecognizable, please refer back to the audio file]"
    object_name.append_text(text)
    print("Sorry, could not recognize what you said, but the audio is saved and you could listen to it.")

def combination_initial(text_file_name,A,object_name):
    if A == True:
      numpy_file_one=access_numpy_2()
      file_name_2 = convert(numpy_file_one,text_file_name,object_name)
      numpy_file_two=access_numpy_1()
      file_name_1 = convert(numpy_file_two,text_file_name,object_name)
    else:
      numpy_file_one=access_numpy_1()
      file_name_1 = convert(numpy_file_one,text_file_name,object_name)
      numpy_file_two=access_numpy_2()
      file_name_2 = convert(numpy_file_two,text_file_name,object_name)
    text_to_speech(file_name_1,text_file_name,object_name)
    text_to_speech(file_name_2,text_file_name,object_name)
      
def combination_general(A,text_file_name,object_name):
    if A == True:
      numpy_file_name=access_numpy_1()
    else:
      numpy_file_name=access_numpy_2()
    file_name_3 = convert(numpy_file_name,text_file_name,object_name)
    text_to_speech(file_name_3,text_file_name,object_name)
      
def create_conversion_class (text_file_name):#3
    new_object= conversion_file(text_file_name)
    return new_object

def combine_waves(name_list,Times_zone_out): 
    segment_list = []
    print(segment_list)
    combined_sounds = AudioSegment.from_wav(name_list[0])  
    print(len(name_list))
    segment_list.append(combined_sounds)
    for i in range(1, len(name_list)):
        segment_list.append(AudioSegment.from_wav(name_list[i])) 
    print("length of segment_list",len(segment_list))
    print("length of name_list",len(name_list))
    for x in range(1, len(segment_list)): 
        combined_sounds += segment_list[x]  
        combined_sounds.export("zoneout"+str(Times_zone_out)+".wav", format = "wav")

def delete_wav_files(name_list):
    for i in name_list:
        os.remove(i)
  
class Timer:
    def __init__(self):
        self.timer = time.time()
    def reset(self):
        self.timer = time.time()
    def get_time(self):
        return time.time() - self.timer

timer1 = Timer()

def on_press(key):
    timer1.reset()
    if key == Key.esc:
       # Stop listener
        return False

def on_move(x, y):
    timer1.reset()

def timetest():
    if (timer1.get_time()) > 10:
        print("It has been over 10 seconds.")
        timer1.reset()
        return False
    else:
        return True

class Recorder(Thread):
    def __init__(self, queue):
        self.queue = queue
        super().__init__()
        
    def run(self):
        cmd = self.queue.get()
        if cmd == "TEXT":
            file = open("subject_name.txt", "r")
            subject = file.read()
            file.close()
            os.remove("subject_name.txt")
            Date = datetime.datetime.now()
            folder_name = "_%s.%s"%(Date.month,Date.day)
            folder_name = subject + folder_name
            save_path=create_folder(folder_name)
            os.chdir(save_path)
            Times_zone_out = 0
            class_list = []
            
            while True:
                cmd = self.queue.get()
                if cmd != "START": continue
                
                myrecording=record()
                text_file_name = "zone_out_"+str(Times_zone_out)
                file_num= create_conversion_class (text_file_name)
                class_list.append(file_num)
                object_name=class_list[Times_zone_out]

                A=True
                
                while True:
                    ttime = timetest()
                    print(str(ttime))

                    if A == True:
                        store_numpy_1(myrecording)
                    else:
                        store_numpy_2(myrecording)

                    object_name.append_key_board_decison_list(ttime)

                    if object_name.get_length_key_board_decison_list() == 1:
                        if ttime == True:
                            A = not A
                            myrecording=record()

                        elif ttime == False:
                            Converting=threading.Thread(target = combination_general, args = (A,text_file_name,object_name,))
                            Converting.start()
                            A = not A
                            myrecording=record()     

                    else:
                        try:
                            cmd = self.queue.get_nowait()
                        except Empty:
                            cmd = ""

                        if cmd == "STOP":
                            print("STOP")
                            Converting=threading.Thread(target = combination_general, args = (A,text_file_name,object_name,))
                            Converting.start()
                        
                            wav_list=object_name.get_wav_file_list()
                            combine_waves(wav_list,Times_zone_out)
                            delete_wav_files(wav_list)
                            object_name.get_text()
                            Times_zone_out +=1
                            A = not A
                            break

                        elif object_name.get_item_in_key_board_decison_list(-1)== False and object_name.get_item_in_key_board_decison_list(-2)==True:
                            object_name.append_key_board_decison_list(ttime)
                            Converting=threading.Thread(target = combination_initial, args = (text_file_name,A,object_name,))
                            Converting.start()
                            A = not A
                            myrecording=record()
                        
                        elif object_name.get_item_in_key_board_decison_list(-1)== False and object_name.get_item_in_key_board_decison_list(-2)== False:
                            Converting=threading.Thread(target = combination_general, args = (A,text_file_name,object_name,))
                            Converting.start()
                            A = not A
                            myrecording=record()

                        elif object_name.get_item_in_key_board_decison_list(-1)== True and object_name.get_item_in_key_board_decison_list(-2)==True:
                            A = not A
                            myrecording=record()

                        elif object_name.get_item_in_key_board_decison_list(-1)== True and object_name.get_item_in_key_board_decison_list(-2)==False:
                            Converting=threading.Thread(target = combination_general, args = (A,text_file_name,object_name,))
                            Converting.start()

                            wav_list=object_name.get_wav_file_list()
                            combine_waves(wav_list,Times_zone_out)
                            delete_wav_files(wav_list)
                            object_name.get_text()

                            Times_zone_out +=1
                            A = not A
                            break

keylistener = Listener(on_press=on_press) 
keylistener.start()

mouselistener = mouse.Listener(on_move=on_move)
mouselistener.start()
