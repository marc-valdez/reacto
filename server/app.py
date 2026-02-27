from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reacto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False)
    claimed = db.Column(db.Boolean, default=False)
    claimed_at = db.Column(db.DateTime)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_code = db.Column(db.String(8), nullable=False)
    clip_name = db.Column(db.String(100), nullable=False)
    rt_ms = db.Column(db.Float, nullable=False)
    verdict = db.Column(db.String(20), nullable=False)
    stimulus_frame = db.Column(db.Integer)
    color_mode = db.Column(db.String(20))
    game = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/claim_code', methods=['POST'])
def claim_code():
    data = request.get_json()
    code_str = data.get('code', '').strip().upper()
    if not code_str or len(code_str) != 8 or not code_str.isalnum():
        return jsonify({'success': False, 'message': 'Invalid code format'}), 400

    code = Code.query.filter_by(code=code_str).first()
    if not code:
        return jsonify({'success': False, 'message': 'Code not found'}), 404
    if code.claimed:
        return jsonify({'success': False, 'message': 'Code already claimed'}), 409

    code.claimed = True
    code.claimed_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Code claimed successfully'})

@app.route('/submit_results', methods=['POST'])
def submit_results():
    data = request.get_json()
    auth_code = data.get('auth_code')
    results = data.get('results', {})

    if not auth_code:
        return jsonify({'success': False, 'message': 'Auth code required'}), 400

    # Verify auth_code is claimed
    code = Code.query.filter_by(code=auth_code, claimed=True).first()
    if not code:
        return jsonify({'success': False, 'message': 'Invalid or unclaimed auth code'}), 403

    for clip_name, res in results.items():
        rt_ms = res.get('rt_ms')
        verdict = res.get('type')
        if rt_ms is None or verdict is None:
            continue  # Skip invalid
        # Extract game, color_mode, stimulus_frame from clip_name
        parts = clip_name.split('_')
        stimulus_frame = int(parts[0]) if parts else 0
        color_mode = parts[1] if len(parts) > 1 else ''
        game = parts[2] if len(parts) > 2 else ''

        result = Result(
            auth_code=auth_code,
            clip_name=clip_name,
            rt_ms=rt_ms,
            verdict=verdict,
            stimulus_frame=stimulus_frame,
            color_mode=color_mode,
            game=game
        )
        db.session.add(result)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Results submitted'})

@app.route('/generate_codes', methods=['POST'])
def generate_codes():
    import random
    import string
    count = request.get_json().get('count', 100)
    codes = set()
    while len(codes) < count:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        codes.add(code)
    for c in codes:
        if not Code.query.filter_by(code=c).first():
            db.session.add(Code(code=c))
    db.session.commit()
    return jsonify({'success': True, 'message': f'Generated {len(codes)} codes'})

@app.route('/export_csv', methods=['GET'])
def export_csv():
    import csv
    from io import StringIO
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['id', 'auth_code', 'clip_name', 'rt_ms', 'verdict', 'stimulus_frame', 'color_mode', 'game', 'timestamp'])
    results = Result.query.all()
    for r in results:
        writer.writerow([r.id, r.auth_code, r.clip_name, r.rt_ms, r.verdict, r.stimulus_frame, r.color_mode, r.game, r.timestamp])
    output = si.getvalue()
    si.close()
    return output, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=results.csv'}

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)