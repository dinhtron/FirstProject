from flask import render_template, request, redirect, url_for, session
import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatbot"
    )

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Kiểm tra xem username và password được cung cấp có khớp với bất kỳ tài khoản nào trong cơ sở dữ liệu MySQL hay không
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        account = cursor.fetchone()
        cursor.close()
        connection.close()
        if account:
            # Lưu user ID vào session
            session['user_id'] = account['id']
            # Chuyển hướng đến trang chatbot
            return redirect(url_for('chatbot'))

        # Nếu đăng nhập thất bại, render lại trang đăng nhập với thông báo lỗi
        error = 'Tên người dùng hoặc mật khẩu không hợp lệ'
        return render_template('login.html', error=error)
    # Render trang đăng nhập
    return render_template('login.html')

def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Kiểm tra xem username đã tồn tại trong cơ sở dữ liệu chưa
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            # Nếu username đã tồn tại, render lại trang đăng ký với thông báo lỗi
            error = 'Tên người dùng đã tồn tại. Vui lòng chọn tên người dùng khác.'
            return render_template('register.html', error=error)
        
        # Nếu username chưa tồn tại, thêm người dùng mới vào cơ sở dữ liệu
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        cursor.close()
        connection.close()
        
        # Chuyển hướng đến trang đăng nhập sau khi đăng ký thành công
        return redirect(url_for('login'))

    # Render trang đăng ký cho phương thức GET
    return render_template('register.html')

def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            new_username = request.form['new_username']
            new_password = request.form['new_password']
            
            # Cập nhật thông tin người dùng trong cơ sở dữ liệu
            cursor.execute("UPDATE users SET username = %s, password = %s WHERE id = %s", (new_username, new_password, user_id))
            connection.commit()

            # Truy xuất lại thông tin người dùng sau khi cập nhật
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            
            # Hiển thị lại trang profile với thông tin người dùng đã được cập nhật
            return render_template('profile.html', user=user)
        
        # Nếu là phương thức GET, chỉ cần hiển thị trang profile
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
