from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = "metrics.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            response_time REAL NOT NULL,
            status_code INTEGER NOT NULL,
            error TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.before_request
def ensure_db():
    init_db()

@app.route('/metrics', methods=['POST'])
def add_metric():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO metrics (timestamp, endpoint, response_time, status_code, error)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data.get('timestamp', datetime.utcnow().isoformat()),
        data['endpoint'],
        data['response_time'],
        data['status_code'],
        data.get('error')
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'}), 201

@app.route('/metrics', methods=['GET'])
def get_metrics():
    # Optional query params: endpoint, since, until, limit
    endpoint = request.args.get('endpoint')
    since = request.args.get('since')
    until = request.args.get('until')
    limit = int(request.args.get('limit', 100))
    query = "SELECT * FROM metrics WHERE 1=1"
    params = []
    if endpoint:
        query += " AND endpoint=?"
        params.append(endpoint)
    if since:
        query += " AND timestamp>=?"
        params.append(since)
    if until:
        query += " AND timestamp<=?"
        params.append(until)
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    conn = get_db()
    c = conn.cursor()
    c.execute(query, params)
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/metrics/summary', methods=['GET'])
def get_summary():
    # Returns average response time and error count per endpoint
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT endpoint,
               COUNT(*) as count,
               AVG(response_time) as avg_response_time,
               SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as error_count
        FROM metrics
        GROUP BY endpoint
    ''')
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "API Performance Monitor is running. Use /metrics or /metrics/summary."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
