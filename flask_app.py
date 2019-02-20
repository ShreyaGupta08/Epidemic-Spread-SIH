from flask import Flask, jsonify, request, send_file
from flask_api import status
from flask_cors import CORS
import os
import requests
import datetime
import sqlite3


app = Flask(__name__)
CORS(app)


def make_connection():
    db_name = "epidemic.db"
    my_dir = os.path.dirname(__file__)
    db = os.path.join(my_dir, db_name)
    try:
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
    except Exception as e:
        print(e)
        print(f"Error connecting to the database")
        return False, False
    return con, cursor

def update_stats(values):
	
    #UPDATE STATS HERE
	con, cursor = make_connection()
    diseaseId = values[2]

    query = f"""
            SELECT * from Stats
            WHERE diseaseid = {diseaseID};
    """
    try:
        cursor.execute(query)
    except Exception as e:
        return_val = str(e) + "Error in executing query for updating stats"
    data = cursor.fetchone()
    if not data:
        query = """
                INSERT INTO Stats
                VALUES (?, ?, ?, ?);
                """
    else:
        query = f"""
                UPDATE Stats
                SET ncases = ncases + 1, ndeaths = ndeaths + {values[3]}
                WHERE diseaseid = {diseaseID};
                """
        values = False
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        con.commit()
    except Exception as e:
        return_val = str(e) + "Can't execute the query for " + type
    finally:
        con.close()
    con.close()
    return return_val    
			

def store_in_db(values, type = None):
    assert type , "type can't be null"
    return_val = "Done"
    con, cursor = make_connection()
    if type == 'hospital':
        query = """
                        INSERT INTO Hospital
                        VALUES(?, ?, ?, ?);
                """
    elif type == 'new_case':
        query = """
                        INSERT INTO Cases
                        VALUES(?, ?, ?);
                """
        update_stats(values)
    elif type == 'drug':
        drug_id = values[0]
        query = f"""
                        SELECT * FROM Drugs
                        WHERE drugid = {drug_id};
            """
        try:
            cursor.execute(query)
        except Exception as e:
            return_val = str(e) + "Error in executing query for drug"
        data = cursor.fetchone()
        if not data:
            query = """
                            INSERT INTO Drugs
                            VALUES (?, ?, ?, ?, ?);
                    """
        else:
            id, available = values[0], values[2]
            query = f"""
                            UPDATE Drugs
                            SET available = available + {available}
                            WHERE drugid = {id};
                    """
            values = False
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        con.commit()
    except Exception as e:
        return_val = str(e) + "Can't execute the query for " + type
    finally:
        con.close()
    con.close()
    return return_val


@app.route("/register_hospital/",methods=['GET'])
def store_hospital():
    #TODO: Generate user and hospital ID
    #TODO: A verify admin code here to verify if its the admin making the request or not
    columns = "id name location userid".split() #You can register multiple userIDs for a single hospital
    data_tuple = []
    for column in columns:
        val = request.args.get(column)
        data_tuple.append(val)
    return store_in_db(tuple(data_tuple), type='hospital')

@app.route("/new_case/",methods=['GET'])
def store_new_case():
    #TODO: Generate case_id
    columns = "date diseaseid death".split()
    data_tuple = []
    for column in columns:
        if column == 'date':
            data_tuple.append(str(datetime.datetime.now()))
            continue
        val = request.args.get(column)
        data_tuple.append(val)
    return store_in_db(tuple(data_tuple), type='new_case')

@app.route("/drug/", methods=['GET'])
def store_drug_data():
    columns = "drugid drugname drugreq available diseaseid".split()
    data_tuple = []
    for column in columns:
        val = request.args.get(column)
        data_tuple.append(val)
    return store_in_db(tuple(data_tuple), type='drug')

@app.route("/new_disease/",methods=['GET'])
def store_new_disease():
    columns = "id name meansofspread symptoms".split() #You can register multiple userIDs for a single hospital
    data_tuple = []
    for column in columns:
        val = request.args.get(column)
        data_tuple.append(val)
    return store_in_db(tuple(data_tuple), type='hospital')

if __name__ == '__main__':
   app.run(debug = True)
