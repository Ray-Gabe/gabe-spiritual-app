from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user
from gabe_app.models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.chat_interface'))

    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        age_range = data.get('age_range', '').strip()

        if not all([username, password, name, age_range]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400

        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password too short'}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Username already exists'}), 400

        new_user = User(username=username, name=name, age_range=age_range)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            new_user.update_last_login()
            return jsonify({'success': True, 'redirect_url': url_for('main.chat_interface')})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Registration failed.'}), 500

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.chat_interface'))

    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            user.update_last_login()
            return jsonify({'success': True, 'redirect_url': url_for('main.chat_interface')})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
