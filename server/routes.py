from flask import request, jsonify
from datetime import datetime
from server.app import app, db
from models import Code, Result

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

@app.route('/generate_codes', methods=['POST'])
def generate_codes():
    import random
    import string
    count = request.get_json().get('count', 100)

    # Clear existing codes
    Code.query.delete()
    db.session.commit()

    # Generate new codes
    codes = set()
    while len(codes) < count:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        codes.add(code)
    for c in codes:
        db.session.add(Code(code=c))
    db.session.commit()
    return jsonify({'success': True, 'message': f'Generated {len(codes)} codes'})

@app.route('/export_codes', methods=['GET'])
def export_codes():
    codes = Code.query.filter_by(claimed=False).all()
    output = '\n'.join(code.code for code in codes)
    return output, 200, {'Content-Type': 'text/plain', 'Content-Disposition': 'attachment; filename=valid_codes.txt'}

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

@app.route('/export_csv', methods=['GET'])
def export_csv():
    import csv
    from io import StringIO
    si = StringIO(newline='')
    writer = csv.writer(si, lineterminator='\n')
    writer.writerow(['id', 'auth_code', 'clip_name', 'rt_ms', 'verdict', 'stimulus_frame', 'color_mode', 'game', 'timestamp'])
    results = Result.query.all()
    for r in results:
        writer.writerow([r.id, r.auth_code, r.clip_name, r.rt_ms, r.verdict, r.stimulus_frame, r.color_mode, r.game, r.timestamp])
    output = si.getvalue()
    si.close()
    return output, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=results.csv'}