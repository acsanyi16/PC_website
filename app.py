from flask import *
import sqlite3
import psutil

app = Flask(__name__)
ram_usage = psutil.virtual_memory()[2]
print(ram_usage)

disk_usage = psutil.disk_usage('/')[0]
disk_usage_GB = int(disk_usage/1024/1024/1024)

cpu_usage = psutil.cpu_percent(4)
print(cpu_usage)

@app.route("/")
def index():
    return render_template("index.html", RAM=ram_usage, CPU=cpu_usage, DISK=disk_usage_GB)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Employees (name, email, address) values (?,?,?)", (name, email, address))
                con.commit()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()

valami = 100
@app.route("/view")
def view():
    con = sqlite3.connect("employee.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows, RAM= ram_usage)


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("employee.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Employees where id = ?", id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)

@app.route("/update")
def update():
    return render_template("update.html")

@app.route("/updatedetails", methods=["POST"])
def updaterecord():
    msg = "msg"
    if request.method == "POST":
        try:
            id = request.form["id"]
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Employees SET name=?, email=?, address=? WHERE id=?", (name, email, address, id))
                con.commit()
                msg = "Employee successfully Updated"
        except:
            con.rollback()
            msg = "We can not update the employee to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()

if __name__ == "__main__":
    app.run(debug=True)