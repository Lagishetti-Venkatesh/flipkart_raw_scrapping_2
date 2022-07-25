from flask import Flask, render_template, request
from project_files.main import scrap_the_data

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    review_data = []
    if request.method == 'POST':
        product = request.form['product']

        # getting the reviewed Data
        review_data = scrap_the_data(product)

        review_data = 0 if (review_data is None) else review_data
        if review_data == 0:
           return render_template("error.html")
        return render_template('fetched_data.html', review_data=review_data, product=product)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
