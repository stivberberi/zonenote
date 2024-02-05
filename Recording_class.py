import datetime

class conversion_file:
  def __init__(self,file_name): #think about name of the foler and wav file later #file_name passed as current DT
    self.key_board_decision_list = [] 
    #we need to compare the current keyboard input condition with the previous one to decide if we want to initiate a new file
    #or if we need to append the current information into the previous file
    # if previous condition = yes input, this condition= no input, it means that we are initiating a new file (it is a new episode of aura)
    # if previous condition = no input, this condition = no input, it means that we are appending to the previous file (it is a new episode of aura)
    # if previous condition = no input, this condition = yes input, it means that we are wraping up this file (this aura episode is over)
    # if previous condition = yes input, this condition = yes input, it means that we will pass(no need of converting)

    self.wav_file_list=[] #for combining the wav files into one big wave file later
    self.text_file_name = file_name+".txt"    # initaie a text file with current time
    
  def create_text_file(self):
    entire_text_file = open(self.text_file_name, "a")
    entire_text_file.close()
  
  def get_text_file_name(self):
    return self.text_file_name

  def get_length_key_board_decison_list(self):
    length = len(self.key_board_decision_list)
    return length
  
  def get_item_in_key_board_decison_list(self,item):
    return self.key_board_decision_list[item]

  def get_wav_file_list(self):
    return self.wav_file_list

  def get_text(self):#accept a string
    file_name_5 = self.text_file_name
    entire_text_file = open(file_name_5, "r")
    read=entire_text_file.readlines()
    print(read)
    entire_text_file.close()
    
  def append_key_board_decison_list(self,condition):
    self.key_board_decision_list.append(condition)
    print("the list saved is currently:",self.key_board_decision_list) #take away later

  def append_wav_file_list(self,new_wav_file):
    self.wav_file_list.append(new_wav_file)

  def append_text(self,text):#accept a string
    file_name_4 = self.text_file_name
    entire_text_file = open(file_name_4, "a")
    entire_text_file.writelines(text)
    entire_text_file.close()