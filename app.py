from flask import Flask, request
from flask import render_template
from werkzeug.utils import redirect
import settings,json, utils 



persons=[]

app = Flask(__name__)
app.config.from_object(settings)


@app.route('/',methods=['GET','POST'])
def template():
    if request.method =='POST':
        discipline=[
            'Mechanic',
            'Electronics',
            'Software'
        ]
        personNumber= request.form.get('personNumber')
        personPosition=request.form.get('personPosition')
        person ={'personNumber':personNumber,'personPosition':personPosition}
        persons.append(person)
        print(persons)
        return render_template('formbootstrap01.html',data=discipline)
    return render_template('formbootstrap01.html')





if __name__=='__main__':
    app.run()
