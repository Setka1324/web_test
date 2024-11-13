from flask import Flask, render_template, jsonify, request, g
import sqlite3
import uuid


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('./DB/companies.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html", active_page="home")

@app.route("/info", methods=["GET"])
def info():
    return render_template("info.html", active_page="info")

@app.route("/techs", methods=["GET"])
def techs():
    return render_template("techs.html", active_page="techs")

@app.route('/news')
def news():
    return render_template('news.html', active_page="news")

@app.route('/compliance', methods=['GET'])
def compliance():
    return render_template('compliance.html', active_page='compliance')


@app.route("/api/headquarters", methods=["GET"])
def headquarters():
    technologies = request.args.get('technologies')
    query = """
        SELECT companies.company_name, headquarters.hq_city, headquarters.hq_country, companies.company_number
        FROM headquarters
        JOIN companies ON headquarters.company_key = companies.bibtex_key
    """
    
    params = []
    if technologies:
        tech_list = technologies.split(',')
        placeholders = ', '.join('?' for _ in tech_list)
        query += f" JOIN operations ON headquarters.company_key = operations.company_key WHERE operations.technology_sold IN ({placeholders})"
        params = tech_list

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()

    companies = []
    for row in rows:
        companies.append({
            "company_name": row["company_name"],
            "hq_city": row["hq_city"],
            "hq_country": row["hq_country"]
        })

    conn.close()
    return jsonify(companies)

@app.route("/api/technologies", methods=["GET"])
def technologies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT technology_sold FROM operations")
    rows = cur.fetchall()
    
    technologies = [row["technology_sold"] for row in rows if row["technology_sold"]]
    conn.close()
    return jsonify(technologies)

@app.route('/api/countries', methods=['GET'])
def get_countries():
    conn = get_db_connection()
    countries = conn.execute('SELECT DISTINCT Country FROM country_data').fetchall()
    conn.close()
    return jsonify([dict(row) for row in countries])

@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    country = request.args.get('country')
    conn = get_db_connection()
    incidents = conn.execute('SELECT Incident FROM country_data WHERE Country = ?', (country,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in incidents])

@app.before_request
def before_request():
    if 'session_id' not in request.cookies:
        session_id = str(uuid.uuid4())
    else:
        session_id = request.cookies.get('session_id')
    g.session_id = session_id

@app.after_request
def after_request(response):
    response.set_cookie('session_id', g.session_id)
    return response

@app.route('/api/track', methods=['POST'])
def track_user_action():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_tracking (session_id, page_name, action, detail)
        VALUES (?, ?, ?, ?)
    """, (g.session_id, data['page_name'], data['action'], data.get('detail', '')))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200

@app.route('/api/companies', methods=['GET'])
def get_companies():
    conn = get_db_connection()
    companies = conn.execute('SELECT company_name FROM companies').fetchall()
    conn.close()
    return jsonify([dict(row) for row in companies])

@app.route('/api/compliance', methods=['GET'])
def get_compliance():
    company_name = request.args.get('company_name')
    if not company_name:
        return jsonify([])  # Return empty list if no company name provided

    conn = get_db_connection()
    company = conn.execute('SELECT bibtex_key FROM companies WHERE company_name = ?', (company_name,)).fetchone()
    if company:
        compliance_standards = conn.execute('SELECT eu, nato, wassenaar, oecd, csr FROM compliance WHERE company_key = ?', (company['bibtex_key'],)).fetchone()
        conn.close()
        if compliance_standards:
            standards = []
            for column in compliance_standards.keys():
                compliant_value = compliance_standards[column]
                compliant = 'Yes' if compliant_value and compliant_value != "0" else 'No'
                column_upper = column.upper()
                standards.append({
                    'standard': column_upper,
                    'compliant': compliant,
                    'csr_value': compliance_standards['csr'] if column == 'csr' else None
                })
            return jsonify(standards)
    else:
        conn.close()
        return jsonify([])  # No company found with that name

    
if __name__ == "__main__":
    app.run(debug=True)
