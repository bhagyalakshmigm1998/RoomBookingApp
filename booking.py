from flask import Flask, render_template, request
from os import path
import os.path
import sqlite3
if path.exists('booking_details.db')!=True:
    con = sqlite3.connect('booking_details.db')
    con.execute('CREATE TABLE Booking_details( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,email TEXT,phone INTEGER,date_booked DATE,guests INTEGER,rooms INTEGER)')

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "booking_details.db")

@app.route("/api/v1/home")
def home():
        return render_template('new_home.html')

#not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#bad request
@app.errorhandler(400)
def page_not_found(e):
    return render_template('400.html'), 404

@app.errorhandler(500)
def handle_500(e):
    return render_template("500.html"), 500

@app.route('/api/v1/new_booking')
def new_booking():
    return render_template("new_booking.html")

@app.route('/api/v1/add_details', methods=['GET','POST'])
def add_details():
    if request.method == 'POST':
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT COUNT(id) FROM Booking_details")
        count=len(cur.fetchall())
        if count<20:
            try:
                new_name = request.form["name"]
                new_email = request.form["email"]
                new_phone = request.form["phone"]
                new_date_booked = request.form["date_booked"]
                new_guests = request.form["guests"]
                new_rooms = request.form["rooms"]

                with sqlite3.connect(db_path) as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO Booking_details(name, email, phone, date_booked, guests, rooms) VALUES (?,?,?,?,?,?)",(new_name,new_email, new_phone, new_date_booked, new_guests, new_rooms))
                    con.commit()
                    msg = "Booking successful!"
            except:
                return "Issues with Booking"

            finally:
                return render_template('result.html')
        elif count==0:
            return render_template("no_bookings.html")
        else:
            return render_template("booking_full.html")

    else:
        return render_template('new_booking.html')

@app.route('/api/v1/no_bookings')
def no_booking():
    return render_template("no_bookings.html")

@app.route('/api/v1/view_booking', methods=["GET"])
def view_booking():
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if cur.execute("SELECT id FROM Booking_details") is None:
        return render_template("404.html")
    else:
        cur.execute("select * from Booking_details")
        rows = cur.fetchall()
        return render_template("view_bookings_new.html", rows=rows)

@app.route('/api/v1/delete_id',methods=["GET"])
def delete_id():
    return render_template("delete_id.html")

@app.route('/api/v1/delete_booking', methods=["GET","POST","DELETE"])
def delete_booking():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    if request.method == "POST":
      id = request.form["id"]
      cur.execute("SELECT id FROM Booking_details WHERE id = ?", id)
      data= cur.fetchone()
      if data is not None:
            id = request.form["id"]
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            cur.execute("DELETE FROM Booking_details where id = ?",id)
            con.commit()
               #del_id="DELETE FROM Booking_details WHERE id = ?"
               #if cur.execute("SELECT id FROM Booking_details WHERE id = ?", id) is True:
            return render_template("delete_booking.html")
      else:
          return render_template("400.html")
    else:
        return render_template("delete_id.html")


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port='5000')
