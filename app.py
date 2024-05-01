from flask import Flask, request, jsonify, render_template
from pipelines import util

app = Flask(__name__)


# Route for serving the app.html file
@app.route('/')
def app_html():
    return render_template('app.html')

# Route for the root URL
# @app.route('/')
# def index():
#     # URLs to be displayed
#     urls_message = "API Endpoints:<br>"\
#                    "1. Get Location Names: <a href='/get_location_names'>/get_location_names</a><br>"\
#                    "2. Predict Home Price: <a href='/predict_home_price'>/predict_home_price</a><br>"\
#                    "3. Web Applications: <a href='/app.html'>/app.html</a><br>"

#     # Return welcome message with URLs
#     return "Welcome to Home Price Prediction Server<br>" + urls_message

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
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

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
    app.run()


