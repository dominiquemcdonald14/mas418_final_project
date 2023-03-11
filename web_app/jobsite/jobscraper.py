from flask import Flask, render_template, request



app = Flask(__name__)

@app.route('/home')
def home_page():
	return render_template('home.html')


@app.route('/recommender')
def rec_page():
	return render_template('recommender.html')


@app.route('/recommender/result')
def rec_result_page():
	return render_template('recommender_result.html')

@app.route('/summary')	
def summ_page():
		return render_template('summary.html')


if __name__ == '__main__':
	app.run(debug = True)