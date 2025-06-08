from pickle import TRUE
import psycopg2
from jinja2 import Template
from flask import Flask, render_template
import os
import gunicorn
from dotenv import load_dotenv
#import pg8000
app = Flask(__name__,template_folder='template')

@app.route('/index')
def home(name):
   return render_template('index.html')
@app.route('/mytemplate')
def user():
   dbfield_list = ["first name", "Last name", "Mobile No"]
   return render_template('user.html',dbfield_list=dbfield_list)
@app.route('/')
def mytemplate():
   #Create a template
   load_dotenv()   
   strTemplate = "<form action=""/action_page.php"">" 
   strTemplate = strTemplate + "<table>{% for dbfield in dbfield_list %}"
   strTemplate = strTemplate + "<tr> <td> <label for='fname'>{{dbfield}}</label> </td>"
   strTemplate = strTemplate + "<td> <input type=""text"" id={{dbfield}} name={{dbfield}}></td></tr>"
   strTemplate = strTemplate + "{% endfor %} <table>"
   strTemplate = strTemplate + "<input type=""submit"" value=""Submit Form"">"
   strTemplate = strTemplate + "</form>"
   #Finsih Create a template finished
    
   # Create a DB Connection with postgres db
   db_name = os.getenv('db_name')
   user_name = os.getenv('user_name')
   port = os.getenv('port')
   password = os.getenv('password')
   host = os.getenv('host')
   pg_db_url = os.getenv('PG_DB_URL')
   print (pg_db_url)
   #connection = psycopg2.connect(database=db_name, user=user_name, password=password, host=host, port=port)
   connection = psycopg2.connect(pg_db_url,sslmode='require')
   #Finsih Create a template finished updated
    
   # Create a DB Connection with postgres db in Heroku
   cursor = connection.cursor()
   #cursor.execute("SELECT Column_name, data_type,udt_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = 'salesforce' AND table_name   = 'contact'")
   cursor.execute("SELECT Column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = 'salesforce' AND table_name   = 'contact' And Data_type <> 'timestamp without time zone' ")
   #print (list(cursor))
   fieldlist = list(cursor)
   # fieldlist = [field.replace('(','') for field in fieldlist ]
   # print (fieldlist)
   #

   #t=Template("<Title> {{ title }} </Title><body> {{ content }} </body>")
   t=Template(strTemplate)
   #dict = {"title": "First page", "content": "This is the first page"}
   dbfield_list = []
   for p in fieldlist:
      #print (p)
      
      dbfield_list.append(p)

   return t.render(dbfield_list=dbfield_list)
if __name__ == '__main__':
   app.run(debug=TRUE)
   app.run()
