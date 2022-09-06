from flask import *
import pymysql as pm

db = pm.connect(host ="localhost",
                user = "root",
                password="",
                database="project")

cursor = db.cursor()
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/donors")
def donors():
    cursor.execute("select * from donations")
    data = cursor.fetchall()
    return render_template("donors.html",data=data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/importance")
def importance():
    return render_template("importance.html")

@app.route("/benefits")
def benefits():
    return render_template("benefits.html")


@app.route("/donors",methods=["POST"])
def create():
    name = request.form.get('name')
    surname = request.form.get('surname')
    bgroup = request.form.get('bgroup')
    address = request.form.get('address')
    age = request.form.get('age')
    weight = request.form.get('weight')
    insq = " insert into donations(Name,Surname,Blood_group,Address,Age,Weight) values('{}','{}','{}','{}','{}','{}')".format(name,surname,bgroup,address,age,weight)
    try:
        cursor.execute(insq)
        db.commit()
        return redirect(url_for('donors'))
    except:
        db.rollback()
        return "Error in query"

@app.route('/delete',methods=['GET'])
def delete():
    id = request.args.get("did")
    delq = "delete from donations where SNo={}".format(id)
    try:
        cursor.execute(delq)
        db.commit()
        return redirect(url_for('donors'))
    except:
        db.rollback
        return "Error in query"

@app.route("/edit")
def edit():
    id = request.args.get('did')
    selq="select * from donations where SNo={}".format(id)
    cursor.execute(selq)
    data = cursor.fetchone()
    return render_template("edit.html",i=data)

@app.route("/update",methods=["POST"])
def update():
    name = request.form.get('name')
    surname = request.form.get('surname')
    bgroup = request.form.get('bgroup')
    address = request.form.get('address')
    age = request.form.get('age')
    weight = request.form.get('weight')
    id = request.form.get('id')
    upsq = "update donations set Name='{}',Surname='{}',Blood_group='{}',Address='{}',Age='{}',Weight='{}' where SNo={}".format(name,surname,bgroup,address,age,weight,id)
    try:
        cursor.execute(upsq)
        db.commit
        return redirect(url_for("donors"))
    except:
        db.rollback()
        return "Error in query"

@app.route("/search")
def search():
    render_template("search.html")

@app.route("/getdata",methods=["POST"])
def getdata():
    id=request.form.get('id')
    selq = "select * from donations where SNo={}".format(id)
    cursor.execute(selq)
    data = cursor.fetchone()
    return render_template('search.html',i=data)






if __name__ == "__main__":
    app.run(debug=True)
