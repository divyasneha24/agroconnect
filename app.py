from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:SQL@localhost:3306/agroconnect'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class MSP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50), nullable=False)
    commodity = db.Column(db.String(100), nullable=False)
    msprice = db.Column(db.Float, nullable=False)

class ProductPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    APMC = db.Column(db.String(50), nullable=False)
    max_price = db.Column(db.Float, nullable=False)
    min_price = db.Column(db.Float, nullable=False)
# Routes
@app.route('/msp', methods=['GET'])
def get_msp():
    region = request.args.get('region')
    print(region)
    if not region:
        return jsonify({'error': 'Region parameter is required'}), 400
    
    msp_data = MSP.query.filter_by(region=region).all()
    # for msp in msp_data : 
    #     print(msp)
    results = [{'price': msp.msprice,'crop': msp.commodity} for msp in msp_data]
    return jsonify(results)

@app.route('/compare', methods=['GET'])
def compare_prices():
    product = request.args.get('product')
    print(product)
    if not product:
        return jsonify({'error': 'Product parameter is required'}), 400
    
    price_data = ProductPrice.query.filter_by(product=product).all()
    results = [{'region': price.APMC, 'price': price.min_price} for price in price_data]
    return jsonify(results)


# Database Initialization
@app.cli.command('initdb')
def initdb():
    db.create_all()

    # Load CSV files (Ensure correct path in Windows)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    msp_file_path = os.path.join(base_dir, 'CMO_MSP_Mandi.csv')
    price_file_path = os.path.join(base_dir, 'Monthly_data_cmo.csv')

    # Load MSP data
    if os.path.exists(msp_file_path):
        msp_data = pd.read_csv(msp_file_path)
        for _, row in msp_data.iterrows():
            db.session.add(MSP(region="Unknown", crop=row['commodity'], price=row['msprice']))
    
    # Load ProductPrice data
    if os.path.exists(price_file_path):
        price_data = pd.read_csv(price_file_path)
        for _, row in price_data.iterrows():
            db.session.add(ProductPrice(product=row['Commodity'], APMC=row['state_name'], price=row['max_price']))
    

    db.session.commit()
    print('Database initialized with CSV data.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
