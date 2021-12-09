from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from flask import Flask, jsonify, make_response

meta = MetaData()

guests = Table(
   'guests', meta, 
   Column('id', Integer, primary_key = True, autoincrement=True), 
   Column('firstname', String), 
   Column('lastname', String), 
)
engine = create_engine('mysql+pymysql://root:123456@localhost/test')

app = Flask(__name__)   
@app.route('/', methods=['GET'])
def index():
    rawdata = {}
    cursor = guests.select()
    with engine.connect() as conn:
        result = conn.execute(cursor)
    data = result.fetchall()
    for i in range(len(data)):
        rawdata[data[i][0]] = data[i][1], data[i][2]

    return jsonify(rawdata)

@app.route('/delete/<id>', methods=['DELETE'])
def delete_info_byid(id):
    cursor = guests.delete().where(guests.c.id == id)
    with engine.connect() as conn:
        conn.execute(cursor)
    return make_response("",204)

@app.route('/post/<firstname>,<lastname>', methods=['POST'])
def post_data(firstname, lastname):
    cursor = guests.insert().values(firstname=f"{firstname}", lastname=f"{lastname}")
    with engine.connect() as conn:
        conn.execute(cursor)
    return make_response("",201)

@app.route('/put/<id>,<firstname>,<lastname>', methods=['PUT'])
def put_data(id, firstname, lastname):
    cursor = guests.update().where(guests.c.id=={id}).values(firstname={firstname}, lastname={lastname})
    with engine.connect() as conn:
        conn.execute(cursor)
    return make_response("",200)

app.run()