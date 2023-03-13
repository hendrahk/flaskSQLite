from flask import Flask,redirect, url_for, render_template, request
import sqlite3 as sql

app = Flask(__name__)

con = sql.connect('database.db')
print('Opened db sucessfully')
con.execute('CREATE TABLE IF NOT EXISTS siswa(nama TEXT, alamat TEXT, nohp TEXT)')
print('tabel sudah dibuat nih')
# con.close()

@app.route('/')
def index():
    return redirect(url_for('list'))

@app.route('/enternew')
def enternew():
    return render_template('insert.html')

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    msg = ""
    if request.method == 'POST':
        try:
            nama = request.form['nama']
            alamat = request.form['alamat']
            nohp = request.form['nohp']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                query = f"INSERT INTO siswa VALUES('{nama}', '{alamat}', '{nohp}')"
                cur.execute(query)
                con.commit()
                msg = "record success"
        except:
            con.rollback()
            msg = "error insert"
        finally:
            return render_template('result.html', msg=msg)


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row #he line of code assigning sqlite3.Row to the row_factory of connection creates what some people call a 'dictionary cursor', - instead of tuples it starts returning 'dictionary' rows after fetchall or fetchone.

    cur = con.cursor() #The sqlite3.Cursor class is an instance using which you can invoke methods that execute SQLite statements, fetch data from the result sets of the queries.
    query = "select * from siswa"
    cur.execute(query)

    rows = cur.fetchall(); # fetches all the rows of a query result. It returns all the rows as a list of tuples. An empty list is returned if there is no record to fetch.
    return render_template("list.html", rows=rows)

if __name__ == '__main__':
    app.run(port=1111)