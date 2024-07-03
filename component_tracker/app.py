from flask import Flask, render_template, redirect, url_for, request
from models import db, Component
from forms import ComponentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///components.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    components = Component.query.all()
    return render_template('index.html', components=components)

@app.route('/add', methods=['GET', 'POST'])
def add_component():
    form = ComponentForm()
    if form.validate_on_submit():
        new_component = Component(name=form.name.data, quantity=form.quantity.data, description=form.description.data)
        db.session.add(new_component)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_component.html', form=form)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_component(id):
    component = Component.query.get_or_404(id)
    form = ComponentForm(obj=component)
    if form.validate_on_submit():
        component.name = form.name.data
        component.quantity = form.quantity.data
        component.description = form.description.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_component.html', form=form)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_component(id):
    component = Component.query.get_or_404(id)
    db.session.delete(component)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
