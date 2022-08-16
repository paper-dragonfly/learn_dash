from flask import Flask, request
import psycopg2 #postgreSQL adaptor for python
import json 
from pydantic import ValidationError
from dash_pets.post_classes import AddPet
import pdb

def db_connect2(): 
    params = {'host': 'localhost', 'database': 'sandbox', 'user': 'katcha'}
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    return conn, cur


app = Flask(__name__)

@app.route('/petinfo', methods=['GET'])
def petinfo():
    try:
        conn, cur = db_connect2()
        cur.execute('SELECT * FROM pets')
        pets_table = cur.fetchall()
        # print(pets_table)
    finally:
        cur.close()
        conn.close()
        return json.dumps({'pets_table' :pets_table})

@app.route('/addpet', methods = ['POST'])
def addpet():
    m = 'Fail'
    try:
        conn, cur = db_connect2()
        new_pet_info = AddPet.parse_obj(request.get_json())
        subs = (new_pet_info.pet_name, new_pet_info.pet_type, new_pet_info.pet_age, new_pet_info.pet_owner)
        cur.execute("INSERT INTO pets(pet_name, type, age, owner_name) VALUES(%s,%s,%s,%s)", subs)
        conn.commit()
        m = 'pet added' 
    except ValidationError() as e:
        return json.dumps({'status_code': 400, 'message': e})    
    finally:
        cur.close()
        conn.close()
        return json.dumps({'status_code': 200, 'message': m})


if __name__ == '__main__':
    app.run(debug=True, host = "localhost", port=8050)




