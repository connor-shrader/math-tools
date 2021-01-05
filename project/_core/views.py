from flask import Blueprint, render_template, redirect, url_for, send_file
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

core = Blueprint('core', __name__, template_folder='templates/_core')

@core.route('/')
def index():
    return render_template('index.html')




