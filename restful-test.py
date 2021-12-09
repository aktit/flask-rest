from flask import Flask, jsonify, Response
from flask_restful import reqparse, Api, Resource, abort
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.sql import select

meta = MetaData()

guests = Table(
   'guests', meta, 
   Column('id', Integer, primary_key = True, autoincrement=True), 
   Column('firstname', String), 
   Column('lastname', String), 
)
engine = create_engine('mysql+pymysql://root:123456@localhost/test')

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('arg1')
parser.add_argument('arg2')

class Todo(Resource):
    def delete(self, todo_id):
        cursor = guests.delete().where(guests.c.id == todo_id)
        with engine.connect() as conn:
            conn.execute(cursor)
        return Response(status=204)
    
    def put(self, todo_id):
        args = parser.parse_args()
        cursor = guests.update().where(guests.c.id==todo_id).values(firstname=args['arg1'], lastname=args['arg2'])
        with engine.connect() as conn:
            conn.execute(cursor)
        return Response(status=201)


    def post(self, todo_id='post'):
        args = parser.parse_args()
        cursor = guests.insert().values(firstname=args['arg1'], lastname=args['arg2'])
        with engine.connect() as conn:
            conn.execute(cursor)
        return Response(status=201)

    def get(self, todo_id='all'):
        cursor = select(guests.c.id)
        with engine.connect() as conn:
            a = conn.execute(cursor)
        data = a.fetchall()
        newdata = []
        gooddata = []
        for i in data:
            newdata.append(str(i).strip('()'))
        for j in newdata:
            gooddata.append(str(j).strip(','))

        if todo_id == 'all':
            rawdata = {}
            cursor = guests.select()
            with engine.connect() as conn:
                result = conn.execute(cursor)
            data = result.fetchall()
            for i in range(len(data)):
                rawdata[data[i][0]] = data[i][1], data[i][2]
            return jsonify(rawdata)
        elif str(todo_id) not in gooddata:
            return abort(404, message = f"ID {todo_id} does'nt exist")

        else:
            rawdata = {}
            cursor = guests.select().where(guests.c.id == {todo_id})
            with engine.connect() as conn:
                result = conn.execute(cursor)
            data = result.fetchall()
            rawdata[data[0][0]] = data[0][1], data[0][2]
            return jsonify(rawdata)
       
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)

#Example
#curl http://localhost:5000/todos/all
#curl http://localhost:5000/todos/post -d "arg1=another" -d "arg2=game" -X POST
#requests.post("http://localhost:5000/todos/post", data={'arg1' : 'hello', 'arg2' : 'world'})