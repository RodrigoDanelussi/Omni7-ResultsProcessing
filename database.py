import pymysql
from header import Continuous, Discrete

db = pymysql.connect(host="pede.zapto.org", user="superuser", password="superpass", db="gpsomni", port=3306)

def Get_Contiuos_Data(road, direction):
    try:
        cursor = db.cursor()
        query = f"SELECT frame, type, subType, latitude, longitude, altitude FROM data d JOIN session s on d.session_id = s.id WHERE s.user_id NOT LIKE '9%' AND road = {road} AND direction = '{direction}' AND module = 'Continuous' AND isDeleted = 0;"
        cursor.execute(query)

        data = cursor.fetchall()

        dados = []
        for row in data:
            d = Continuous()
            d.frame = int(row[0])
            d.type = row[1]
            d.subType = row[2]
            dados.append(d)

        return dados
    except:
        print('Error Mysql Get_GPS_Route_Database')

def Get_Types(module):
    try:
        cursor = db.cursor()
        query = f"Select type from type where module = '{module}' AND isDeleted = 0 ORDER BY type;"
        cursor.execute(query)

        data = cursor.fetchall()

        dados = []
        for row in data:
            dados.append(row[0])

        return dados
    except:
        print('Error Mysql Get_GPS_Route_Database')

def Get_Discrete_Data(road, direction):
    try:
        cursor = db.cursor()
        query = f"SELECT frame, type, subType, complement1, complement2, latitude, longitude, altitude, originFrameName FROM data d JOIN session s on d.session_id = s.id WHERE s.user_id NOT LIKE '9%' AND road = {road} AND direction = '{direction}' AND module = 'Discrete' AND isDeleted = 0 ORDER BY type, frame;"
        cursor.execute(query)

        data = cursor.fetchall()

        dados = []
        for row in data:
            print(row[0])
            d = Discrete()
            d.frame = int(row[0])
            d.type = row[1]
            d.subType = row[2]
            d.complement1 = row[3]
            d.complement2 = row[4]
            d.latitude = row[5]
            d.longitude = row[6]
            d.altitude = row[7]
            d.image = row[8]
            dados.append(d)

        return dados
    except:
        print('Error Mysql Get_GPS_Route_Database')