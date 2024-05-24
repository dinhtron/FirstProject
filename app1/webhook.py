from flask import Flask, render_template, request, jsonify, url_for, redirect
import requests
import speech_recognition as sr
from datetime import datetime
from flask import redirect, url_for, session
import openai
from llama_index.core import StorageContext, load_index_from_storage
from dotenv import load_dotenv
import os
import json
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from app1 import auth, chatbot, activity,bert
import torch
from transformers import BertTokenizer, BertForSequenceClassification
toggle_rasa_response= False
toggle_rasa_bert= False
openai.api_key = os.getenv('OPENAI_API_KEY')
RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'



def webhook():
   dulieu = []
   user_id = session.get('user_id')
   print("User ID:", user_id)
   user_message = request.json['message']
   print("Bert:",toggle_rasa_bert)
   print("GPT:",toggle_rasa_response)
   if toggle_rasa_bert:
      bot_response=bert.bert_modun(user_message) 
      if  bot_response == "hoat_dong":
                     dulieu = activity.hoatdong()
      if bot_response == "diem_thi":
                     dulieu = activity.get_user_exam_score(user_id)
   else:
         print("User Message:", user_message) 
        
         if toggle_rasa_response:
            bot_response = activity.get_bot_response(user_message)
            print("Bot:", bot_response) 
         else:
            rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
            rasa_response_json = rasa_response.json()
            print("Rasa Response:", rasa_response_json)
            print(toggle_rasa_response)
            if rasa_response_json:
                  
                  bot_response = rasa_response_json[0]['text']
                  if  bot_response == "hoat_dong":
                     dulieu = activity.hoatdong()
                  if bot_response == "diem_thi":
                     dulieu = activity.get_user_exam_score(user_id)
                  if bot_response == "lich_hoc":
                     bot_response = activity.lichhoc(user_id)
            else:
                  bot_response = activity.get_bot_response(user_message)
    
   return jsonify({'response': bot_response,"dulieu": dulieu})

def update_toggle():
    global toggle_rasa_response
    data = request.json
    current_value = toggle_rasa_response
    new_value = not current_value  # Đảo ngược giá trị hiện tại của toggle_rasa_response
    toggle_rasa_response = data.get('toggle_rasa_response', new_value)
    print("RASA:",toggle_rasa_response)
    return jsonify({'success': True})

def update_toggle_bert():
    global toggle_rasa_bert
    data = request.json
    current_value = toggle_rasa_bert
    new_value = not current_value  # Đảo ngược giá trị hiện tại của toggle_rasa_response
    toggle_rasa_bert = data.get('toggle_rasa_response', new_value)
    print("Bert:",toggle_rasa_bert)
    return jsonify({'success': True})