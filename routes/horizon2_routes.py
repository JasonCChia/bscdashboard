from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import create_connection  # your create_connection() function

horizon2_bp = Blueprint('horizon2', __name__)

def log_activity(table_name, action, record_id, user_id):
    """Log user activity to the log_activity table."""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO log_activity 
            (table_name, action, record_id, user_id)
            VALUES (%s, %s, %s, %s)
        """, (table_name, action, record_id, user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error logging activity: {e}")
    finally:
        cursor.close()
        conn.close()

def get_objective_data(objective_id):
    """Fetch initiatives, measurements, and objective notes for the given objective."""
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM initiative WHERE objective = %s", (objective_id,))
    initiatives = cursor.fetchall()
    
    cursor.execute("SELECT * FROM measurement WHERE objective = %s", (objective_id,))
    measurements = cursor.fetchall()
    
    cursor.execute("SELECT * FROM objective_note WHERE objective = %s", (objective_id,))
    objective_notes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {
        'initiatives': initiatives,
        'measurements': measurements,
        'objective_notes': objective_notes,
    }

@horizon2_bp.route('/horizon/2/objective_<string:objective_id>')
def view_objective(objective_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))

    user_role = session.get('role')
    user_horizon = int(session.get('horizon', 0))  # Ensure it's an integer

    # Store the current objective id in the session
    session['current_objective_id'] = objective_id
    print("DEBUG: current_objective_id set to", session.get('current_objective_id'))  # Debugging

    # Fetch the data from the database
    data = get_objective_data(objective_id)
    
    # Check authorization and render the template with the data
    if user_role == 'admin' or (user_role == 'user' and user_horizon == 2):
        return render_template(f'objective_{objective_id}.html',
                               objective_id=objective_id,
                               **data)
    else:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('main.home'))

# ---------------------------
# Objective Page (Read)
# ---------------------------
@horizon2_bp.route('/horizon/2/objective_<string:objective_id>/')
def objective_page(objective_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    # Save current objective id in session
    session['current_objective_id'] = objective_id

    data = get_objective_data(objective_id)
    return render_template(f'objective_{objective_id}.html',
                           objective_id=objective_id,
                           **data)

# ============================
# CRUD for Initiative Table
# ============================
@horizon2_bp.route('/horizon/2/add_initiative', methods=['GET', 'POST'])
def add_initiative():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    objective_id = session.get('current_objective_id')
    if not objective_id:
        flash('No current objective selected.', 'warning')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        initiative_name = request.form.get('initiative_name')
        target = request.form.get('target')
        achieved = request.form.get('achieved')
        status = request.form.get('status')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        note = request.form.get('note')
        created_by = session.get('user_id')

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO initiative 
            (initiative_name, objective, target, achieved, status, start_date, end_date, note, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (initiative_name, objective_id, target, achieved, status, start_date, end_date, note, created_by))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Initiative added successfully!', 'success')
        data = get_objective_data(objective_id)
        return render_template(f'objective_{objective_id}.html',
                               objective_id=objective_id,
                               **data)
    return render_template('add_initiative.html', objective_id=objective_id)

@horizon2_bp.route('/horizon/2/edit_initiative/<int:initiative_id>', methods=['GET', 'POST'])
def edit_initiative(initiative_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    objective_id = session.get('current_objective_id')
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        initiative_name = request.form.get('initiative_name')
        target = request.form.get('target')
        achieved = request.form.get('achieved')
        status = request.form.get('status')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        note = request.form.get('note')
        updated_by = session.get('user_id')
        cursor.execute("""
            UPDATE initiative 
            SET initiative_name=%s, target=%s, achieved=%s, status=%s, 
                start_date=%s, end_date=%s, note=%s, updated_by=%s
            WHERE id=%s
        """, (initiative_name, target, achieved, status, start_date, end_date, note, updated_by, initiative_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Initiative updated successfully!', 'success')
        data = get_objective_data(objective_id)
        return render_template(f'objective_{objective_id}.html',
                               objective_id=objective_id,
                               **data)

    cursor.execute("SELECT * FROM initiative WHERE id = %s", (initiative_id,))
    initiative = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_initiative.html', initiative=initiative, objective_id=objective_id)

@horizon2_bp.route('/horizon/2/delete_initiative/<int:initiative_id>', methods=['POST'])
def delete_initiative(initiative_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    objective_id = session.get('current_objective_id')
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM initiative WHERE id = %s", (initiative_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Initiative deleted successfully!', 'success')
    data = get_objective_data(objective_id)
    return render_template(f'objective_{objective_id}.html',
                           objective_id=objective_id,
                           **data)

# ============================
# CRUD for Measurement Table
# ============================
@horizon2_bp.route('/horizon/2/add_measurement', methods=['GET', 'POST'])
def add_measurement():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    objective_id = session.get('current_objective_id')
    if not objective_id:
        flash('No current objective selected.', 'warning')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        measurement_name = request.form.get('measurement_name')
        target = request.form.get('target')
        achieved = request.form.get('achieved')
        note = request.form.get('note')  # Will be used for objective_note
        created_by = session.get('user_id')

        conn = create_connection()
        cursor = conn.cursor()
        
        # Insert into measurement (without note)
        cursor.execute("""
            INSERT INTO measurement 
            (measurement_name, objective, target, achieved, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (measurement_name, objective_id, target, achieved, created_by))
        
        conn.commit()
        cursor.close()
        conn.close()

        flash('Measurement and linked note added successfully!', 'success')
        data = get_objective_data(objective_id)
        return render_template(f'objective_{objective_id}.html',
                               objective_id=objective_id,
                               **data)
    return render_template('add_measurement.html', objective_id=objective_id)

@horizon2_bp.route('/horizon/2/edit_measurement/<int:measurement_id>', methods=['GET', 'POST'])
def edit_measurement(measurement_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    objective_id = session.get('current_objective_id')
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        measurement_name = request.form.get('measurement_name')
        target = request.form.get('target')
        achieved = request.form.get('achieved')
        note = request.form.get('note')
        updated_by = session.get('user_id')
        cursor.execute("""
            UPDATE measurement 
            SET measurement_name=%s, target=%s, achieved=%s,note=%s, updated_by=%s
            WHERE id=%s
        """, (measurement_name, target, achieved, note, updated_by, measurement_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Measurement updated successfully!', 'success')
        data = get_objective_data(objective_id)
        return render_template(f'objective_{objective_id}.html',
                               objective_id=objective_id,
                               **data)

    cursor.execute("SELECT * FROM measurement WHERE id = %s", (measurement_id,))
    measurement = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_measurement.html', measurement=measurement, objective_id=objective_id)

@horizon2_bp.route('/horizon/2/delete_measurement/<int:measurement_id>', methods=['POST'])
def delete_measurement(measurement_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    objective_id = session.get('current_objective_id')
    conn = create_connection()
    cursor = conn.cursor()
        
    # Now, delete the measurement record.
    cursor.execute("DELETE FROM measurement WHERE id = %s", (measurement_id,))
    
    conn.commit()
    cursor.close()
    conn.close()

    flash('Measurement and its linked note deleted successfully!', 'success')
    data = get_objective_data(objective_id)
    return render_template(f'objective_{objective_id}.html',
                           objective_id=objective_id,
                           **data)


# ================================
# CRUD for Objective Note Table
# ================================
@horizon2_bp.route('/horizon/2/add_objective_note', methods=['GET', 'POST'])
def add_objective_note():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    objective_id = session.get('current_objective_id')
    if not objective_id:
        flash('No current objective selected.', 'warning')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        note = request.form.get('note')
        issues = request.form.get('issues')
        implication = request.form.get('implication')
        action = request.form.get('action')
        accountabilities = request.form.get('accountabilities')
        created_by = session.get('user_id')

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO objective_note 
            (objective, note, issues, implication, action, accountabilities, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (objective_id, note, issues, implication, action, accountabilities, created_by))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Objective note added successfully!', 'success')
        data = get_objective_data(objective_id)
        return render_template(f'objective_{objective_id}.html',
                               objective_id=objective_id,
                               **data)
    return render_template('add_objective_note.html', objective_id=objective_id)


@horizon2_bp.route('/horizon/2/edit_objective_note/<int:note_id>', methods=['GET', 'POST'])
def edit_objective_note(note_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    objective_id = session.get('current_objective_id')
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Retrieve all form fields
        issues = request.form.get('issues')
        implication = request.form.get('implication')
        action = request.form.get('action')
        accountabilities = request.form.get('accountabilities')
        note = request.form.get('note')

        cursor.execute("""
            UPDATE objective_note 
            SET issues = %s, implication = %s, action = %s, 
                accountabilities = %s, note = %s 
            WHERE id = %s
        """, (issues, implication, action, accountabilities, note, note_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Objective note updated successfully!', 'success')
        data = get_objective_data(objective_id)
        return render_template(f'objective_{objective_id}.html',
                               objective_id=objective_id,
                               **data)

    # GET: Fetch the note data
    cursor.execute("SELECT * FROM objective_note WHERE id = %s", (note_id,))
    objective_note = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('edit_objective_note.html',
                           objective_note=objective_note,
                           objective_id=objective_id)



@horizon2_bp.route('/horizon/2/delete_objective_note/<int:note_id>', methods=['POST'])
def delete_objective_note(note_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    objective_id = session.get('current_objective_id')
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM objective_note WHERE id = %s", (note_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Objective note deleted successfully!', 'success')
    data = get_objective_data(objective_id)
    return render_template(f'objective_{objective_id}.html',
                           objective_id=objective_id,
                           **data)
