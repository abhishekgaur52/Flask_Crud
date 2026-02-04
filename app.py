from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        emp = Employee(name=name, email=email)
        db.session.add(emp)
        db.session.commit()
        return redirect("/")
    allemployee = Employee.query.all()
    return render_template("index.html", allemployee=allemployee)

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    emp = Employee.query.filter_by(sno=sno).first()
    if request.method == "POST":
        emp.name = request.form["name"]
        emp.email = request.form["email"]
        db.session.commit()
        return redirect("/")
    return render_template("update.html", emp=emp)

@app.route("/delete/<int:sno>")
def delete(sno):
    emp = Employee.query.filter_by(sno=sno).first()
    db.session.delete(emp)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)