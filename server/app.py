from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from models import Code

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reacto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('reacto.db'):
            db.create_all()
            # Generate initial codes only once
            if Code.query.count() == 0:
                import random
                import string
                codes = set()
                while len(codes) < 100:
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                    codes.add(code)
                for c in codes:
                    db.session.add(Code(code=c))
                db.session.commit()
        else:
            db.create_all()
    # Export unused codes to a .txt file on server launch
    with app.app_context():
        codes = Code.query.filter_by(claimed=False).all()
        with open('valid_codes.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(code.code for code in codes))
        print("Unused codes exported to 'valid_codes.txt'")

    app.run(debug=True, host='0.0.0.0', port=5000)