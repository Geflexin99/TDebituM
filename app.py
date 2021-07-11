from flask import Flask, request
from flask import render_template
from werkzeug.utils import redirect
import settings,json, utils,queries 



persons=[]

app = Flask(__name__)
app.config.from_object(settings)


@app.route('/',methods=['GET','POST'])
def template():
   
    tdtyp=queries.getallTDType()
    Party=queries.getallParty()
    return render_template('formbootstrap01.html',party=Party)





if __name__=='__main__':
    app.run()
