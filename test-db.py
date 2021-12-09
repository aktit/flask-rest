import mysql.connector
from flask import Flask, jsonify, make_response
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="test"
)

mycursor = mydb.cursor()


app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    mycursor.execute("select * from guests")
    myresult = mycursor.fetchall()
    rawdata = {}
    for i in range(len(myresult)):
        rawdata['id:'+ str(myresult[i][0])] = [str(myresult[i]).strip('()')]
    return jsonify(rawdata)

@app.route('/<id>', methods=['DELETE'])
def delete_info_byid(id):
    mycursor.execute(f"delete from guests where id={id}")
    mydb.commit()
    return make_response("",204)
app.run()
