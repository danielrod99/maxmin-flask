from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/informacion')
def informacion():
    return "<h1>Hola</h1>"
@app.route('/calcular', methods=['GET','POST'])
def calcular():
    if request.method== 'POST':
        fullData=request.get_json()
        formaCanonica=fullData['canonica']
        todasRestricciones=fullData['restricciones']
        print(formaCanonica)
        print(todasRestricciones)
        return 'data collected' #aqui se deben de devolver los resultados
if __name__=='__main__':
    app.run(debug=True)