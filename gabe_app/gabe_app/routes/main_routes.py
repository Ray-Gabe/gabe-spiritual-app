from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', name=current_user.name)
    return render_template('welcome.html')

@main_bp.route('/chat')
@login_required
def chat_interface():
    return render_template('chat.html', name=current_user.name)
