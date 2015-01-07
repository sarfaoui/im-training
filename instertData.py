import os
import MySQLdb
import getpass
import csv
import yaml

#######################################################
def dbconnect():

    # mysql error 1045 workaround
    p = getpass.getpass()

    env = os.getenv('SERVER_SOFTWARE')
    if (env and env.startswith('Google App Engine/')):
        # Connecting from App Engine
        db = MySQLdb.connect(
                             unix_socket='/cloudsql/rare-basis-686:samir',
                             user='root')
    else:
        # Connecting from an external network.
        # Make sure your network is whitelisted
        db = MySQLdb.connect(
                             host='173.194.254.191',
                             port=3306,
                             user='root',
                             passwd=p,
                             db='world')
    return db

#######################################################
def loadCountries(db):

    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS Countries')
    cursor.execute('CREATE TABLE Countries (id INT, \
                   alpha2 VARCHAR(2), \
                   alpha3 VARCHAR(3), \
                   name VARCHAR(50), \
                   targetable INT)')

    filename = 'countries.csv'
    f = open(filename, 'r')
    try:
        reader = csv.DictReader(f)
        for row in reader:
            print row

            cursor.execute('INSERT INTO Countries VALUES(%s,"%s","%s","%s",%s)' %
                           (row['id'],
                            row['alpha2'],
                            row['alpha3'],
                            row['name'],
                            row['targetable']
                           ))

    finally:
        db.commit()
        db.close()
        f.close()

#######################################################
def loadRegions(db):

    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS Regions')
    cursor.execute('CREATE TABLE Regions (id INT, \
                    country_id INT, \
                    name VARCHAR(50), \
                    iso_code VARCHAR(5))')
        
    filename = 'regions.csv'
    f = open(filename, 'r')
    try:
        reader = csv.DictReader(f)
        for row in reader:
            print row
                                   
            cursor.execute('INSERT INTO Regions VALUES(%s,%s,"%s","%s")' %
                           (row['id'],
                            row['country_id'],
                            row['name'],
                            row['iso_code']
                            ))
                               
    finally:
        db.commit()
        db.close()
        f.close()

#######################################################
def loadCities(db):

    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS Cities')
    cursor.execute('CREATE TABLE Cities (id INT, \
                    country_id INT, \
                    region_id INT, \
                    name VARCHAR(50), \
                    iso_code VARCHAR(5))')
    
    filename = 'cities.json'
    f = open(filename, 'r')
    try:
        for line in f:
            d = yaml.load(line)
            id = d.get('id','NULL')
            country_id = d.get('country_id','NULL')
            region_id = d.get('region_id','NULL')
            name = d.get('name','NULL').encode('utf-8')
            iso_code = d.get('iso_code','NULL')

            print id, country_id, region_id, name, iso_code

            cursor.execute('INSERT INTO Cities VALUES(%s,%s,%s,"%s","%s")' %
                           (
                            id,
                            country_id,
                            region_id,
                            name,
                            iso_code
                            )
                           )
                   
    finally:
        db.commit()
        db.close()
        f.close()


#######################################################
if __name__ == '__main__':

    db = dbconnect()

    #loadCountries(db)
    #loadRegions(db)
    #loadCities(db)








