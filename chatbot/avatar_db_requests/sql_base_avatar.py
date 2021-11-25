
#explication code
from os import times
import mysql.connector #pip3 install mysql-connector-python
from mysql.connector import Error
import json
import time
import base64 #pip3 install pybase64


config = {                      # nouvelle base de données
    'host': "dev.smartevlab.fr",
    'database': "avatar",
    'user': "smartevlab",
    'password': "nMJgkM9R4RKXvc",
    'port': "3308"
}

#variable de connection

#region input
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                           Input user Data
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def verification(user_id):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "SELECT * FROM login WHERE vin_user = '%s'" % (user_id)
    #sql = """SELECT ValA FROM `%s` WHERE Val2 = '%s' AND Val3 = '%s'""" % (Val1, Val2, Val3)
    cur.execute(sql)
    myresult = cur.fetchall()
    if myresult == []:
        print("this vin_user is not in base login")
        return False
    sql = "SELECT * FROM info_vehicule WHERE vin_user = '%s'" % (user_id)
    cur.execute(sql)
    myresult = cur.fetchall()
    if myresult == []:
        print("this vin_user is not in base info_vehicule")
        return False
    sql = "SELECT * FROM services WHERE vin_user = '%s'" % (user_id)
    cur.execute(sql)
    myresult = cur.fetchall()
    if myresult == []:
        print("this vin_user is not in base services")
        return False


# ajouter à la base de données le véhicule du client à l'aide du vin
def insert(vin, email, password,first_name,last_name,postalcode):  
    #new_customer=0  
    #if verification(vin) == True: #L'utilisateur n'est pas présent dans la base de données
        #print("Utilisateur déjà présent dans la database")
        #return
   # else:
    new_customer='1'          
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "INSERT INTO login (vin_user, email, password, first_name, last_name,postalcode,new_customer ) VALUES (%s, %s, %s,%s,%s,%s,%s)" # categorie messenger_user_id remplacée par vin_user
    val = (vin, email, encode(password),first_name,last_name,postalcode, new_customer)
    cur.execute(sql,val)
    #ajoute dans la base d'info vehicule le vin du véhicule
      # sql = """INSERT INTO info_vehicule (vin_user) VALUES (%s)""" 
       #cur.execute(sql, (vin,))
    #ajoute dans la base des servise
       #sql = """INSERT INTO services (vin_user) VALUES (%s)""" 
       #cur.execute(sql, (vin,))
    cnx.commit() #Push de la requête
    #reset_services(vin)
    cur.close()



#endregion

#region login
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                           Login Data
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#Cette fonction a pour objectif de créer un compte à l'utilisateur lors de la première utilisation. Elle est appellée par app.py dans la classe "CreateAccount"
def create_account(vin_user,email, password):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    new_customer= "1"
    print(vin_user, email, password)
    sql = "INSERT INTO login (vin_user, email, password, new_customer) VALUES (%s, %s, %s, %s)" 
    #Avant d'insérer les valeurs dans la tale login, on encode en base 64 le mdp par sécurité
    val = (vin_user, email, encode(password), new_customer)
    cur.execute(sql,val)
     #ajoute dans la base d'info vehicule le  user id
    sql = """INSERT INTO info_vehicule (vin_user) VALUES (%s)""" 
    cur.execute(sql, (vin_user,))
    # #ajoute dans la base des servise
    sql = """INSERT INTO services (vin_user) VALUES (%s)""" 
    cur.execute(sql, (vin_user,))
    cnx.commit() #Push de la requête
    #reset_services(user_id)
    cur.close()


def read_login(user_id): #renvoit le vin_user et email et password // en dictionnaire
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "SELECT * FROM login WHERE vin_user = '%s'" % (user_id)
    cur.execute(sql)
    myresult = cur.fetchone() #renvoile un tuple qui et une liste que on peux pas changer 
    #print(myresult)
    #print(type(myresult))
    #print(myresult[2])
    data_returne = {"vin_user": myresult[0], "email": myresult[1], "password": decode(myresult[2])}
    #print(data_returne.get("password"))
    return data_returne

def read_info(user_id):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "SELECT * FROM login WHERE vin_user = '%s'" % (user_id)
    cur.execute(sql)
    myresult = cur.fetchone() #renvoile un tuple qui et une liste que on peux pas change 
    return myresult


def read_login_id():
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    cur.execute("SELECT login.vin_user, login.email, login.password  FROM avatar.login;")
    #récupèrer toutes les lignes de la dernière instruction exécutée.
    lista = []
    while True:
        rest = cur.fetchone()
        if rest == None:
            #print("sorite")
            break
        else:
            #print("resr: " , rest)
            lista.append(rest[0])
            lista.append(rest[1])
            lista.append(decode(rest[2]))
    #print(lista)
    return lista


def list_for_first_scrapping():
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    cur.execute("SELECT login.vin_user, login.email, login.password  FROM avatar.login  WHERE new_customer = '1';")
    #récupèrer toutes les lignes de la dernière instruction exécutée.
    liste_new_customer = []
    while True:
        rest = cur.fetchone()
        if rest == None:
            #print("sorite")
            break
        else:
            #print("resr: " , rest)
            liste_new_customer.append(rest[0])
            liste_new_customer.append(rest[1])
            liste_new_customer.append(decode(rest[2]))
    #print(liste_new_customer)
    return liste_new_customer


def read_postal_code():#recupere id et la localisation des personne "departement"
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    cur.execute("SELECT login.vin_user, login.postal_code  FROM avatar.login WHERE login.postal_code != 'null';")
    #récupèrer toutes les lignes de la dernière instruction exécutée.
    lista = []
    while True:
        rest = cur.fetchone()
        if rest == None:
            #print("sorite")
            break
        else:
            #print("resr: " , rest)
            lista.append(rest[0]) #id
            lista.append(rest[1]) #postal
    #print(lista)
    return(lista)


def modification_type_login(user_id, categorie, value):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "UPDATE `avatar`.`login` SET `%s` = '%s' WHERE (`vin_user` = '%s')" % (categorie,value, user_id)
    cur.execute(sql)
    cnx.commit() #Push de la requête
    cur.close()

#endregion

#region Info_vehicule
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                           Info vehicule Data
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def modification_type(user_id, categorie, value):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "UPDATE `avatar`.`info_vehicule` SET `%s` = '%s' WHERE (`vin_user` = '%s')" % (categorie,value, user_id)
    cur.execute(sql)
    cnx.commit() #Push de la requête
    cur.close()


def modification_meteo(user_id, notif_meteo, forecast_temp):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "UPDATE `avatar`.`info_vehicule` SET `notif_meteo` = '%s' WHERE (`vin_user` = '%s')" % (notif_meteo, user_id)
    cur.execute(sql)
    sql = "UPDATE `avatar`.`info_vehicule` SET `forecast_temp` = '%s' WHERE (`vin_user` = '%s')" % (forecast_temp, user_id)
    cur.execute(sql)
    cnx.commit() #Push de la requête
    cur.close()


def decalage_heur_HVAC(user_id):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "SELECT * FROM info_vehicule WHERE vin_user = '%s'" % (user_id)
    cur.execute(sql)
    myresult = cur.fetchone() #renvoile un tuple qui et une liste que on peux pas change 
    heur = myresult[15] #recupere l'heur emie
    print(heur)
    modification_type(user_id, "old_HVAC_heure_depart", heur)
    modification_type(user_id, "HVAC_heure_depart", "")

def read_type_info_vehicule(user_id):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "SELECT * FROM info_vehicule WHERE vin_user = '%s'" % (user_id)
    cur.execute(sql)
    myresult = cur.fetchone() #renvoile un tuple qui et une liste que on peux pas change 
    return myresult




def read_hvac(): #recupère l'id, email, password, heur d'activation de hvac// renvoille comme une liste
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    cur.execute("SELECT info_vehicule.vin_user, login.email, login.password,  info_vehicule.HVAC_heure_depart FROM avatar.login INNER JOIN avatar.info_vehicule ON login.vin_user=info_vehicule.vin_user WHERE info_vehicule.HVAC_heure_depart != 'null' AND info_vehicule.HVAC_heure_depart != '';")
    #récupèrer touts les personne qui on le hvac avec une heur d'active
    lista = []
    while True:
        reset = cur.fetchone()
        if reset == None:
            #print("sorite")
            break
        else:
            lista.append(reset[0]) #id
            lista.append(reset[1]) #email
            lista.append(decode(reset[2])) #password
            lista.append(reset[3]) #time d'activation
    #print(lista)
    return(lista)


def soc_target_scrapping(): #recupere l'id, email, passe word quand la personne et abonne au servise soc_target et que sont niveau de batterie et audessus soc_target alors il faudra arrete la charge
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "SELECT info_vehicule.vin_user, login.email, login.password FROM avatar.services INNER JOIN avatar.login ON services.vin_user=login.vin_user  INNER JOIN avatar.info_vehicule ON services.vin_user=info_vehicule.vin_user WHERE info_vehicule.batteryLevel >= info_vehicule.soc_target AND services.SOC_Target > 0;"
    cur.execute(sql)
    #crée une liste vide
    liste_soc_target = []
    while True:
        reset = cur.fetchone()
        #print(reset)
        if reset == None:
            #print("sorite")
            #arrive a la fin du tableau
            break
        else:
            liste_soc_target.append(reset[0]) #id
            liste_soc_target.append(reset[1]) #email
            liste_soc_target.append(decode(reset[2])) #password
    #print(liste_soc_target)
    return(liste_soc_target)

def soc_target_expert(user_id): #recupere le soc target si le service et active et que le soc targerd et supereure a 0
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "SELECT info_vehicule.soc_target FROM avatar.services INNER JOIN avatar.info_vehicule ON services.vin_user=info_vehicule.vin_user        WHERE info_vehicule.vin_user = '%s' AND info_vehicule.soc_target > '0' AND info_vehicule.soc_target != 'null' AND services.SOC_Target > 0" % (user_id)
    cur.execute(sql)
    myresult = cur.fetchone()
    if myresult == None:
        print("vide")
        return None
    print("myresult: ",myresult[0])
    return myresult[0]




def read_url_car(user_id):
    return read_categorie(user_id, "info_vehicule", "url_car")

def modification_autonomie(user_id, autonomie):
    modification_type(user_id, "batteryAutonomy", autonomie)

def read_soc_target(user_id):
    return read_categorie(user_id, "info_vehicule", "soc_target")

def modification_soc_target(user_id, value):
    modification_type(user_id, "soc_target", value)

#endregion

#region services
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                           Services Data
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def modification_type_services(user_id, categorie, value):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "UPDATE `chatbot`.`services` SET `%s` = '%s' WHERE (`vin_user` = '%s')" % (categorie,value, user_id)
    cur.execute(sql)
    cnx.commit() #Push de la requête
    cur.close()

def incrementation_service(user_id, categorie):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    categorie2 = categorie + " + 1"
    sql = "UPDATE `chatbot`.`services` SET `%s` = %s WHERE (`vin_user` = '%s')" % (categorie, categorie2, user_id)
    cur.execute(sql)
    cnx.commit() #Push de la requête
    cur.close()

def verification_notif_service(user_id,service): #permet de vérifier si l'utilisateur est inscrit à un service
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "SELECT * FROM services WHERE `%s` > '0' AND vin_user ='%s'" % (service,user_id)
    cur.execute(sql)
    myresult = cur.fetchall()
    print(myresult)
    if myresult == []:
        print("Le client n'est pas inscrit au service ",service)
        return False
    else :
        print("Le client est inscrit au service ",service)
        return True

def manage_notif(user_id,service,notif_status): #permet de modifier la valeur d'une notif en fonction du service
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "UPDATE `chatbot`.`services` SET `%s`  = '%s' WHERE (vin_user = '%s')" % (service,notif_status,user_id)
    cur.execute(sql)
    cnx.commit()
    myresult = cur.fetchall()
    print(myresult)
    cur.close()

def reset_services(user_id): 
    name_column = column_names("services")
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    for idx, val in enumerate(name_column):
        #mettre a zero tout les servise
        if idx > 0: #ne pas mettre 0 sur messeger_user_id
            #print("numero: ", idx, " valeur: ", val)
            if val == "SOC_target" : #mettre a 0 le soc target pour pas l'active de base
                sql = "UPDATE `chatbot`.`services` SET `%s` = '%s' WHERE (`vin_user` = '%s')" % (val,"0", user_id)
                cur.execute(sql)
            else:
                sql = "UPDATE `chatbot`.`services` SET `%s` = '%s' WHERE (`vin_user` = '%s')" % (val,"1", user_id)
                cur.execute(sql)

    cnx.commit() #Push de la requête
    cur.close()
    




#endregion

#region fonction


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                           Autre fonction Data
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def read_categorie(user_id, table, categorie):
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "SELECT %s FROM `%s` WHERE vin_user = '%s' " % (categorie, table, user_id)
    cur.execute(sql) 
    myresult = cur.fetchone()
    #print("myresult: ",myresult[0])
    return myresult[0]


#renvoille le nom des column disponible
def column_names(categorie): 
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "SELECT * FROM `%s` " % (categorie)
    cur.execute(sql) 
    field_names = [i[0] for i in cur.description]
    print(field_names)
    return field_names

def killeur(userd_id):
    print("killeur")
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    sql = "DELETE FROM `chatbot`.`login` WHERE (`vin_user` = '%s')" %(userd_id)
    cur.execute(sql)
    sql = "DELETE FROM `chatbot`.`services` WHERE (`vin_user` = '%s')" %(userd_id)
    cur.execute(sql)
    sql = "DELETE FROM `chatbot`.`info_vehicule` WHERE (`vin_user` = '%s')" %(userd_id)
    cur.execute(sql)
    cnx.commit() #Push de la requête
    cur.close()


def mois(i):
    switcher={
        1:'Janvier',
        2:'Février',
        3:'Mars',
        4:'Avril',
        5:'Mai',
        6:'Juin',
        7:'Juillet',
        8:'Aout',
        9:'Septembre',
        10:'Octobre',
        11:'Novembre',
        12:'Décembre'
    }
    return switcher.get(i,"Invalid day of week")


def decode(x):
    #print("x : ", x)
    try:
        password_byte= x.encode("ascii") #on convertie password en ascii
        password_decode = base64.b85decode(password_byte)
        password_string = password_decode.decode("ascii")
        #print(password_string)
        return password_string

    except:
        print("An exception occurred")
        return x


def encode(x):
    password_byte= x.encode("ascii") #on convertie password en ascii
    password_encode = base64.b85encode(password_byte)
    return password_encode

#endregion

'''

'''
