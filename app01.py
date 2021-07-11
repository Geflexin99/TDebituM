from flask import Flask, request
from flask import render_template
from werkzeug.utils import redirect
import settings,json, utils 



persons=[]

app = Flask(__name__)
app.config.from_object(settings)


@app.route('/',methods=['GET','POST'])
def template():
   
    discipline=[
        'Mechanic',
        'Electronics',
        'Software'
        ]
    
    return render_template('formbootstrap01.html',data=discipline)





if __name__=='__main__':
    app.run()
