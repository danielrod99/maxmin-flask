from flask import Flask, redirect, url_for, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from pulp import *

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
        print(fullData)
        maxomin=fullData['maxomin']
        formaCanonica=fullData['canonica']
        todasRestricciones=fullData['restricciones']
        """
        Resolver por pulp
        """
        x1=LpVariable('x1',lowBound=0,cat='Continuous')
        x2=LpVariable('x2',lowBound=0,cat='Continuous')

        if maxomin=="Maximizar":
            PROBLEMA = LpProblem('test',LpMaximize)
        elif maxomin=="Minimizar":
            PROBLEMA = LpProblem('test',LpMinimize)
        pX1=float(formaCanonica['x1'])
        pX2=float(formaCanonica['x2'])
        
        PROBLEMA+= pX1*x1+pX2*x2

        for x in range(len(todasRestricciones)):
            parte1=float(todasRestricciones[x]["x1"])*x1
            parte2=float(todasRestricciones[x]["x2"])*x2
            resultado=float(todasRestricciones[x]["resultado"])
            if todasRestricciones[x]["igualador"]=="<=":
                PROBLEMA+= parte1 + parte2 <= resultado
            elif todasRestricciones[x]["igualador"]==">=":
                PROBLEMA+= parte1 + parte2 >= resultado
            elif todasRestricciones[x]["igualador"]=="=":
                PROBLEMA+= parte1 + parte2 == resultado

        PROBLEMA.solve()
        resultadoTexto=""
        resultadoTexto+="Resultado:\n"
        cont=0
        for v in PROBLEMA.variables():
            resultadoTexto+=f"{v.name} = {v.varValue}\n"
            #print(v.name,'=',v.varValue)
            if cont==0:
                x1Fobj=v.varValue
                cont+=1
            elif cont==1:
                x2Fobj=v.varValue
        resultadoTexto+=f"Resultado funcion Objetivo: {value(PROBLEMA.objective)}"
        resFobj=value(PROBLEMA.objective)
        resultadoFunObj={"x1":x1Fobj,"x2":x2Fobj,"resultado":resFobj}
        print(resultadoFunObj) ##################################################
        """
        Puntos
        """
        return 'data collected' #aqui se deben de devolver los resultados
if __name__=='__main__':
    app.run(debug=True)