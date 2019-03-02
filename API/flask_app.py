from flask import Flask, jsonify, request, send_file
from flask_api import status
from flask_cors import CORS
import os
import requests
import datetime
import sqlite3
import uuid
import pickle
from alert_data_handle import Alert

app = Flask(__name__)
CORS(app)


def district_to_location(district):
    my_dir = os.path.dirname(__file__)
    district_file = os.path.join(my_dir, "district.csv")
    with open(district_file) as handle:
        data = handle.readlines()
    for datum in data:
        datum = datum.split(",")
        if datum[0] == district:
            return float(datum[-2]), float(datum[-3])
def send_alert():
    #WRITE THISIHSISHISHSI THIS
    pass


def get_pharma_from_db(drugid):
    con, cursor = make_connection()
    query = f"""
            SELECT * from Pharmacy
        """
    amount = {}
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except Exception as e:
        print(f"Exception {e} in Pharmacy")
    finally:
        con.close()
    data = [dict(row) for row in rows]
    for datum in data:
        ids = datum['drugid'].split()
        print(type(ids))
        try:
            i = ids.index(drugid)
            try:
                inner_data = {
                                "avail" : int(datum['drugavail'].split()[i]),
                                "location" : datum['location'],
                                }
                amount[datum['id']] = inner_data
            except:
                inner_data = {
                                "avail" : datum['drugavail'].split()[i],
                                "location" : datum['location'],
                                }
                amount[datum['id']] = inner_data
        except:
            continue
        # if id in ids:
        #     farm_id.append(datum['id'])
        #     amount[id] = datum['drugavail'].split()
    return amount


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

def fetch_from_db(values, type = None):
    assert type , "type can not be None"
    con, cursor = make_connection()
    if type == "cases":
        diseaseid, days = values
        cur_date = datetime.datetime.now().date()
        ref_date = cur_date - datetime.timedelta(days=int(days))
        query = f"""
                SELECT * from Cases
                WHERE date > \"{ref_date}\" AND diseaseid = {diseaseid}
                """
    elif type == "stats":
        diseaseid = values[0]
        query = f"""
                SELECT * from Stats
                WHERE diseaseid = {diseaseid}
                """
    else:
        drugid, diseaseid = values
        if drugid and diseaseid:
            query = f"""
                    SELECT * from Drugs
                    WHERE drugid = {drugid} AND diseaseid = {diseaseid}
                    """
        else:
            query = f"""
                    SELECT * from Drugs
                    WHERE diseaseid = {diseaseid}
                    """
    print("\n\n", query)
    cursor.execute(query)
    try:
        cursor.execute(query)
    except Exception as e:
        return_val = str(e)
        con.close()
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    con.close()
    if data:
        return data
    else:
        return {}

def validate_login(values):
    userid = values[0]
    password = values[1]
    query = f"""
    				SELECT * FROM Login
    				WHERE id = {userid} and password = \"{password}\"
    		"""
    con, cursor = make_connection()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except Exception as e: #User doesn't exist
        con.close()
        return str(e)
    finally: #close connection in either case
        con.close()
    if rows:
        return_val = True
    else:
        return_val = False
    return str(return_val)

def update_stats(values, con, cursor):
    return_val = "Done"
    values = tuple(list(values)[:-1])
    diseaseid = values[1]
    new_values = [ diseaseid, 1, values[2] ]
    query = f"""
            SELECT * from Stats
            WHERE diseaseid = {diseaseid};
    """
    try:
        cursor.execute(query)
    except Exception as e:
        return_val = str(e) + "Error in executing query for updating stats"
    data = cursor.fetchone()
    if not data:
        query = """
                INSERT INTO Stats (diseaseid, ncases, ndeaths)
                VALUES (?, ?, ?);
                """
    else:
        query = f"""
                UPDATE Stats
                SET ncases = ncases + 1, ndeaths = ndeaths + {values[2]}
                WHERE diseaseid = {diseaseid};
                """
        new_values = False
    print(f"Doing query {query} and values {new_values}")
    try:
        if new_values:
            cursor.execute(query, new_values)
        else:
            cursor.execute(query)
        con.commit()
    except Exception as e:
        return_val = str(e) + "Can't execute the query."
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
                        INSERT INTO Cases(date, diseaseid, death, location)
                        VALUES(?, ?, ?, ?);
                """
        try:
            update_stats(values, con, cursor)
        except:
            print("hahahah")
            con.close()
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

@app.route("/", methods=['GET', 'POST'])
def home():
    return "SIH Epidemic shiz is working"

#STORING DATA IN DB
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
    columns = "date diseaseid death location".split()
    data_tuple = []
    for column in columns:
        if column == 'date':
            data_tuple.append(str(datetime.datetime.now().date()))
            continue
        val = request.args.get(column)
        data_tuple.append(val)
    store_in_db(tuple(data_tuple), type='new_case')
    alert = Alert()
    if alert.update(data_tuple[1], data_tuple[3]):
        alert.send_sms("Swine flu")
    return_val = f"Epidemic ID: {data_tuple[1]} stored in databse."
    return str(True)

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

@app.route("/login/", methods = ['GET'])
def store_new_login():
	columns = "id password".split()
	data_tuple = []
	for column in columns:
		val = request.args.get(column)
		data_tuple.append(val)
	return validate_login(data_tuple)

# FETCHING DATA
@app.route("/fetch_cases/", methods = ['GET', 'POST'])
def fetch_cases():
    columns = "diseaseid days".split()
    data_tuple = []
    for column in columns:
        val = request.args.get(column)
        data_tuple.append(val)
    return_data = fetch_from_db(data_tuple, type = 'cases')
    return jsonify(return_data)

@app.route("/fetch_stats/", methods = ['GET', 'POST'])
def fetch_stats():
    columns = "diseaseid".split()
    data_tuple = []
    for column in columns:
        val = request.args.get(column)
        data_tuple.append(val)
    return_data = fetch_from_db(data_tuple, type = 'stats')
    return jsonify(return_data)

@app.route('/genome_upload/', methods = ['POST'])
def upload_file():
    """
    This is to upload the FASTA sequence files. These are crowdsourced from
    research labs and or test labs
    """
    try:
        type = request.args.get("type") #Type can be DNA seq or protien seq
    except:
        type = "unknown"
    if request.method == 'POST':
      f = request.files['file']
      id = str(uuid.uuid4())
      f.save(str(type) + str(f.filename) + id)
      return 'file uploaded successfully'
    return False

@app.route("/fetch_drugs/", methods = ['GET', 'POST'])
def fetch_drugs():
    drugid, diseaseid = False, False
    if "diseaseid" in request.args:
        diseaseid = request.args.get("diseaseid")
    if "drugid" in request.args:
        drugid = request.args.get("drugid")
    data_tuple = [drugid, diseaseid]
    print("\n\nAAA", data_tuple)
    return_data = fetch_from_db(data_tuple, type = 'drugs')
    return jsonify(return_data)

@app.route("/similar_states/", methods = ['GET', 'POST'])
def similar_states():
    try:
        state = request.args.get("state")
    except:
        return False
    file_name = "final_list.txt"
    my_dir = os.path.dirname(__file__)
    cluster_file = os.path.join(my_dir, file_name)
    with open(cluster_file, "rb") as fp:
        list_final = pickle.load(fp)
    for i in list_final:
        if state in i:
            districts = i
    # if state == "Ujjain":
        # districts = ["Shivpuri", "Datia", "Gwalior"]
    answer = []
    for district in districts:
        answer.append(district_to_location(district))
    return jsonify({"similar" : answer})

@app.route("/get_pharma/", methods = ['GET', 'POST'])
def get_pharma():
    drugid = request.args.get("drugid")
    return_data = get_pharma_from_db(drugid)
    # print("nani")
    return jsonify(return_data)



if __name__ == '__main__':
   app.run(debug = True)
   #register_hospital
   # http://127.0.0.1:5000/new_case/?date=12-01-2019&diseaseid=20&death=1&location="123.423423 124.356345"
   # http://127.0.0.1:5000/fetch_cases/?days=30&diseaseid=10985
   # http://127.0.0.1:5000/fetch_stats/?diseaseid=10985
   # http://127.0.0.1:5000/login/?id=12&password=123
   # http://127.0.0.1:5000/similar_states/?state=Ujjain
   # http://127.0.0.1:5000/fetch_drugs/?diseaseid=1
   # http://127.0.0.1:5000/drug/?drugid=2&drugname=test&drugreq=12&available=12&diseaseid=1
   # http://127.0.0.1:5000/get_pharma/?drugid=502
