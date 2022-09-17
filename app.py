from flask import Flask, render_template, request
import mysql.connector


app = Flask(__name__)

config = {
    'user': 'pyconmy',
    'password': 'pyconmy12345',
    'host': 'pyconmydb.pycon.my',
    'database': 'acme_business_card'
    }

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

@app.route("/check_is_connected")
def check_is_connected():
    if cnx.is_connected():
        return "You're connected to database"
    else:
        return "Not connected"

@app.route("/create_table", methods=['POST'])
def create_table():
    cursor = cnx.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS `individual` (
        `individual_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        `first_name` varchar(255),
        `middle_name` varchar(255),
        `last_name` varchar(255),
        `mobile_number` varchar(255),
        `office_number` varchar(255),
        `email_address` varchar(255),
        `portfolio_url` varchar(255),
        `linkedin_url` varchar(255),
        `education` varchar(255),
        `state` varchar(255),
        `company_id` int,
        `job_id` int
        );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS `company` (
        `company_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        `company_name` varchar(255),
        `address` varchar(255),
        `city` varchar(255),
        `state` varchar(255),
        `company_url` varchar(255),
        `company_type` varchar(255),
        `industry` varchar(255)
        );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS `job` (
        `job_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        `job_title` varchar(255)
        );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS `individual_relationship` (
        `relationship_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        `individual_id` int,
        `connected_individual_id` int,
        `connected_date` date
        );""")
    return 'success'

@app.route("/insert_business_card", methods=['POST'])
def insert_business_card():
    cursor = cnx.cursor()
    try:
        first_name = request.args.get('first_name')
        middle_name = request.args.get('middle_name')
        last_name = request.args.get('last_name')
        mobile_number = request.args.get('mobile_number')
        office_number = request.args.get('office_number')
        email_address = request.args.get('email_address')
        portfolio_url = request.args.get('portfolio_url')
        linkedin_url = request.args.get('linkedin_url')
        education = request.args.get('education')
        state = request.args.get('state')
        company_id = request.args.get('company_id')
        job_id = request.args.get('job_id')
        cursor.execute(f"""INSERT INTO individual 
                        (first_name, middle_name, last_name, mobile_number, office_number, email_address, portfolio_url, linkedin_url, education, state, company_id, job_id)
                        VALUES ('{first_name}', '{middle_name}', '{last_name}', '{mobile_number}', '{office_number}', '{email_address}', '{portfolio_url}', '{linkedin_url}', '{education}', '{state}', '{company_id}', '{job_id}');""", )
        cnx.commit()
        return {'status': 'success', 'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name, 'mobile_number': mobile_number, 'office_number': office_number, 'email_address': email_address, 'portfolio_url': portfolio_url, 'linkedin_url': linkedin_url, 'education': education, 'state': state, 'company_id': company_id, 'job_id': job_id}
    except:
        return {'status': 'error'}

@app.route("/insert_company", methods=['POST'])
def insert_company():
    cursor = cnx.cursor()
    try:
        company_name = request.args.get("company_name")
        address = request.args.get("address")
        city = request.args.get("city")
        state = request.args.get("state")
        company_url = request.args.get("company_url")
        company_type = request.args.get("company_type")
        industry = request.args.get("industry")
        cursor.execute(f"""INSERT INTO company 
                    (company_name, 
                    address, 
                    city,
                    state,
                    company_url,
                    company_type,
                    industry) 
                    VALUES 
                    ('{company_name}', 
                    '{address}', 
                    '{city}',
                    '{state}',
                    '{company_url}',
                    '{company_type}',
                    '{industry}');""")
        cnx.commit()
        return {'status': 'success', 'company_name': company_name, 'address': address, 'city': city, 'state': state, 'company_url': company_url, 'company_type': company_type, 'industry': industry}
    except:
        return {'status': 'error'}

@app.route("/insert_relationship", methods=['POST'])
def insert_relationship():
    cursor = cnx.cursor()
    try:
        connected_individual_id = request.args.get("connected_individual_id")
        connected_date = request.args.get("connected_date")
        individual_id = request.args.get("individual_id")
        cursor.execute(f"""INSERT INTO individual_relationship (individual_id, connected_individual_id, connected_date) 
                    VALUES ('{individual_id}', '{connected_individual_id}', '{connected_date}') ;""")
        cnx.commit()    
        return {'status': 'success', 'connected_individual_id': connected_individual_id, 'connected_date': connected_date}
    except:
        return {'status': 'error'}

@app.route("/insert_job", methods=['POST'])
def insert_job():
    cursor = cnx.cursor()
    try:
        job_title = request.args.get("job_title")
        cursor.execute(f"""INSERT INTO job (job_title) 
                    VALUES ('{job_title}');""")
        cnx.commit()
        return {'status': 'success', 'job_title': job_title}
    except:
        return {'status': 'error'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)