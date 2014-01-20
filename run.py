import os
from flask import Flask,  render_template, flash, redirect, url_for, request, send_file
from py_reflection import PKGModuleReflection

app = Flask(__name__)

@app.route('/<pkg_name>')
def index(pkg_name):
    cr = PKGModuleReflection(pkg_name)
    #cr.class_tree.debug()
    #cr.class_tree.print_map(map_func=ClassNode.dump)
    data = cr.class_tree.get_json_d3(root_name='INICIO')
    return render_template('d3tree.html', data = data)

    
app.run(host='0.0.0.0', port=8080, debug=True)
