from flask import render_template, redirect, url_for, flash, request, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import LoginForm, RegisterForm, AddDiveForm, ChangePasswordForm
from app.models import User, DiveSite, DiveEvent, Favourites
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import request, jsonify, session

# Displays dives site as default page
@app.route('/')
@app.route('/dive_sites')
def dive_sites():

    sort_filter = request.args.get('sort', 'asc')  # Default to 'asc' for A-Z
    page = request.args.get('page', 1, type=int)  # Current page number
    per_page = 10  # Number of items per page

    # Apply sorting based on the filter
    if sort_filter == 'asc':
        paginated_sites = DiveSite.query.order_by(DiveSite.name.asc()).paginate(page=page, per_page=per_page)
    elif sort_filter == 'desc':
        paginated_sites = DiveSite.query.order_by(DiveSite.name.desc()).paginate(page=page, per_page=per_page)
    else:
        paginated_sites = DiveSite.query.paginate(page=page, per_page=per_page)  # Default sorting

    # Get favourite site ids for the current user
    favourite_site_ids = []
    if current_user.is_authenticated:
        favourite_site_ids = [favourite.dive_site_id for favourite in Favourites.query.filter_by(user_id=current_user.id).all()]

    return render_template(
        'sites.html',
        paginated_sites=paginated_sites,
        favourite_site_ids=favourite_site_ids,
        sort_filter=sort_filter
    )


   
#Route for logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('dive_sites'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            session['username'] = user.username  # Store username in session
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Set cookies_accepted to 'false' on login
            resp = make_response(redirect(url_for('dive_sites')))
            resp.set_cookie('cookies_accepted', 'false', max_age=60 * 60 * 24 * 7)  # 7 days
            return resp

        flash('Email or password is incorrect', 'danger')

    return render_template('login.html', form=form)

#Route to change passwords
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Allow the user to change their password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Check if the current password matches
        if not check_password_hash(current_user.password, form.current_password.data):
            flash('Information not correct: Current password is incorrect.', 'danger')
            return redirect(url_for('change_password'))

        # Ensure new password and confirmation match 
        if form.new_password.data != form.confirm_password.data:
            flash('Current password is incorrect or new passwords dont match', 'danger')
            return redirect(url_for('change_password'))

        # Update the password in the database
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('dive_sites'))  # Redirect to a relevant page

    return render_template('change_password.html', form=form)


#Route to allow users to register
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)

        # Check if the email already exists
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email is already registered. Please use a different email.', 'danger')
            return render_template('register.html', form=form)

        # Check if passwords match
        if form.password.data != form.confirm_password.data:
            flash('Passwords must match.', 'danger')
            return render_template('register.html', form=form)

        # Hash the password and create a new user
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        
        try:
            db.session.commit()
            flash('Account created. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')

    return render_template('register.html', form=form)

# Route to lougout 
@app.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    session.pop('username', None)
    session.pop('login_time', None)
    logout_user()
    flash('You are now logged out', 'info')
    return redirect(url_for('dive_sites'))


# Add a Dive
@app.route('/add_dive', methods=['GET', 'POST'])
@login_required
def add_dive():
    """Allow the user to add a dive event."""
    form = AddDiveForm()
    form.site_id.choices = [(site.id, site.name) for site in DiveSite.query.order_by(DiveSite.name.asc()).all()]


    if form.validate_on_submit():
        # Convert the form's date string into a datetime object
        dive_date = datetime.strptime(form.date.data, '%Y-%m-%dT%H:%M')

        # Create a new DiveEvent instance
        new_dive = DiveEvent(
            user_id=current_user.id,
            dive_site_id=form.site_id.data,
            date=dive_date
        )
        db.session.add(new_dive)
        db.session.commit()

        flash('Dive added successfully!', 'success')
        return redirect(url_for('dive_log')) 

    return render_template('add_dive.html', form=form)


# My Dives Page - allowing to be displayed in time order

@app.route('/dive_log')
@login_required
def dive_log():
    """Show the logged-in user's dive events."""
    order = request.args.get('order', 'desc')  

    if order == 'asc':
        dive_events = DiveEvent.query.filter_by(user_id=current_user.id).order_by(DiveEvent.date.asc()).all()
    else:
        dive_events = DiveEvent.query.filter_by(user_id=current_user.id).order_by(DiveEvent.date.desc()).all()

    return render_template('dive_log.html', dive_events=dive_events, current_order=order)
    


#route to display dive site when a user pressed on a dive log
@app.route('/dive_site/<int:site_id>')
def dive_site_detail(site_id):
    dive_site = DiveSite.query.get(site_id)  
    return render_template('display_dive_site.html', site=dive_site)



#Route to favourite heart button
@app.route('/favorite/<int:site_id>', methods=['POST'])
def favorite_dive_site(site_id):
    """Mark a dive site as favorite."""
    dive_site = DiveSite.query.get(site_id)
    if dive_site in current_user.favorites:
        return jsonify({"success"})
    current_user.favorites.append(dive_site)
    db.session.commit()
    return jsonify({"success": True, "message": "Favourite added"})


# Route to unfavourite the heart icon
@app.route('/unfavorite/<int:site_id>', methods=['POST'])
def remove_favorite_dive_site(site_id):
    """Remove a dive site from favorites."""
    dive_site = DiveSite.query.get(site_id)
    if dive_site not in current_user.favorites:
        return jsonify({"success"})
    current_user.favorites.remove(dive_site)
    db.session.commit()
    return jsonify({"success": True, "message": "Removed"})


#Route to set cookies
@app.route('/setcookie', methods=['POST'])
def setcookie():
    """Set the cookies_accepted cookie."""
    resp = make_response(jsonify({'success': True, 'message': 'Cookies accepted'}))
    resp.set_cookie('cookies_accepted', 'true', max_age=60 * 60 * 24 * 7)  # 7 days
    return resp



#Used this route to verify that cookies have been initialised
@app.route('/getcookie')
def getcookie():
    cookies_accepted = request.cookies.get('cookies_accepted')
    if cookies_accepted == 'true':
        return " Cookies accepted"
    return "cookies not accpeted"
        

# Route to display favourite dive sites for users
@app.route('/favourites')
@login_required
def favourites():
    """Display user's favourite dive sites with pagination."""
    page = request.args.get('page', 1, type=int)  # Current page number
    per_page = 10  # Number of items per page

    # Query favourite dive site IDs for the current user
    favourite_site_ids = (
        db.session.query(Favourites.dive_site_id)
        .filter(Favourites.user_id == current_user.id)
        .all()
    )
    favourite_site_ids = [id[0] for id in favourite_site_ids]

    # Query the dive sites that are favourited by the user and paginate
    paginated_favourites = DiveSite.query.filter(DiveSite.id.in_(favourite_site_ids)).paginate(
        page=page, per_page=per_page
    )

    return render_template(
        'favourites.html',
        paginated_favourites=paginated_favourites,
        favourite_site_ids=favourite_site_ids
    )


@app.route('/mark_as_favourite/<int:site_id>', methods=['POST'])
@login_required
def toggle_favourite(site_id):
    """Toggle the favourite state of a dive site and update the database."""
    favourite = Favourites.query.filter_by(user_id=current_user.id, dive_site_id=site_id).first()

    if favourite:
        db.session.delete(favourite)
        db.session.commit()
        favourited = False
    else:
        new_favourite = Favourites(user_id=current_user.id, dive_site_id=site_id)
        db.session.add(new_favourite)
        db.session.commit()
        favourited = True

    favourite_count = Favourites.query.filter_by(dive_site_id=site_id).count()

    return jsonify({"success": True, "favourited": favourited, "favourite_count": favourite_count})


#Route to get favourites
@app.route('/get_favourites', methods=['GET'])
@login_required
def get_favourites():
    """Return the list of favourite site IDs for the logged-in user."""
    favourites = Favourites.query.filter_by(user_id=current_user.id).all()
    favourite_site_ids = [f.dive_site_id for f in favourites]
    return jsonify({'favourites': favourite_site_ids})
