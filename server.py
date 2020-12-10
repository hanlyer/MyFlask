# -*- coding: utf-8 -*-
# @Author  : bobo

from flask import Flask
from flask import request
from flask import render_template
import json

app = Flask(__name__)


@app.route("/message/", methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_code = request.form['company_code']

        print('put message %s(%s) into DB' % (company_name, company_code))

        return 'success'

    return 'failed method'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)