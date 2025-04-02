from flask import Flask,render_template,jsonify
import http.client
import json

app = Flask(__name__)


@app.route('/get-covid-data')
def get_covid_data():
    try:
        conn = http.client.HTTPSConnection("covid-193.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': "5fafa80fbbmsh2a1f576e6ce1b1dp18adcdjsnbd3633751711",
            'x-rapidapi-host': "covid-193.p.rapidapi.com"
        }
        
        conn.request("GET", "/statistics", headers=headers)
        
        res = conn.getresponse()
        data = res.read()
        
        # Parse the response as a string
        data_str = data.decode('utf-8')
        
        # Replace NaN values with null before parsing as JSON
        data_str = data_str.replace('NaN', 'null')
        
        j = json.loads(data_str)
        
        # Get the response data directly
        covid_data = j['response']
        
        return jsonify({
            'status': 'success',
            'data': covid_data,
            'count': len(covid_data)
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/')
def home():
    return render_template('index.html', title='COVID-19 Data')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 