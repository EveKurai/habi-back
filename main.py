from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import connection as conn
import json
import collections
main = Flask(__name__)

query="SELECT p.city, p.description, p.price, p.address, p.year, s.name  FROM status_history AS sh INNER JOIN property AS p ON sh.property_id=p.id INNER JOIN status AS s ON sh.status_id=s.id "

queryCities="SELECT p.city FROM status_history AS sh INNER JOIN property AS p ON sh.property_id=p.id INNER JOIN status AS s ON sh.status_id=s.id "

queryYear="SELECT p.year FROM status_history AS sh INNER JOIN property AS p ON sh.property_id=p.id INNER JOIN status AS s ON sh.status_id=s.id "

CORS(main)


@main.route('/properties/filters/', methods=['POST'])
def get_properties():    
    filters = request.json
    filterValue = filters.values()
    filterKey = filters.keys()
    listFilterKey = list(filterKey) 
    listFilterValue = list(filterValue)
    if len(filterValue)>0:
        querySTR = "WHERE "
        p = ""
        for i in range(len(listFilterValue)):
            if listFilterKey[i]=="status":
                p="s."
                listFilterKey[i]="name"
            else:
                p="p."
            querySTR+=p+str(listFilterKey[i])+"= '"+str(listFilterValue[i])+"' AND "
    
        where = (querySTR).rstrip("AND ")
        querySQL=query+where        
    else:
        querySQL=query
    conn.cursor.execute(querySQL)
    propertiesF = conn.cursor.fetchall()
    
    objects_list = []
    for row in propertiesF:
        d = collections.OrderedDict()
        d["city"] = row[0]
        d["description"] = row[1]
        d["price"] = row[2]
        d["address"] = row[3]
        d["year"] = row[4]
        d["status"] = row[5]
        objects_list.append(d)
    p = json.dumps(objects_list)

    return p


@main.route('/properties/cities/', methods=['GET']) #Servicio para obtener y generar JSON para autocomplete de ciudades
def get_cities():   
    conn.cursor.execute(queryCities)
    propertiesCities = conn.cursor.fetchall()
    list_cities = []   
    for row in propertiesCities:
        list_cities.append(row[0])
    cities=set(list_cities)
    objects_list = [] 
    for c in cities:
        d = collections.OrderedDict()
        d["title"] = c
        d["value"] = c
        objects_list.append(d)
    c = json.dumps(objects_list)

    return c

@main.route('/properties/years/', methods=['GET']) #Servicio para obtener y generar JSON para autocomplete de año de construcción
def get_years():   
    conn.cursor.execute(queryYear)
    propertiesYears = conn.cursor.fetchall()
    list_years = []   
    for row in propertiesYears:
        list_years.append(row[0])
    years=set(list_years)
    objects_list = [] 
    for y in years:
        d = collections.OrderedDict()
        d["title"] = str(y)
        d["value"] = str(y)
        objects_list.append(d)
    y = json.dumps(objects_list)

    return y

if __name__ == '__main__':
    main.run(debug=True, port=4000)