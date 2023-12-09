#!/usr/bin/env python3 
from flask import Flask, render_template, request, redirect, url_for
from forms import RegisterForm, LoginForm, TicketForm      # Import forms from forms.py
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy    # Init SQLAlchemy

app = Flask(__name__)
app.secret_key = 'corn'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Not needed?
app.config['SECRET_KEY'] = 'corn'  # For Flask_WTF form(s)
db = SQLAlchemy(app)

# Setup for persistent login sessions across site/app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

# Define models (User, Ticket)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), unique=True) # email must be unique
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.Integer)
    dept = db.Column(db.String(30))


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.String(30)) # get dept from finding user based on their user_id?
    dept = db.Column(db.String(30))
    title = db.Column(db.String(30))
    description = db.Column(db.String(100))
    location = db.Column(db.String(30))
    attachment = db.Column(db.String(30))


# Init db & tables if needed
with app.app_context():
    db.create_all()


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    # Check for user in db, if password matches, redirect to dashboard template
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template("home.html", form=form)
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Store form info as new user
        new_user = User(name=form.name.data,
                        username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        role=form.role.data,
                        dept=form.dept.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html', form=form)
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    return render_template('dashboard.html')
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
@app.route("/tickets", methods=['GET', 'POST'])
@login_required
def tickets():
    if current_user.role == 0:
        ticket_list = Ticket.query.filter_by(created_by=current_user.name).all()  # Grab only the user's own ticket(s)
    elif current_user.role == 1:
        ticket_list = Ticket.query.filter_by(dept=current_user.dept).all()
    else:
        ticket_list = Ticket.query.all()

    return render_template("tickets.html", tickets=ticket_list)
@app.route("/submit_ticket", methods=['GET', 'POST'])
@login_required
def submit_ticket():
    form = TicketForm()

    # Pre-fill 'created_by' field
    if request.method == 'GET':
        form.created_by.data = current_user.name

    if form.validate_on_submit():
        # Store form data as new ticket
        new_ticket = Ticket(created_by=form.created_by.data,
                            title=form.title.data,
                            description=form.description.data,
                            location=form.location.data,
                            attachment=form.attachment.data)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('tickets'))

    return render_template("submit_ticket.html", form=form)
@app.route('/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)  # Grab ticket based on ticket_id match
    form = TicketForm(obj=ticket)

    # Fill form with data from current ticket
    if form.validate_on_submit():
        ticket.dept = form.dept.data
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.location = form.location.data
        ticket.attachment = form.attachment.data

        db.session.commit()  # Save any changes
        return redirect(url_for('tickets'))

    return render_template('edit_ticket.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port="8000",debug=True)
