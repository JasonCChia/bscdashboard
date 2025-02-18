from flask import Blueprint, render_template, redirect, url_for, session, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        return render_template('home.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/horizon/<int:horizon_id>')
def view_horizon(horizon_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))

    user_role = session.get('role')
    user_horizon = session.get('horizon')

    if user_role == 'admin':
        return render_template(f'horizon{horizon_id}.html')
    elif user_role == 'user' and user_horizon == horizon_id:
        return render_template(f'horizon{horizon_id}.html')
    else:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('main.home'))