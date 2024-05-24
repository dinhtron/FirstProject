# conda activate rasa
# cd chatbot\simple_ai\FirstProject

from flask import Flask
from flask import redirect, url_for, session, jsonify,request
import openai
from dotenv import load_dotenv
import os
from app1 import auth, chatbot,webhook , toggle,activity
import mysql.connector
from flask import Flask, render_template, redirect, url_for, session
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

app.add_url_rule('/login', 'login', auth.login, methods=['GET', 'POST'])
app.add_url_rule('/register', 'register', auth.register, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', auth.logout)
app.add_url_rule('/profile', 'profile', auth.profile, methods=['GET', 'POST'])
app.add_url_rule('/chatbot', 'chatbot', chatbot.chatbot, methods=['GET', 'POST'])
app.add_url_rule('/webhook', 'webhook', webhook.webhook, methods=[ 'POST'])
app.add_url_rule('/update_toggle', 'update_toggle',webhook.update_toggle, methods=[ 'POST'])
app.add_url_rule('/update_toggle_bert', 'update_toggle_bert',webhook.update_toggle_bert, methods=[ 'POST'])
app.add_url_rule('/toggle_sound', 'toggle_sound', toggle.toggle_sound, methods=[ 'POST'])
app.add_url_rule('/voice_input', 'voice_input', toggle.voice_input, methods=[ 'POST'])
@app.route('/user_id', methods=['GET'])
def get_user_id():
    user_id = session['user_id']
    return jsonify({"user_id": user_id})
                   

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Thay đổi với mật khẩu của cơ sở dữ liệu của bạn
        database="chatbot"
    )

# Route cho bảng điều khiển
@app.route('/dashboard')
def dashboard():
    try:
        # Kết nối đến cơ sở dữ liệu
        connection = connect_to_database()

        # Thực hiện truy vấn để lấy dữ liệu người dùng
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        user_count = len(users)
        # Đóng con trỏ và kết nối
        cursor.close()
        connection.close()

        return render_template('admin/dashboard.html',user_count=user_count)
    except mysql.connector.Error as err:
        # Xử lý các lỗi của cơ sở dữ liệu
        return f"Lỗi cơ sở dữ liệu: {err}"
@app.route('/dashboard/thongbao')
def thongbao():
    return render_template('admin/thongbao.html')
@app.route('/dashboard/sukien')
def sukien():
    try:
        # Kết nối đến cơ sở dữ liệu
        connection = connect_to_database()

        # Thực hiện truy vấn để lấy dữ liệu người dùng
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM activity")
        activity = cursor.fetchall()
        # Đóng con trỏ và kết nối
        cursor.close()
        connection.close()
        print(activity)
        return render_template('admin/sukien.html', activity=activity)
    except mysql.connector.Error as err:
        # Xử lý các lỗi của cơ sở dữ liệu
        return f"Lỗi cơ sở dữ liệu: {err}"
   
# Route cho bảng điều khiển
@app.route('/dashboard/users')
def  users():
    try:
        # Kết nối đến cơ sở dữ liệu
        connection = connect_to_database()

        # Thực hiện truy vấn để lấy dữ liệu người dùng
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        # Đóng con trỏ và kết nối
        cursor.close()
        connection.close()

        # Trả về template với dữ liệu người dùng
        return render_template('admin/users.html', users=users)

    except mysql.connector.Error as err:
        # Xử lý các lỗi của cơ sở dữ liệu
        return f"Lỗi cơ sở dữ liệu: {err}"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/submit', methods=['POST','GET'])
def submit():
    name_phanhoi=request.form['name']
    message = request.form['message']
    user_id = session['user_id']
    print(name_phanhoi)
    # Kết nối tới cơ sở dữ liệu
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT name, email FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    
    if user is None:
        cursor.close()
        conn.close()
        return jsonify({"status": "error", "message": "User not found"}), 404
    
    name = user[0]  # assuming name is the first column
    email = user[1]  # assuming email is the second column
    
    cursor.execute(
        'INSERT INTO feedback (id_user, name, email, message,name_phanhoi) VALUES (%s, %s, %s, %s, %s)',
        (user_id, name, email, message,name_phanhoi)
    )
    
    conn.commit()
    
    # Đóng kết nối
    cursor.close()
    conn.close()
    
    return jsonify({"status": "success", "message": "Phản hồi đã được gửi thành công!"})
@app.route("/user_phanhoi")
def user_phanhoi():
    user_id = session['user_id']
    connection = connect_to_database()
    
        # Thực hiện truy vấn để lấy dữ liệu người dùng
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedback WHERE id_user = %s", (user_id,))
    feedback = cursor.fetchall()
        # Đóng con trỏ và kết nối
    cursor.close()
    connection.close()
    return render_template('user_phanhoi.html', feedback=feedback)
# @app.route("dashboard/phan_hoi")
# def phan_hoi():
#     user_id = session['user_id']
#     connection = connect_to_database()
    
#         # Thực hiện truy vấn để lấy dữ liệu người dùng
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM feedback ")
#     feedback = cursor.fetchall()
#         # Đóng con trỏ và kết nối
#     cursor.close()
#     connection.close()
#     return render_template('admin/phan_hoi.html',feedback=feedback)

if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)



