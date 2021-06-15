import soundfile as sf
import argparse 
import os
import queue
import vosk
import sys
import json
import pyttsx3
import wordtodigits
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import re
##import simpleaudio as sa
from datetime import date
import time
import pygame

pygame.mixer.init()
soundObj = pygame.mixer.Sound('Beginning.wav')
soundObj1 = pygame.mixer.Sound('1.wav')
soundObj2 = pygame.mixer.Sound('2.wav')
soundObj3 = pygame.mixer.Sound('3.wav')
soundObj4 = pygame.mixer.Sound('4.wav')
soundObj5 = pygame.mixer.Sound('5.wav')
soundObj6 = pygame.mixer.Sound('6.wav')
soundObj7 = pygame.mixer.Sound('7.wav')
soundObj8 = pygame.mixer.Sound('8.wav')
soundObj9 = pygame.mixer.Sound('9.wav')
soundObj10 = pygame.mixer.Sound('10.wav')
soundObj11 = pygame.mixer.Sound('11.wav')
soundObj12 = pygame.mixer.Sound('12.wav')
soundObj13 = pygame.mixer.Sound('13.wav')
soundObj14 = pygame.mixer.Sound('14.wav')
soundObj15 = pygame.mixer.Sound('15.wav')
soundObj16 = pygame.mixer.Sound('16.wav')
soundObj17 = pygame.mixer.Sound('17.wav')
soundObj18 = pygame.mixer.Sound('18.wav')
soundObj19 = pygame.mixer.Sound('19.wav')
soundObj20 = pygame.mixer.Sound('20.wav')
soundObj21 = pygame.mixer.Sound('21.wav')
soundObj22 = pygame.mixer.Sound('22.wav')
soundObj23 = pygame.mixer.Sound('23.wav')
soundObj24 = pygame.mixer.Sound('24.wav')
soundObj25 = pygame.mixer.Sound('25.wav')
soundObj26 = pygame.mixer.Sound('26.wav')
soundObj27 = pygame.mixer.Sound('27.wav')
soundObj28 = pygame.mixer.Sound('28.wav')
soundObj29 = pygame.mixer.Sound('29.wav')
soundObj30 = pygame.mixer.Sound('30.wav')
soundObj31 = pygame.mixer.Sound('31.wav')
soundObj32 = pygame.mixer.Sound('32.wav')
soundObj33 = pygame.mixer.Sound('33.wav')
soundObj34 = pygame.mixer.Sound('34.wav')
soundObj35 = pygame.mixer.Sound('35.wav')
soundObj36 = pygame.mixer.Sound('36.wav')
soundObj37 = pygame.mixer.Sound('37.wav')
soundObj38 = pygame.mixer.Sound('38.wav')
soundObj39 = pygame.mixer.Sound('39.wav')
soundObja = pygame.mixer.Sound('bbm_tone.wav')
soundObjb = pygame.mixer.Sound('Pipes.wav')








df = pd.read_csv('Intents.csv', header = None, names = ['Examples', 'Intent'])
device = []
appliances= ['fridge', 'tv', 'television', 'ac','air conditioner','pump','waterpump',
              'bulb','water pump','heater','microwave','cooker','kettle','electric kettle','light','speaker','refridgerator']
currencies = ['dollars', 'pounds', 'euros', 'naira', 'yuan', 'canadian dollars', 'canadian dollar', 'australian dollars', 'australian dollar',
              'dollar','pound' , 'euro']
times = ['today', 'yesterday', 'last week', 'last month', 'a month ago', 'two days ago', 'two months ago', 'three days ago', 'one month', 'one day']
quantity = []
currency = []
period= []
today = date.today()

def get_intent(text):
  global device, quantity, currency, period
  quantity = []
  currency = []
  examples_list = df['Examples'].tolist()
  quantity = list (map(int, re.findall(r'\d+', text)))
  device_check = any(appliance in text.lower() for appliance in appliances)
  currency_check  = any(currency in text.lower() for currency in currencies)
  period_check = any(time in text.lower() for time in times)
  if period_check:
    period = list(set(times).intersection(set(text.split())))
  if currency_check:
    currency =list(set(currencies).intersection(set(text.split())))
  if not 'device' in text.lower():
    if device_check:
      device =list(set(appliances).intersection(set(text.split())))
      for d in device:
        text = text.replace(d, 'device')
  elif 'it' in text.lower():
    pass
  else:
    device = []
  text = [text]
  cv = CountVectorizer()
  vectors = cv.fit_transform(examples_list+text).toarray()
  vectors_list = [vec for vec in vectors]
  similarity_scores = cosine_similarity(vectors_list)[-1][:-1]
  i=np.argmax(similarity_scores)
  intent = df[df['Examples'] == examples_list[i]]['Intent'].values[0].strip()
  return intent

def intent2action(intent):
  text = ''
  global device, quantity, currency
  if intent == 'Utilities_Device_status':
     
    if device:
        
      for d in device:
        
        
        address= fr"http://localhost/nlp/?key=passkey&device={d}&get_state=1"
        address = address.replace(' ', '%20')
        web_res  = requests.get(address).json() 
        response =  web_res['response']
        if web_res['status']==0:
            text+= f'.{response}.'
        else:#get status from db
          soundObj21.play()
          time.sleep(2)
          
          text += f'{d}'

          soundObj22.play()
          time.sleep(2)
          text += f'{rerfsponse}'

    else:
      soundObj1.play()
      time.sleep(2)

  elif intent == 'Utilities_Device_Usage':

    if device and period:
      for d in device:
        address = fr"http://localhost/nlp/?key=passkey&device={d}&get_energy=1&period={period}"
        address = address.replace(' ', '%20')
        
        web_res = requests.get(address).json()
        usage = web_res['response']

        soundObj21.play()
        time.sleep(2)

        text += f'.{d}.'

        soundObj23.play()
        time.sleep(2)

        text += f'.{period}.'

        soundObj24.play()
        time.sleep(2)

        text += f'.{usage}.'

        soundObj25.play()
        time.sleep(2)



    elif device:
      address = fr"http://localhost/nlp/?key=passkey&device={d}&get_energy=1&period=today"
      address = address.replace(' ', '%20')
      web_res = requests.get(address).json()
      usage = web_res['response']

      soundObj39.play()
      time.sleep(2)

      text += f'.{usage}.'

    else:
      soundObj1.play()
      time.sleep(2)
        

  elif intent == 'Turn_off_device':
    if device:
      for d in device:
        address = fr"http://localhost/nlp/?key=passkey&device={d}&turn_off=1"
        address = address.replace(' ', '%20')
        web_res = requests.post(address).json()

        soundObj26.play()
        time.sleep(2)

        text += f'.{d}.'

    else:
      soundObj2.play()
      time.sleep(2)

  elif intent == 'Turn_on_device':
    if device:
      for d in device:
        address = fr"http://localhost/nlp/?key=passkey&device={d}&turn_on=1"
        address = address.replace(' ', '%20')
        web_res= requests.post(address).json()

        soundObj27.play()
        time.sleep(2)

        text += f'.{d}.'
    else:
      soundObj3.play()
      time.sleep(2)

  elif intent == 'Utilities_Energy_Balance':
      address = fr"http://localhost/nlp/?key=passkey&get_balance=1"
      address = address.replace(' ', '%20')
      web_res = requests.get(address).json()
      balance = web_res['response']
      
      soundObj28.play()
      time.sleep(2)

      text += f'.{balance}.'

      soundObj25.play()
      time.sleep(2)

  elif intent == 'Utilities_energy_price':
      address = fr"http://localhost/nlp/?key=passkey&get_price=1"
      address = address.replace(' ', '%20')
      web_res= requests.get(address).json()
      price = web_res['response'] 
      if quantity and currency:

        soundObj29.play()
        time.sleep(2)

        text+= f'.{quantity[0]/price}.'

        soundObj30.play()
        time.sleep(2)

        text+= f'.{quantity[0]} {currency[0]}.'

      elif quantity:
        price = price * quantity[0]

        soundObj31.play()
        time.sleep(2)

        text += f'.{quantity[0]}.'

        soundObj32.play()
        time.sleep(2)

        text += f'.{price}.'


      else:

        soundObj33.play()
        time.sleep(2)

        text += f'.{price}.'

  elif intent == 'Utilities_Recharge_Account':
    if quantity and currency:

      soundObj34.play()
      time.sleep(5)

      text += f'{quantity[0]} {currency[0]}'

    elif quantity:

      soundObj35.play()
      time.sleep(2)

      text += f'{quantity[0]}'

      soundObj25.play()
      time.sleep(2)

    else:
      soundObj4.play()
      time.sleep(2)
      
   

  elif intent == 'Utilities_View_Usage':
    if period:
      address = fr"http://localhost/nlp/?key=passkey&get_energy=1&period={period}"
      address = address = address.replace(' ', '%20')
      web_res = requests.get(address).json()
      usage = web_res['response']

      soundObj36.play()
      time.sleep(2)
      

      text += f'{period[0]}'
      

      soundObj24.play()
      time.sleep(2)
     

      text += f'{usage}'

      



    else:
      address = fr"http://localhost/nlp/?key=passkey&get_energy=1&period=today"
      address = address = address.replace(' ', '%20')
      web_res = requests.get(address).json()
      usage = web_res['response']

      soundObj37.play()
      time.sleep(2)

    
      text += f"{usage}"

  # elif intent == 'Age':
  #   filename = '5.wav'
  #   data, fs = sf.read(filename, dtype='float32')
  #   #sd.play(data, fs)
  #   status = sd.wait()
  #   soundObj5.play()
  #   time.sleep(2)

  elif intent == 'Ask_question':
    soundObj6.play()
    time.sleep(2)
    t="Sure how can I be of help?"

  elif intent == 'Bored':
    soundObj7.play()
    time.sleep(2)
    t="So sorry about that"

  elif intent == 'Love':
    soundObj8.play()
    time.sleep(5)
    t="I'm happy being single. the upside is I get to focus on managing your Energy"


  elif intent == 'Compliment':
    soundObj9.play()
    time.sleep(2)
    t="Oh!, thank you. i'm blushing right now!."

  
  elif intent == 'Hobby':
    soundObj10.play()
    time.sleep(2)
    t="I love to help you manage your energy"


  elif intent == 'get_personal':
    soundObj11.play()
    time.sleep(2)
    t="I,m your energy concierge!"


  elif intent == 'Pissed':
    soundObj12.play()
    time.sleep(5)
    t="sorry!, boss!!"


  elif intent == 'Language':
    soundObj13.play()
    time.sleep(5)
    t="I speak English. Visit your language settings to change"


  elif intent == 'Boss':
    soundObj14.play()
    time.sleep(2)
    t="I was made by Robotics & Artificial Intelligence Nigeria."
    


  elif intent == 'Retraining':
    soundObj15.play()
    time.sleep(2)
    t="I learn everyday!"



  elif intent == 'Job':
    soundObj16.play()
    time.sleep(2)
    t="I'm always happy to help!"


  #elif intent == 'know_weather':
    #text+= f"The weather today is..." #get from db

  elif intent == 'know_date':
    d2 = today.strftime("%B %d, %Y")

    soundObj38.play()
    time.sleep(2)
    
    text+= f".{d2}" 

  elif intent == 'End_conversation':
    soundObj17.play()
    time.sleep(2)
    t="I'm happy I was able to help"

    
  elif intent == 'Ask_question':

    soundObj18.play()
    time.sleep(2)
    t="Sure how can I help?"

    
  elif intent == 'greeting':

    soundObj19.play()
    time.sleep(2)
    t="Hey! How may I be of assistance?"

      
  elif intent == 'Utilities_Report_Outage':
    soundObjb.play()
    time.sleep(7)
    t="Our team will respond, to your request! as soon as possible."

      
  elif intent == 'Utilities_Start_Service':
    soundObjb.play()
    time.sleep(7)
    t="Our team will respond, to your request! as soon as possible."
      
  elif intent == 'Utilities_Stop_Service':
    soundObjb.play()
    time.sleep(7)
    t="Our team will respond, to your request! as soon as possible."
      
  else:
    soundObjb.play()
    time.sleep(2)


  return text
      



def speakword(text):

  if text !='':
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 140)
    engine.say(text)
    engine.runAndWait()
    
    
q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
    
    
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 16000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    jres = json.loads((rec.Result()))
                    print (jres) 
                    
                    if ("hello vivian" in jres["text"]) or ("hello" in jres["text"]) or ("vivian" in jres["text"]):
                        # address = fr"http://localhost/nlp/vivian.php?trigger=true"
                        # requests.get(address)
                        
                        # filename = 'Beginning.wav'
                        # data, fs = sf.read(filename, dtype='float32')
                        # # sd.play(data, fs)
                        # status = sd.wait()
                        soundObj.play()

                        not_done_with_Q= True

                        

                    
                        
                        
                        

                        
                        
                        
                        
                        
                        while not_done_with_Q:
                             
                            data= q.get()
                            if rec.AcceptWaveform(data):
                                jres = json.loads((rec.Result()))
                                print (jres)    
                           
                                if jres['text'] != '':
                                  finaltext= wordtodigits.convert((jres["text"]))
                                  user_intent = get_intent(finaltext)
                                  adeus_reply = intent2action(user_intent)
                                  print(adeus_reply)

                                  f = open("nlp_q.txt","w")
                                  f.write(jres['text'])
                                  f.close()

                                  f2 = open("nlp_r.txt","w")
                                  f2.write(adeus_reply)
                                  f2.close()

                                  if adeus_reply.startswith('Which device do you'):
                                      
                                      speakword(adeus_reply)
                                      q.queue.clear()
                                      time.sleep(2)
                                      while True: 
                                          data = q.get()
                                          if rec.AcceptWaveform(data):
                                              jres = json.loads(rec.Result())
                                              finaltext = wordtodigits.convert(jres["text"])
                                              print(jres["text"])
                                              device_check = any(appliance in finaltext.lower() for appliance in appliances)
                                              if device_check:
                                                  device =list(set(appliances).intersection(set(finaltext.split())))
                                                  print(device)
                                                  adeus_reply= intent2action(user_intent)
                                                  speakword(adeus_reply)
                                                  q.queue.clear()
                                                  break
                                              
                                          
                                              else:
                                                  speakword("please respond with a device name")
                                                  q.queue.clear()
                                              
                                      
                                          
                                          
                                  elif adeus_reply.startswith('How many kilowatts'):
                                      speakword(adeus_reply)
                                      q.queue.clear()
                                      time.sleep(2)
                                      while True:
                                          data = q.get()
                                          if rec.AcceptWaveform(data):
                                              jres = json.loads(rec.Result())
                                              print(jres["text"])
                                              finaltext = wordtodigits.convert(jres["text"])
                                              quantity = list (map(int, re.findall(r'\d+', finaltext)))
                                              currency_check  = any(currency in finaltext.lower() for currency in currencies)
                                              if currency_check and quantity:
                                                  currency = list(set(currencies).intersection(set(finaltext.split())))
                                                  adeus_reply = intent2action(user_intent)
                                                  speakword(adeus_reply)
                                                  q.queue.clear()
                                                  break
                                              elif quantity:
                                                  adeus_reply = intent2action(user_intent)
                                                  print(user_intent)
                                                  speakword(adeus_reply)
                                                  q.queue.clear()
                                                  break
                                              else:
                                                  speakword("please respond with how much energy you need")
                                                  q.queue.clear()
                                                  
                                  elif adeus_reply.startswith('For which period'):
                                      speakword(adeus_reply)
                                      q.queue.clear()
                                      while True:          
                                          data = q.get()
                                          rec.AcceptWaveform(data)
                                          jres = json.loads(rec.Result())
                                          finaltext = wordtodigits.convert(jres["text"])
                                          quantity = list (map(int, re.findall(r'\d+', finaltext)))
                                          period_check  = any(time in finaltext.lower() for time in times)
                                          if period_check:
                                              period = list(set(times).intersection(set(finaltext.split())))
                                              adeus_reply = intent2action(user_intent)
                                              speakword(adeus_reply)
                                              q.queue.clear()
                                              break
                                          else:
                                              speakword("please respond with the period you want ")
                                                          
                                                          
                                  else:
                                      speakword(adeus_reply)
                                      q.queue.clear()

                            if ("thank you" in jres["text"]) or ("bye" in jres["text"]):
                                # address = fr"http://localhost/nlp/vivian.php?trigger=false"
                                # requests.get(address)
                                
                                not_done_with_Q= False
                                filename = 'bbm_tone.wav'
                                data, fs = sf.read(filename, dtype='float32')
                                # sd.play(data, fs)
                                status = sd.wait()
                                soundObja.play()

                    
                                
                                                            
                                                            
                                                           
except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
