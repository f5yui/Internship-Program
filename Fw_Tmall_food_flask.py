import function
from flask import Flask
from flask import render_template

app = Flask(__name__)


# @app.route('/fw/food')
@app.route('/')
def index():
    food_info, base_info = function.get_data()
    rec3_info = function.rec3_data()
    return render_template('Fw_food.html', base_info_html=base_info, rec3_info_html=rec3_info)


@app.route('/<index>')
def food_index(index):
    main_info = function.use_data(index)
    rec_info, rec2_info = function.rec_data(index)
    return render_template('Fw_food1.html', main_info_html=main_info, rec_info_html=rec_info, rec2_info_html=rec2_info)
