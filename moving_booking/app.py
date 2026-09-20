# app.py (small change: return conflict seat ids on booking conflict)
from flask import Flask, request, jsonify, render_template, session
import mysql.connector
from datetime import datetime
import traceback
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET', 'change_this_to_a_random_secret_123')

db_cfg = {
    'user': 'root',
    'password': 'S@rthak20',
    'host': '127.0.0.1',
    'database': 'movie_booking'
}

def get_conn():
    return mysql.connector.connect(**db_cfg)

SEAT_MULTIPLIER = {
    'Regular': 1.0,
    'Premium': 1.2,
    'VIP': 1.4,
    'Recliner': 1.6
}

# ---------- helpers ----------
def valid_email(e):
    return isinstance(e, str) and '@' in e and len(e) >= 5

def valid_password(p):
    # at least 8 chars, 1 uppercase, 1 number, 1 special
    if not isinstance(p, str) or len(p) < 8:
        return False
    if not re.search(r'[A-Z]', p): return False
    if not re.search(r'[0-9]', p): return False
    if not re.search(r'[\W_]', p): return False
    return True

@app.route('/')
def index():
    return render_template('index_v2.html')

# shows with optional filters
@app.route('/shows')
def shows():
    city = request.args.get('city')
    fmt = request.args.get('format')
    q = """
      SELECT s.id, m.title, t.name as theater, t.city as city, sc.name as screen, s.start_time, s.price, s.format
      FROM `Show` s
      JOIN Movie m ON s.movie_id = m.id
      JOIN Screen sc ON s.screen_id = sc.id
      JOIN Theater t ON sc.theater_id = t.id
    """
    cond = []
    params = []
    if city:
        cond.append("t.city = %s"); params.append(city)
    if fmt:
        cond.append("s.format = %s"); params.append(fmt)
    if cond:
        q += " WHERE " + " AND ".join(cond)
    q += " ORDER BY s.start_time LIMIT 500"
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute(q, tuple(params))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(rows)

@app.route('/seats_status/<int:show_id>')
def seats_status(show_id):
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT s.screen_id, sc.name as screen_name, t.name as theater_name, t.city, s.price as base_price, s.format FROM `Show` s JOIN Screen sc ON s.screen_id=sc.id JOIN Theater t ON sc.theater_id=t.id WHERE s.id=%s", (show_id,))
    meta = cur.fetchone()
    if not meta:
        cur.close(); conn.close()
        return jsonify({'error':'show not found'}), 404
    screen_id = meta['screen_id']
    cur.execute("""
      SELECT seat.id, seat.row_label, seat.seat_number, seat.seat_type,
             (CASE WHEN t.seat_id IS NULL THEN 0 ELSE 1 END) AS is_booked
      FROM Seat seat
      LEFT JOIN (
        SELECT seat_id FROM Ticket WHERE show_id=%s AND status='BOOKED'
      ) t ON seat.id = t.seat_id
      WHERE seat.screen_id=%s
      ORDER BY seat.row_label, seat.seat_number
    """, (show_id, screen_id))
    rows = cur.fetchall()
    cur.close(); conn.close()
    for r in rows:
        r['is_booked'] = bool(r['is_booked'])
    return jsonify({'meta': meta, 'seats': rows})

@app.route('/book', methods=['POST'])
def book():
    data = request.json
    user_id = session.get('user_id') or data.get('user_id')
    show_id = data.get('show_id')
    seat_ids = data.get('seat_ids')

    if not user_id or not show_id or not seat_ids:
        return jsonify({'error':'missing params, login or include user_id'}), 400

    try:
        if isinstance(seat_ids, str):
            seat_ids = [int(x.strip()) for x in seat_ids.split(',') if x.strip()]
        else:
            seat_ids = [int(x) for x in seat_ids]
    except Exception:
        return jsonify({'error':'invalid seat_ids; must be list of integers'}), 400

    if len(seat_ids) == 0:
        return jsonify({'error':'no seats provided'}), 400

    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()
        format_ids = ",".join(["%s"]*len(seat_ids))
        # lock selected seat rows and consume result
        cur.execute(f"SELECT id FROM Seat WHERE id IN ({format_ids}) FOR UPDATE", tuple(seat_ids))
        _locked = cur.fetchall()

        # check already booked (we will return exact list if conflict)
        cur.execute(
            f"SELECT seat_id FROM Ticket WHERE seat_id IN ({format_ids}) AND show_id=%s AND status='BOOKED'",
            tuple(seat_ids + [show_id])
        )
        conflict_rows = cur.fetchall()
        if conflict_rows:
            conflict_ids = [r['seat_id'] if isinstance(r, dict) else r[0] for r in conflict_rows]
            conn.rollback()
            return jsonify({'error':'some seats not available', 'conflict': conflict_ids}), 409

        # get show & base price
        cur.execute("SELECT s.id, s.price, s.format, m.title FROM `Show` s JOIN Movie m ON s.movie_id=m.id WHERE s.id=%s", (show_id,))
        show_row = cur.fetchone()
        if not show_row:
            conn.rollback()
            return jsonify({'error':'show not found'}), 404
        base_price = float(show_row['price'])

        # get seat types
        cur.execute(f"SELECT id, seat_type FROM Seat WHERE id IN ({format_ids})", tuple(seat_ids))
        seat_types = cur.fetchall()
        price_map = {}; total = 0.0
        for st in seat_types:
            sid = st['id'] if isinstance(st, dict) else st[0]
            stype = st['seat_type'] if isinstance(st, dict) else st[1]
            stype = stype or 'Regular'
            mult = SEAT_MULTIPLIER.get(stype, 1.0)
            price = round(base_price * mult, 2)
            price_map[sid] = price
            total += price

        # insert booking
        cur.execute("INSERT INTO Booking (user_id, show_id, total_amount, status) VALUES (%s,%s,%s,'CONFIRMED')",
                    (user_id, show_id, total))
        booking_id = cur.lastrowid

        # insert tickets
        for sid in seat_ids:
            price_for_seat = price_map.get(sid, base_price)
            cur.execute("INSERT INTO Ticket (booking_id, show_id, seat_id, price, status) VALUES (%s,%s,%s,%s,'BOOKED')",
                        (booking_id, show_id, sid, price_for_seat))

        # payment
        cur.execute("INSERT INTO Payment (booking_id, amount, method, status) VALUES (%s,%s,%s,'SUCCESS')",
                    (booking_id, total, data.get('method','CARD')))
        conn.commit()
        return jsonify({'success': True, 'booking_id': booking_id})
    except Exception as e:
        print("ERROR in /book:", e); traceback.print_exc()
        try: conn.rollback()
        except: pass
        return jsonify({'error': str(e)}), 500
    finally:
        try: cur.close(); conn.close()
        except: pass

@app.route('/booking/<int:booking_id>')
def booking_detail(booking_id):
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("""
      SELECT b.id as booking_id, b.user_id, b.show_id, b.booking_time, b.total_amount, b.status,
             s.start_time as show_time, s.price as base_price, s.format,
             m.title as movie_title, sc.name as screen_name, t.name as theater_name, t.city
      FROM Booking b
      JOIN `Show` s ON b.show_id = s.id
      JOIN Movie m ON s.movie_id = m.id
      JOIN Screen sc ON s.screen_id = sc.id
      JOIN Theater t ON sc.theater_id = t.id
      WHERE b.id = %s
    """, (booking_id,))
    b = cur.fetchone()
    if not b:
        cur.close(); conn.close(); return jsonify({'error':'booking not found'}), 404
    cur.execute("""
      SELECT tk.id as ticket_id, tk.seat_id, tk.price, tk.status, se.row_label, se.seat_number, se.seat_type
      FROM Ticket tk
      JOIN Seat se ON tk.seat_id = se.id
      WHERE tk.booking_id = %s
      ORDER BY se.row_label, se.seat_number
    """, (booking_id,))
    tickets = cur.fetchall()
    cur.close(); conn.close()
    for t in tickets: t['seat_label'] = f"{t['row_label']}{t['seat_number']}"
    return jsonify({'booking': b, 'tickets': tickets})

# ---------- AUTH ----------
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()
    password = data.get('password')
    if not name or not email or not password:
        return jsonify({'error':'name, email and password required'}), 400
    if not valid_email(email):
        return jsonify({'error':'invalid email (must contain @)'}), 400
    if not valid_password(password):
        return jsonify({'error':'password must be 8+ chars, include 1 uppercase, 1 number, 1 special char'}), 400
    pw_hash = generate_password_hash(password)
    conn = get_conn(); cur = conn.cursor()
    try:
        cur.execute("INSERT INTO MovieUser (name, email, phone, password_hash) VALUES (%s,%s,%s,%s)",
                    (name, email, phone, pw_hash))
        conn.commit()
        user_id = cur.lastrowid
        session['user_id'] = user_id; session['name'] = name
        cur.close(); conn.close()
        return jsonify({'success':True, 'user_id': user_id})
    except mysql.connector.IntegrityError:
        conn.rollback(); cur.close(); conn.close()
        return jsonify({'error':'email already registered'}), 409
    except Exception as e:
        conn.rollback(); cur.close(); conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = (data.get('email') or '').strip(); password = data.get('password')
    if not email or not password:
        return jsonify({'error':'email and password required'}), 400
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, password_hash FROM MovieUser WHERE email=%s", (email,))
    user = cur.fetchone(); cur.close(); conn.close()
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error':'invalid credentials'}), 401
    session['user_id'] = user['id']; session['name'] = user['name']
    return jsonify({'success':True, 'user_id': user['id'], 'name': user['name']})

@app.route('/logout')
def logout():
    session.clear(); return jsonify({'success':True})

@app.route('/whoami')
def whoami():
    if 'user_id' in session:
        return jsonify({'logged_in':True, 'user_id': session['user_id'], 'name': session.get('name')})
    return jsonify({'logged_in':False})

if __name__ == '__main__':
    app.run(debug=True)
