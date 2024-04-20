from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS from flask_cors
from ETL import ETL
from ML_Model import Model

try:
    elt = ETL()
    print('Load ETL Successfully')
except KeyError as e:
    raise(f'Error from initializing : {e}')



app = Flask(__name__)
CORS(app, origins=["*"])



@app.route('/')
def hello():
    return 'Hello, World!'



@app.route('/query', methods=['POST'])
def query():
    if request.method == 'POST':
        data = request.json  
        query_value = data.get('query', None)
        if query_value is not None:

            model = Model('./files/best_model.pkl')

            sql_data = {'table': 'rawdata', 'db_name': 'data_warehouse', 'UniqueID': query_value}
            df = elt.transform(document_type='sql', sql_data=sql_data)
            df = df.drop(columns=['DISBURSAL_DATE','DATE_OF_BIRTH','STATE_ID','EMPLOYEE_CODE_ID','PRI_NO_OF_ACCTS','PRI_SANCTIONED_AMOUNT','SEC_NO_OF_ACCTS','SEC_CURRENT_BALANCE','SEC_SANCTIONED_AMOUNT','SUPPLIER_ID','BRANCH_ID','MANUFACTURER_ID','CURRENT_PINCODE_ID'])
            prediction = model.predict(df)
            prediction = prediction.tolist()
            rawdata = df[['DISBURSED_AMOUNT','AGE','LTV','PERFORM_CNS_SCORE_DESCRIPTION','NO_OF_INQUIRIES','CREDIT_HISTORY_LENGTH','ASSET_COST']].to_dict(orient='records')
           
            return jsonify({'result': prediction,'rawdata':rawdata}), 200
        else:
            return jsonify({'error': 'No query provided'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)