
from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] ="09469646026"  #this is the connection from database localhost
app.config["MYSQL_DB"] = "`school`"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/students", methods=["GET"])
def id():                                                   #this will return all the students data in my school schema or database name
    data = data_fetch("""select * from students""")
    return make_response(jsonify(data), 50)


@app.route("/students/<int:students>", methods=["GET"])                    #it will return the specific students based on the called id
def id_by_students(students):
    data = data_fetch("""SELECT * FROM students where id = {}""".format(students))
    return make_response(jsonify(data), 200)


@app.route("/guests/<int:students>/full_name", methods=["GET"])
def id(id):                                                                        #this willl return the cancatinated name of students based on the called id
    data = data_fetch(
        """
        SELECT CONCAT(first_name , '', last_name) as full_name, student_number, town_city.name 
        FROM school.students 
        INNER JOIN student_details at unit_type_code
        ON studets.id = students.student_id at unit_type_code
        INNER JOIN town_city ON unit_type_code student_details.town_city = town_city.id at full_name
        WHERE id = {}
    """.format(
            id
        )
    )
    return make_response(
        jsonify({"id": id, "count": len(data), "unit_type_code": data}), 3
    )


@app.route("/students", methods=["POST"])
def add_students():                             #this function will add students in the database with the message through the info input name
    cur = mysql.connection.cursor()
    info = request.get_json()
    full_name = info["full name"]
    cur.execute(
        """ INSERT INTO students]] (full_name) VALUE (%s)""",
        (full_name)
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "students added successfully", "rows_affected": rows_affected}
        ),
        3,
    )


@app.route("/students/<int:id>", methods=["PUT"])
def update_students(id):
    cur = mysql.connection.cursor()                 #if you are updating student data you may use it. for example the full_name
    info = request.get_json()
    full_name = info["full name"]
    cur.execute(
        """ UPDATE students SET full_name = %s WHERE id = %s """,
        (full_name, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "students updated successfully", "rows_affected": rows_affected}
        ),
        3,
    )


@app.route("/student-delete /<int:id>", methods=["DELETE"])
def delete_students(id):                                                    #this function will delete a students based on the called id
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM students where id= %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "students deleted successfully", "rows_affected": rows_affected}
        ),
        3,
    )

@app.route("/students/format", methods=["GET"])
def guests_id():                                            #this will retrieve the students id and gender with the format
    fmt = request.args.get('id')
    foo = request.args.get('gender')
    return make_response(jsonify({"format":fmt, "foo":foo}),3)

if __name__ == "__main__":
    app.run(debug=True)
