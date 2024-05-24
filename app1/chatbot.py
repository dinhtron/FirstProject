from flask import Flask, render_template, request, jsonify, url_for, redirect
import requests
import speech_recognition as sr
from io import BytesIO
import mysql.connector
from datetime import datetime
from flask import redirect, url_for, session
import openai
from llama_index.core import StorageContext, load_index_from_storage
from dotenv import load_dotenv
import os
import json
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from app1 import auth
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatbot"
    )

def chatbot():
    if 'user_id' in session:
        user_id = session['user_id']
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('index.html', user=user)
    else:
        return redirect(url_for('login'))

def create_chat_history_table():
    try:
        connection = auth.connect_to_database()
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS chat_history (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, user_message TEXT, bot_response TEXT, timestamp DATETIME)")
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error creating chat history table:", e)

# Hàm lưu tin nhắn với user_id
def save_message(user_id, user_message, bot_response):
    try:
        connection = auth.connect_to_database()
        cursor = connection.cursor()
        query = "INSERT INTO chat_history (user_id, user_message, bot_response, timestamp) VALUES (%s, %s, %s, %s)"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(query, (user_id, user_message, bot_response, timestamp))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error saving message:", e)
        
def save_feedback(user_id, message):
    try:
        # Thực hiện kết nối đến cơ sở dữ liệu
        connection = connect_to_database()

        # Nếu kết nối thành công, truy vấn để lấy thông tin name và email từ bảng users
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
            user_info = cursor.fetchone()

            # Nếu tìm thấy thông tin user, thêm feedback vào bảng feedback
            if user_info:
                name = user_info['name']
                email = user_info['email']
                sql_query = "INSERT INTO feedback (name, email, message, created_at, id_user) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_query, (name, email, message, datetime.now(), user_id))
                connection.commit()
                
            cursor.close()

    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        # Đóng kết nối
        if 'connection' in locals() and connection.is_connected():
            connection.close()
def switch_response_mode():
    global toggle_rasa_response
    toggle_rasa_response = not toggle_rasa_response