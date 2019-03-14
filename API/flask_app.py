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
import json
import pickle
import pandas as pd



app = Flask(__name__)
CORS(app)

def distancefunc(i,j,data):
    dist = 0
    for k in range(1,8):
        dist = dist + abs(data.iloc[i][k]-data.iloc[j][k])
    match = 0
    b = []
    return dist
data = pd.read_csv('new_clustering.csv')
data.head()


# In[21]:


def ret_cluster_list(name):
    data = pd.read_csv('new_clustering.csv')
    for i in range(0,50):
#     print(data.iloc[i][2])
        data.iloc[i,2] = data.iloc[i,2][:-1]
        data.iloc[i,2] = float(data.iloc[i,2])
    index = {}
    for i in range(0,50):
        index[data.iloc[i][0]] = i
    with open("final_list.txt", "rb") as fp:
        list_final = pickle.load(fp)
    l = []
    for i in list_final:
        if name in i:
            l=i
            break
    dist = []
    for k in l:
        dist.append((distancefunc(index[name],index[k],data),k))
    dist.sort()
    color = {}
    c = '#ffff99'
    for i in range(0,len(dist)):
        if len(dist)-i<=4:
            c = '#ff8000'
        if len(dist)-i<=2:
            c = '#cccc00'
        color[dist[i][1]] = c
    return color

def get_pharmacies(diseaseid):
    vals = fetch_from_db([False, diseaseid], type = 'drugs')
    try:
        drugid =  vals[0]['drugid']
    except:
        drugid = -1
    return get_pharma_from_db(str(drugid))


def get_predicted_districts(diseaseid):
    my_dir = os.path.dirname(__file__)
    dicts = []
    correlated_file = os.path.join(my_dir, "correlated.json")
    with open(correlated_file) as handle:
        json_data = json.loads(handle.read())
    try:
        districts = json_data[diseaseid]
    except:
        districts = []
    if districts:
        final_keys = []
        final_vals = []
        answer = []
        for district in districts:
            dicts.append(ret_cluster_list(district))
        for d in dicts:
            for key in d:
                f1, f2 = district_to_location(key)
                string = str(f1) + " " + str(f2)
                final_keys.append(string)
                final_vals.append(d[key])
        for fk, fv in zip(final_keys, final_vals):
            answer.append(str(fk) + " " + str(fv))
        # answer = []
        # for d in ds:
        #     answer.append(district_to_location(d))
    else:
        answer = ""
    # for k in answer:
    #     temp = ""
    #     for l in k:
    #         temp += str(l)
    #         temp += " "
    #     final_answer.append(temp[:-1])
    return answer


def district_to_location(district):
    my_dir = os.path.dirname(__file__)
    district_file = os.path.join(my_dir, "district.csv")
    with open(district_file) as handle:
        data = handle.readlines()
    for datum in data:
        datum = datum.split(",")
        if datum[0] == district:
            return float(datum[-2]), float(datum[-3])
    return False

def to_name(diseaseid):
    con, cursor = make_connection()
    query = f"""
            SELECT * from Diseases
            where id = {diseaseid}
        """
    cursor.execute(query)
    try:
        data = cursor.fetchone()
    except Exception as e:
        print(f"Exception {e} in Pharmacy")
    finally:
        con.close()
    return data[1]

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
    index = 0
    for datum in data:
        ids = datum['drugid'].split()
        try:
            i = ids.index(drugid)
            try:
                inner_data = {
                                "avail" : int(datum['drugavail'].split()[i]),
                                "location" : datum['location'],
                                }
                amount[index+1] = inner_data
            except:
                inner_data = {
                                "avail" : datum['drugavail'].split()[i],
                                "location" : datum['location'],
                                }
                amount[index+1] = inner_data
            index += 1
        except:
            continue
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
    # print("\n\n", query)
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
    # print(f"Doing query {qfuery} and values {new_values}")
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
            print("nani da fak")
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
                            VALUES (?, ?, ?, ?);
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
        elif column == 'location':
            val = request.args.get(column)
            data_tuple.append(val.replace("\"",""))
            continue
        val = request.args.get(column)
        data_tuple.append(val)
    store_in_db(tuple(data_tuple), type='new_case')
    alert = Alert()
    alert.time_prediction(data_tuple[1])
    diseaseid, location = data_tuple[1], data_tuple[3]
    if alert.update(diseaseid, location):
        alert.correlated(diseaseid, location)
        dname = to_name(diseaseid)
        alert.send_sms(dname)
        alert.post_twitter(dname, location)
    return_val = f"Epidemic ID: {data_tuple[1]} stored in databse."
    return str(True)

@app.route("/new_drug/", methods=['GET'])
def store_drug_data():
    columns = "drugid drugname drugreq diseaseid".split()
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
    return_data = {}
    return_data['cases'] = fetch_from_db(data_tuple, type = 'cases')
    return_data["predicted_districts"] = get_predicted_districts(data_tuple[0])
    return_data["pharmacies"] = get_pharmacies(data_tuple[0])
    return jsonify(return_data)

@app.route("/fetch_only_cases/", methods = ['GET', 'POST'])
def fetch_only_cases():
    columns = "diseaseid days".split()
    data_tuple = []
    for column in columns:
        val = request.args.get(column)
        data_tuple.append(val)
    return_data = {}
    data = fetch_from_db(data_tuple, type = 'cases')
    final_case_data, final_death_data = {}, {}
    for row in data:
        date = row['date']
        try:
            final_case_data[date] += 1
        except:
            final_case_data[date] = 1
        try:
            final_death_data[date] += 1
        except:
            final_death_data[date] = 1
        final_cases_array = []
        final_death_array = []
        for key in final_case_data:
            string = str(key) + " " + str(final_case_data[key])
            final_cases_array.append(string)
        for key in final_death_data:
            string = str(key) + " " + str(final_death_data[key])
            final_death_array.append(string)
    return jsonify({"cases":final_cases_array, "deaths":final_death_array})

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

@app.route("/get_ratio/", methods = ['GET', 'POST'])
def get_ratio():
    con, cursor = make_connection()
    query = """
            select * from Stats
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
    except Exception as e:
        return_val = str(e)
    finally:
        con.close()
    final_data = []
    for datum in data:
        value = int(datum['ndeaths']) / int(datum['ncases'])
        id = datum['diseaseid']
        string = str(value) + " " + str(id)
        final_data.append(string)
    return jsonify(final_data)

if __name__ == '__main__':
   # app.run(debug = True)
   # sudo python -m smtpd -c DebuggingServer -n localhost:1025
   app.run(host="127.0.0.1", port=5000)
   # https://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=7
   # register_hospital
   # https://07b92f1b.ngrok.io/new_case/?date=2019-03-03&diseaseid=4&death=1&location="26 78"
   # https://07b92f1b.ngrok.io/new_case/?date=2019-03-03&diseaseid=4&death=1&location=%2225.6577%2078.45%22
   # http://127.0.0.1:5000/new_case/?date=2019-03-03&diseaseid=2&death=1&location="25.6577 78.45"
   # http://127.0.0.1:5000/fetch_cases/?days=30&diseaseid=10
   # http://127.0.0.1:5000/fetch_only_cases/?days=30&diseaseid=10
   # http://127.0.0.1:5000/fetch_stats/?diseaseid=10
   # http://127.0.0.1:5000/login/?id=12&password=123
   # http://127.0.0.1:5000/fetch_drugs/?diseaseid=1
   # http://127.0.0.1:5000/new_drug/?drugid=2&drugname=test&drugreq=12&diseaseid=10
   # http://127.0.0.1:5000/get_pharma/?drugid=502
   # http://127.0.0.1:5000/get_ratio/
