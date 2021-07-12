from flask import Flask, request
from flask import render_template
import settings,queries 



persons=[]

app = Flask(__name__)
app.config.from_object(settings)


@app.route('/',methods=['GET','POST'])
def template():
   
    tdtyp=queries.getallTDType()
    Party=queries.getallParty()
    cause=queries.getallCause()
    return render_template('formbootstrap01.html',party=Party,causes=cause, types=tdtyp)





if __name__=='__main__':
    app.run()
