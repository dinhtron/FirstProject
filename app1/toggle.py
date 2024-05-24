
from flask import Flask, render_template, request, jsonify, url_for, redirect
import requests
import speech_recognition as sr
from io import BytesIO
import mysql.connector
from datetime import datetime
from flask import redirect, url_for, session
from dotenv import load_dotenv
from llama_index.core.chat_engine import CondenseQuestionChatEngine
RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'


sound_enabled = True
def toggle_sound():
    global sound_enabled
    data = request.json
    sound_enabled = data.get('sound_enabled', False)
    return jsonify({'success': True})

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        user_message = recognizer.recognize_google(audio, language='vi-VN')
        print("User Message:", user_message)
        # Forward user's voice message to Rasa server
        rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
        rasa_response_json = rasa_response.json()
        print("Rasa Response:", rasa_response_json)
        bot_response = rasa_response_json[0]['text'] if rasa_response_json else 'Xin lỗi, tôi không hiểu điều đó.'

        # Print the bot response
        print("Bot Response:", bot_response)
        return jsonify({'response': bot_response})

    except sr.UnknownValueError:
        print("Could not understand audio")
        return jsonify({'response': 'Xin lỗi, tôi không thể hiểu âm thanh của bạn.'})

    except sr.RequestError as e:
        print("Error with the service: {0}".format(e))
        return jsonify({'response': 'Xin lỗi, có lỗi xảy ra với dịch vụ nhận dạng giọng nói.'})