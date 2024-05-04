from flask import Flask, request, jsonify, render_template
from pipelines import util

app = Flask(__name__)

# Route for serving the app.html file
@app.route('/')
def app_html():
    return render_template('app.html')

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form['Squareft'])
        location = request.form['uiLocations']
        bhk = int(request.form['uiBHK'])
        bath = int(request.form['uiBathrooms'])

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 400

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)
