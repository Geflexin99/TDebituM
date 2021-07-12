from flask import Flask, request
from flask import render_template
import settings,queries 



persons=[]

app = Flask(__name__)
app.config.from_object(settings)


@app.route('/',methods=['GET','POST'])
def person():
    subtdtyp=queries.getallTDSubtype()
    tdtyp=queries.getallTDType()
    Party=queries.getallParty()
    cause=queries.getallCause()
    return render_template('person.html',party=Party,causes=cause, types=tdtyp,subtypes=subtdtyp)

@app.route('/incident',methods=['GET','POST'])
def incident():
    
    return render_template('incident.html')




if __name__=='__main__':
    app.run()
