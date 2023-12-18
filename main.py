from flask import Flask, request, jsonify
import sqlite3
import hashlib
import json
from encryption import decrypt_message, fetchPubKey
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#----------------------TESTING AREA


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

  cursor.execute("SELECT username FROM Register WHERE udid=?", (device_id))

  result = cursor.fetchone()
  conn.close()

  username = result[0]

  token = generate_token(device_id, username)

  return jsonify({'token': token})


@app.route('/', methods=['GET'])
def my_route():
  print('hi')
  return 'HunianKu'


# Register a user
@app.route('/users', methods=['POST'])
def register_user():
  # request = [udid, username, password]
  data = request.get_json()

  # token = data.get('token')
  udid = data.get('udid')
  username = data.get('username')
  password = data.get('password')
  phone = data.get('phone')
  email = data.get('email')

  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM Register WHERE username=?", (username, ))
  existing_user = cursor.fetchone()

  if existing_user:
    conn.close()
    return jsonify({
        'message':
        'Username already exists. Please choose a different username.'
    }), 400

  # If the username doesn't exist for the given udid, insert the new record
  else:
    cursor.execute(
        "INSERT INTO Register (udid, username, password, phone, email) VALUES (?, ?, ?, ?, ?)",
        (udid, username, password, phone, email))

    conn.commit()

    conn.close()

    return jsonify({'message': 'User registered successfully'})


@app.route('/users', methods=['GET'])
def get_all_users():
  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM Register")
  users_data = cursor.fetchall()

  conn.close()

  users_list = []
  for user_data in users_data:
    user_dict = {
        'udid': user_data[0],
        'username': user_data[1],
        'password': user_data[2],
        'phone': user_data[3],
        'email': user_data[4]
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
  encryptedPassword = data['encryptedPassword']
  encryptedUsername = data['encryptedUsername']
  udid = data['udid']

  print(encryptedPassword)

  decryptedPassword = decrypt_message(encryptedPassword)
  decryptedUsername = decrypt_message(encryptedUsername)
  print(udid)
  print(decryptedPassword)
  print(decryptedUsername)

  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  input_udid = udid
  input_password = decryptedPassword
  input_username = decryptedUsername

  cursor.execute("SELECT * FROM Register WHERE password=? AND username=?",
                 (input_password, input_username))

  result = cursor.fetchone()
  conn.close()

  if result:
    print("Correct password for the given udid.")
    return jsonify({'status': 'success'})
  else:
    print("Incorrect password, username or udid not found.")
    return jsonify({'status': 'failed'}), 400


@app.route('/pubkey', methods=['GET'])
def pubKey():
  key = fetchPubKey()
  return jsonify({'publicKey': key})


@app.route('/property', methods=['POST'])
def add_property():
  # request = [udid, username, password]
  data = request.get_json()

  # token = data.get('token')
  udid = data.get('udid')
  action = data.get('action')
  type = data.get('type')
  lokasi = data.get('lokasi')
  harga = data.get('harga')
  area = data.get('area')
  kTidur = data.get('kTidur')
  kMandi = data.get('kMandi')
  kMandiKos = data.get('kMandiKos')
  tipeKost = data.get('tipeKost')
  ketinggian = data.get('ketinggian')
  sewa = data.get('sewa')
  image = data.get('image')
  date = data.get('date')
  status = data.get('status')
  desc = data.get('deskripsi')

  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  cursor.execute(
      "INSERT INTO properties (udid, action, status, type, lokasi, harga, area, kTidur, kMandi,kMandiKos, tipeKost, ketinggian, sewa, image, date, status, desc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)",
      (udid, action, status, type, lokasi, harga, area, kTidur, kMandi,
       kMandiKos, tipeKost, ketinggian, sewa, image, date, status,desc))

  conn.commit()

  conn.close()

  return jsonify({'message': 'Post created successfully'})


@app.route('/properties', methods=['GET'])
def get_all_beli_rumah():
  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM properties")
  datas = cursor.fetchall()

  conn.close()

  data_list = []
  for data in datas:
    data_dict = {
        'id': data[0],
        'udid': data[1],
        'action': data[2],
        'type': data[3],
        'lokasi': data[4],
        'harga': data[5],
        'area': data[6],
        'kTidur': data[7],
        'kMandi': data[8],
        'kMandiKos': data[9],
        'tipeKost': data[10],
        'ketinggian': data[11],
        'sewa': data[12],
        'image': data[13],
        'date': data[14],
        'status': data[15],
        'desc': data[16]
    }
    data_list.append(data_dict)

  return jsonify({'property': data_list})


# Filter


@app.route('/filter', methods=['POST'])
def filter_property():
  # request = [udid, username, password]
  data = request.get_json()
  print(data)

  ### Get all data
  udid = data.get('udid')
  action = data.get('action')
  type = data.get('type')
  lokasi = data.get('lokasi')
  harga1 = data.get('harga1')
  area1 = data.get('area1')
  harga2 = data.get('harga2')
  area2 = data.get('area2')
  kTidur = data.get('kTidur')
  kMandi = data.get('kMandi')
  kMandiKos = data.get('kMandiKos')
  tipeKost = data.get('tipeKost')
  ketinggian = data.get('ketinggian')
  sewa = data.get('sewa')
  image = data.get('image')
  date = data.get('date')
  status = data.get('status')

  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  ##Beli Komersial
  if action == 'Beli' and type == 'Komersial':
    print('masuk paeko')
    cursor.execute(
        "SELECT * FROM properties WHERE status='Ready' AND action ='Jual' AND type='Komersial' AND lokasi=? AND harga >= ? AND harga <= ? AND area >= ? AND area <=? AND kTidur=? AND kMandi=? ",
        (lokasi, harga1, harga2, area1, area2, kTidur, kMandi))

  ##Beli Rumah
  elif action == 'Beli' and type == 'Rumah':
    print("tes")
    cursor.execute(
        "SELECT * FROM properties WHERE status='Ready' AND action ='Jual' AND type='Rumah' AND lokasi=? AND harga >= ? AND harga <= ? AND area >= ? AND area <=? AND kTidur=? AND kMandi=? ",
        (lokasi, harga1, harga2, area1, area2, kTidur, kMandi))

  ##Beli Apartement
  elif action == 'Beli' and type == 'Apartement':
    cursor.execute(
        "SELECT * FROM properties WHERE status='Ready' AND action ='Jual' AND type='Apartement' AND lokasi=? AND harga >= ? AND harga <= ? AND area >= ? AND area <=? AND kTidur=? AND kMandi=? ",
        (lokasi, harga1, harga2, area1, area2, kTidur, kMandi))

  ##Beli Tanah
  elif action == 'Beli' and type == 'Tanah':
    cursor.execute(
        "SELECT * FROM properties WHERE status='Ready' AND action ='Jual' AND type='Tanah' AND lokasi=? AND harga >= ? AND harga <= ? AND area >= ? AND area <=? AND ketinggian=? ",
        (lokasi, harga1, harga2, area1, area2, ketinggian))

  ##Beli Kost
  elif action == 'Beli' and type == 'Kost':
    cursor.execute(
        "SELECT * FROM properties WHERE status='Ready' AND action ='Jual' AND type='Kost' AND lokasi=? AND harga >= ? AND harga <= ? AND area >= ? AND area <=? AND kMandiKos=? AND tipeKost=? AND kTidur=? AND kMandi=? ",
        (lokasi, harga1, harga2, area1, area2, kMandiKos, tipeKost, kTidur,
         kMandi))

  ##Sewa Komersial
  elif action == 'Sewa' and type == 'Komersial':
    print('masuk paeko')
    cursor.execute(
        "SELECT * FROM properties WHERE status='Ready' AND action ='Sewa' AND type='Komersial' AND lokasi=? AND harga >= ? AND harga <= ? AND area >= ? AND area <=? AND kTidur=? AND kMandi=? AND sewa=?",
        (lokasi, harga1, harga2, area1, area2, kTidur, kMandi,sewa))

  ##Sewa Rumah
  elif action == 'Sewa' and type == 'Rumah':
    print("tes")
    cursor.execute(
        "SELECT * FROM properties WHERE status='Ready' AND action ='Sewa' AND type='Rumah' AND lokasi=? AND harga >= ? AND harga <= ? AND area >= ? AND area <=? AND kTidur=? AND kMandi=? AND sewa=?",
        (lokasi, harga1, harga2, area1, area2, kTidur, kMandi,sewa))

  ##Sewa Apartement
  elif action == 'Sewa' and type == 'Apartement':
    cursor.execute(
        "SELECT * FROM properties WHERE status='Ready' AND action ='Sewa' AND type='Apartement' AND lokasi=? AND harga >= ? AND harga <= ? AND area >= ? AND area <=? AND kTidur=? AND kMandi=? AND sewa=?",
        (lokasi, harga1, harga2, area1, area2, kTidur, kMandi,sewa))

  ##Sewa Tanah
  elif action == 'Sewa' and type == 'Tanah':
    cursor.execute(
        "SELECT * FROM properties WHERE status='Ready' AND action ='Sewa' AND type='Tanah' AND lokasi=? AND harga >= ? AND harga <= ? AND area >= ? AND area <=? AND ketinggian=? AND sewa=?",
        (lokasi, harga1, harga2, area1, area2, ketinggian, sewa))

  ##Sewa Kost
  elif action == 'Sewa' and type == 'Kost':
    cursor.execute(
        "SELECT * FROM properties WHERE status='Ready' AND action ='Sewa' AND type='Kost' AND lokasi=? AND harga >= ? AND harga <= ? AND area >= ? AND area <=? AND kMandiKos=? AND tipeKost=? AND kTidur=? AND kMandi=? AND sewa=?",
        (lokasi, harga1, harga2, area1, area2, kMandiKos, tipeKost, kTidur, kMandi, sewa))


  #Assign the data
  filteredData = cursor.fetchall()
  print(filteredData)

  conn.commit()

  conn.close()
  return jsonify(filteredData), 200




@app.route('/myListing', methods=['POST'])
def myListing():
  data = request.get_json()

  udid = data.get('udid')

  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  cursor.execute(
        "SELECT * FROM properties WHERE udid=?", (udid,))

  myListingData = cursor.fetchall()

  conn.commit()

  conn.close()
  return jsonify(myListingData), 200




@app.route('/postForum', methods=['POST'])
def add_post_forum():
  # request = [udid, username, password]
  data = request.get_json()

  # token = data.get('token')
  udid = data.get('udid')
  # username = data.get('username')
  caption = data.get('caption')
  # image = data.get('image')
  # komen = data.get('komen')
  date = data.get('date')
  image = data.get('image')

  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  cursor.execute("SELECT username FROM Register WHERE udid = ?", (udid,))
  result = cursor.fetchone()

  if result:
    username = result[0]

    # Insert post into the Forum table with the retrieved username
    cursor.execute("INSERT INTO Forum (udid, username, caption, date, image) VALUES (?, ?, ?, ?, ?)",
                   (udid, username, caption, date, image))

    conn.commit()
    conn.close()
    return jsonify({'message': 'Post created successfully'})
  else:
    conn.close()
    return jsonify({'error': 'User not found for the provided udid'}), 404

  # cursor.execute(
  #       "INSERT INTO post_Forum (udid, username, caption, komen, date) VALUES (?, ?, ?, ?, ?)",
  #       (udid, username, caption, komen, date)
  #   )

  # cursor.execute("INSERT INTO Forum (udid, caption, date) VALUES (?, ?, ?)",
  #                (udid, caption, date))

  # conn.commit()
  # conn.close()
  # return jsonify({'message': 'Post created successfully'})


@app.route('/postForum', methods=['GET'])
def get_all_post_forum():
  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM Forum")
  datas = cursor.fetchall()

  conn.close()

  data_list = []
  for data in datas:
    data_dict = {
        'id': data[0],
        'udid': data[1],
        'username': data[2],
        'caption': data[3],
        # 'komen': data[4],
        'date': data[5],
        'image': data[6]
    }
    data_list.insert(0, data_dict)

  return jsonify({'Forum': data_list})

@app.route('/postKomen', methods=['GET'])
def get_post_komen():
  data = request.get_json()
  komen = data.get('komen')

  conn = sqlite3.connect('userdb.db')
  cursor = conn.cursor()
  cursor.execute("INSERT komen FROM Forum WHERE id = ?", (id,))

  conn.commit()  
  conn.close()
  return jsonify({'message': 'Post Komen successfully'})

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=9000)
