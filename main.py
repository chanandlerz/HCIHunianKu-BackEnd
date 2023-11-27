from flask import Flask, request, jsonify
import sqlite3
import hashlib
import json
from encryption import decrypt_message, fetchPubKey
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

#----------------------TESTTING AREA


@app.route("/tes", methods=["POST"])
def getMe():
  data = json.loads(request.data)
  print(data[0])
  return data[0] + " halo"


#------------------END TESTINGA REA
# Database
# @app.route('/generate_token', methods=['GET'])
def generate_token(device_id, username):
  data = request.get_json()
  device_id = data.get('device_id')
  username = data.get('username')

  combined_str = f"{device_id}-{username}"
  hashed_token = hashlib.sha256(combined_str.encode()).hexdigest()
  return jsonify({'token': hashed_token})


@app.route('/generate_token', methods=['POST'])
def generate_post_token():
  data = request.get_json()
  device_id = data.get('udid')

  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  cursor.execute("SELECT username FROM users WHERE udid=?", (device_id))

  result = cursor.fetchone()
  conn.close()

  username = result[0]

  token = generate_token(device_id, username)

  return jsonify({'token' : token})


@app.route('/', methods=['GET'])
def my_route():
  print('hi')
  return 'HunianKu'


@app.route('/users', methods=['POST'])
def register_user():
  # request = [udid, username, password]
  data = request.get_json()

  # token = data.get('token')
  udid = data.get('udid')
  username = data.get('username')
  password = data.get('password')

  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  cursor.execute(
      "INSERT INTO users (udid, username, password) VALUES (?, ?, ?)",
      (udid, username, password))

  conn.commit()

  conn.close()

  return jsonify({'message': 'User registered successfully'})


@app.route('/users', methods=['GET'])
def get_all_users():
  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM users")
  users_data = cursor.fetchall()

  conn.close()

  users_list = []
  for user_data in users_data:
    user_dict = {
        'udid': user_data[0],
        'username': user_data[1],
        'password': user_data[2]
    }
    users_list.append(user_dict)

  return jsonify({'users': users_list})


# @app.errorhandler(Exception)
# def handle_error(e):
#     print(str(e))
#     return jsonify(error=str(e)), 500


@app.route('/verify', methods=['POST'])
#request = Map<udid, encrypted password>
def verifyUser():
  #data = request.data
  data = json.loads(request.data)
  # print(data)
  # print(type(data))
  encryptedData = data['encryptedData']
  udid = data['udid']

  print(encryptedData)

  decryptedData = decrypt_message(encryptedData)
  print(udid)
  print(decryptedData)

  #nanti kan udah ada decryptednya trs assign ke variabel
  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  input_udid = udid
  input_password = decryptedData

  cursor.execute("SELECT * FROM users WHERE udid=? AND password=?",
                 (input_udid, input_password))

  result = cursor.fetchone()
  conn.close()

  if result:
    print("Correct password for the given udid.")
    return jsonify({'status': 'success'})
  else:
    print("Incorrect password or udid not found.")
    return jsonify({'status': 'failed'})



@app.route('/pubkey', methods=['GET'])
def pubKey():
  key = fetchPubKey()
  return jsonify({'publicKey': key})



if __name__ == '__main__':
  app.run(host="0.0.0.0", port=9000)
