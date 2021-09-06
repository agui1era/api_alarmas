
import flask
import psycopg2
from flask import request
import datetime
import math 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase
import smtplib
from dateutil.relativedelta import relativedelta


def getDB(sql_query):
    try:     
        connection = psycopg2.connect(user = "postgres",
                                        password = "imagina12",
                                        host = "52.200.54.135",
                                        port = "5432",
                                        database = "postgres")
        print("Using Python variable in PostgreSQL select Query")
        cursor = connection.cursor()
        postgreSQL_select_Query = sql_query
        cursor.execute(postgreSQL_select_Query)
        bd_records = cursor.fetchall()
        for row in bd_records:
            print( "Query ok")
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)
    finally:
        # closing database connection
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed \n")
    try: 
       out_query=row[0]
    except (Exception, psycopg2.Error) as error:
       out_query="ERROR"
    return out_query

def date_to_milis(date_string):
    #convert date to timestamp
    obj_date = datetime.datetime.strptime(date_string,"%d/%m/%Y %H:%M:%S")
    return str(math.trunc(obj_date.timestamp() * 1000))

app = flask.Flask(__name__)

@app.route("/alarma/email/hmGbxMUUW2EVA1tqG2otEQ6zGq995kDk", methods=["GET"])
def alarma():
     mensaje = request.args.get("mensaje")
     email=request.args.get("email")
     hora_actual = datetime.datetime.now()
     str_hora_actual=hora_actual.strftime("%d/%m/%Y %H:%M:%S")
     
     sql_str_det="SELECT fecha FROM alarmas WHERE tipo_alarma ='email';"
     print(sql_str_det)
     result_det=str(getDB(sql_str_det))

     date_time_str = result_det
     print(date_time_str)
     date_time_obj = datetime.datetime.strptime(date_time_str, '%d/%m/%Y %H:%M:%S')  
     hora_bd = date_time_obj  + relativedelta(seconds=600)

     if hora_actual > hora_bd:
         print("Enviado mail")
         fromaddr = "notificaciones@igromi.com"
         msg = MIMEMultipart() 
         # storing the senders email address 
         msg['From'] = fromaddr 
         msg['Subject'] = mensaje
         body='' 
         # attach the body with the msg instance 
         msg.attach(MIMEText(body, 'plain')) 
         # instance of MIMEBase and named as p 
         p = MIMEBase("application", "octet-stream") 
         # creates SMTP session 
         s = smtplib.SMTP("smtp.zoho.com", 587) 
         # start TLS for security 
         s.starttls() 
         # Authentication 
         s.login(fromaddr, "imagina12") 
         # Converts the Multipart msg into a string 
         text = msg.as_string() 
         # sending the mail 
         msg["To"] = email,
         s.sendmail(fromaddr,email, text)

         sql_str_det="UPDATE alarmas SET fecha = '"+str_hora_actual+"'"
         print(sql_str_det)
         result_det=str(getDB(sql_str_det))

     return "Ok"
   
app.run(host="0.0.0.0", port=12345)
