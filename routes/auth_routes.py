from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from utils import hash_password
import mysql.connector
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        horizon = request.form.get('horizon')

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.register'))

        hashed_password = hash_password(password)
        role = ""

        try:
            User.create(name, email, hashed_password, role, horizon)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except mysql.connector.Error as err:
            if err.errno == 1062:
                flash('Email already exists!', 'error')
            else:
                flash(f'Error: {err}', 'error')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = hash_password(password)

        user = User.get_by_email(email)
        if user and user['password'] == hashed_password:
            session.permanent = True
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['horizon'] = user['horizon']
            session['objective'] = user['objective']
            session['last_activity'] = os.times().elapsed
            flash('Login successful!', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password!', 'error')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))