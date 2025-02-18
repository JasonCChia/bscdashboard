from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from utils import hash_password
import mysql.connector

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('main.home'))
    
    users = User.get_all()
    return render_template('admin_dashboard.html', users=users)

@admin_bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        horizon = request.form.get('horizon', 0)

        hashed_password = hash_password(password)

        try:
            User.create(name, email, hashed_password, role, horizon)
            flash('User created successfully!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except mysql.connector.Error as err:
            if err.errno == 1062:
                flash('Email already exists!', 'error')
            else:
                flash(f'Error: {err}', 'error')
    
    return render_template('create_user.html')

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        horizon = request.form.get('horizon', 0)
        new_password = request.form.get('new_password')

        existing_user = User.get_by_email(email)
        if existing_user and existing_user['id'] != user_id:
            flash('Email already exists!', 'error')
            return redirect(url_for('admin.edit_user', user_id=user_id))

        hashed_password = hash_password(new_password) if new_password else None

        try:
            User.update(user_id, name, email, role, horizon, hashed_password)
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')

    user = User.get_by_id(user_id)
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('edit_user.html', user=user)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('main.home'))
    
    try:
        User.delete(user_id)
        flash('User deleted successfully!', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'error')
    return redirect(url_for('admin.admin_dashboard'))