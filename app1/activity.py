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
from app1 import auth, chatbot, activity
import mysql.connector
toggle_rasa_bert= False
toggle_rasa_response= False
openai.api_key = os.getenv('OPENAI_API_KEY')
RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatbot"
    )
def get_user_exam_score(user_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM diemthi WHERE id = %s", (user_id,))
    diemthi = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if diemthi:
        return diemthi
    else:
        return "Không tìm thấy thông tin điểm thi của bạn."
def get_bot_response(user_message):
    # Load index from storage
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        verbose=True
    )
    response_node = chat_engine.chat(user_message)
    bot_response = response_node.response
    return bot_response

def update_toggle():
    global toggle_rasa_response
    data = request.json
    current_value = toggle_rasa_response
    new_value = not current_value  # Đảo ngược giá trị hiện tại của toggle_rasa_response
    toggle_rasa_response = data.get('toggle_rasa_response', new_value)
    print("RASA: ",toggle_rasa_response)
    return jsonify({'success': True})

def update_toggle_bert():
    global toggle_rasa_bert
    data = request.json
    current_value = toggle_rasa_bert
    new_value = not current_value  # Đảo ngược giá trị hiện tại của toggle_rasa_response
    toggle_rasa_bert = data.get('toggle_rasa_response', new_value)
    print("Bert: ",toggle_rasa_bert)
    return jsonify({'success': True})


def phanhoi(user_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user and user.get('name') and user.get('email'):
        bot_response = "phan_hoi"
    else:
        missing_info = []
        if not user.get('name'):
                    missing_info.append("Tên người dùng")
        if not user.get('email'):
                    missing_info.append("Email")
                    missing_info_str = ", ".join(missing_info)
                    bot_response = f"Thiếu thông tin người dùng. Vui lòng bổ sung {missing_info_str}."
    return bot_response

def lichhoc(user_id):
    connection = connect_to_database()  # Assuming this function establishes a connection
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM lich_hoc WHERE id_user = %s", (user_id,))
        data_lichhoc = cursor.fetchone()

        if data_lichhoc:  # Check if data was found
            lichhoc = f"Lịch học của bạn: Lớp {data_lichhoc['ten_lop']} có thời khóa biểu chi tiết như sau: {data_lichhoc['thoi_khoa_bieu']}. Vui lòng sắp xếp thời gian và chuẩn bị đầy đủ cho các buổi học để đảm bảo bạn nắm bắt tốt kiến thức và hoàn thành các nhiệm vụ học tập đúng hạn."
            return lichhoc
        else:
            return None  # Indicate no schedule found

    except Exception as e:
        print(f"Error fetching schedule: {e}")  # Log any errors
        return None  # Indicate an error

    finally:
        if connection:
            cursor.close()
            connection.close()  # Ensure proper resource closure



def hoatdong():
    connection = connect_to_database()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM activity")
    activity1 = cursor.fetchall()

    # Đóng con trỏ và kết nối
    cursor.close()
    connection.close()

    # Chuyển đổi kết quả thành một danh sách các tên hoạt động
    # activity_names = [activity['name'] for activity in activity1]

    return activity1




def retrieve_previous_messages(user_id):
    # Thực hiện kết nối đến cơ sở dữ liệu
    connection =connect_to_database()
    previous_messages = []

    # Nếu kết nối thành công, thực hiện truy vấn để lấy tin nhắn trước đó của người dùng
    if connection.is_connected():
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chat_history WHERE user_id = %s", (user_id,))
        previous_messages = cursor.fetchall()
        cursor.close()

    # Đóng kết nối
    connection.close()

    # Trả về danh sách tin nhắn
    return previous_messages
