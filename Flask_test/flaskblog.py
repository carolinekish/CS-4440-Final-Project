from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'd731b23257269647d5634c7bd1f9dd4d'

posts = [
    {
        'author': 'NB',
        'title': 'Item 1',
        'content': 'Data can be displayed iteratively like this',
        'date_posted': 'April 20, 2069'
    },
    {
        'author': 'NB',
        'title': 'Item 2',
        'content': 'when items are placed in a list.',
        'date_posted': 'April 22, 2069'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='about')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check username and password.', 'danger')
    return render_template('login.html', title='login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
