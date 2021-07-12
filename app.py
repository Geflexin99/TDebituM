from flask import Flask, request
from flask import render_template
import settings,queries 



persons=[]

app = Flask(__name__)
app.config.from_object(settings)
users=[]

@app.route('/',methods=['GET','POST'])
def person():
    print(request.method)
    Party=queries.getallParty()
    
    return render_template('person.html',party=Party)

@app.route('/incident',methods=['POST'])
def incident():
    personNumber=request.form.get('personNumber')
    personPosition=request.form.get('personPosition')
    discipline=request.form.get('discipline')
    leadingPosition=request.form.get('leadingPosition')
    experience=request.form.get('experience')
    person={'number':personNumber,'position':personPosition, 'party':discipline,'leadingposition':leadingPosition,'experience':experience }
    persons.append(person)
    print(persons)
    cause=queries.getallCause()
    subtdtyp=queries.getallTDSubtype()
    tdtyp=queries.getallTDType()
    return render_template('incident.html',causes=cause, types=tdtyp,subtypes=subtdtyp)

if __name__=='__main__':
    app.run()
