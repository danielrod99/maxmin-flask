from flask import Flask, redirect, url_for, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from pulp import *
import json
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
        #print(fullData)
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
        """
        Puntos
        """
        puntosConRepeticion=[]
        newPuntos=[]
        todosPuntos=[]
        for otherX in range(len(todasRestricciones)):
            a=float(todasRestricciones[otherX]["x1"])
            b=float(todasRestricciones[otherX]["x2"])
            c=float(todasRestricciones[otherX]["resultado"])
            if a!=0:
                paraX=[(c/a),0]
                puntosConRepeticion.append(paraX)
            if b!=0:
                paraY=[0,(c/b)]
                puntosConRepeticion.append(paraY)
            for another in range(len(todasRestricciones)):
                d=float(todasRestricciones[another]["x1"])
                e=float(todasRestricciones[another]["x2"])
                f=float(todasRestricciones[another]["resultado"])
                if otherX != another:
                    #sacar puntos
                    g = a * e - b * d
                    if g==0:
                        return 'Inderterminacion'
                    x=(c*e-b*f)/g
                    y=(a*f-c*d)/g
                    soloUno=[]
                    soloUno.append(x)
                    soloUno.append(y)
                    puntosConRepeticion.append(soloUno)
        for a in range(len(puntosConRepeticion)):
            for b in range(len(puntosConRepeticion)):
                if a!=b and puntosConRepeticion[a][0]==puntosConRepeticion[b][0] and puntosConRepeticion[a][1]==puntosConRepeticion[b][1] and puntosConRepeticion[b][0]!=-1 and puntosConRepeticion[b][1]!=-1:
                    puntosConRepeticion[b][0]=-1
                    puntosConRepeticion[b][1]=-1
        for a in range(len(puntosConRepeticion)):
            if puntosConRepeticion[a][0]!=-1 and puntosConRepeticion[a][1]!=-1:
                todosPuntos.append(puntosConRepeticion[a]) 
        exito=True
        for another in range(len(todosPuntos)):
            for otherX in range(len(todasRestricciones)):
                a=float(todasRestricciones[otherX]["x1"])
                b=float(todasRestricciones[otherX]["x2"])
                igual=todasRestricciones[otherX]["igualador"]
                c=float(todasRestricciones[otherX]["resultado"])
                resu=(a*todosPuntos[another][0])+(b*todosPuntos[another][1])
                if igual==">=":
                    if resu>=c:
                        exito=True
                    else:
                        exito=False
                        break
                elif igual=="<=":
                    if resu<=c:
                        exito=True
                    else:
                        exito=False
                        break
                elif igual=="=":
                    if resu==c:
                        exito=True
                    else:
                        exito=False
                        break  
            if exito:
                newPuntos.append(todosPuntos[another])
        """
        Graficar
        """
        maxX=20.0
        maxY=20.0
        for otherX in range(len(todasRestricciones)):
            theX1=float(todasRestricciones[otherX]["x1"])
            theX2=float(todasRestricciones[otherX]["x2"])
            resul=float(todasRestricciones[otherX]["resultado"])
            if theX2!=0.0:
                maximoEnY=(resul/theX2)+((theX1/theX2)*-1)
                if maximoEnY>maxY:
                    maxY=int(maximoEnY)+10
            if theX1!=0.0:
                maximoEnX=(resul/theX1)+((theX2/theX1)*-1)
                if maximoEnX>maxX:
                    maxX=int(maximoEnX)+10

        x = np.linspace(0, maxX, 2000)
        allYs=[]
        posi=0
        for otherX in range(len(todasRestricciones)):
            resul=float(todasRestricciones[otherX]["resultado"])
            rX1=float(todasRestricciones[otherX]["x1"])*-1
            rX2=float(todasRestricciones[otherX]["x2"])
            if rX2!=0.0:
                operacion=(resul/rX2)+((rX1/rX2)*x)
                allYs.append(operacion)
                simbolo=todasRestricciones[otherX]["igualador"]
                plt.plot(x, operacion, label=f"{str(rX1*-1)}X1+{str(rX2)}X2{simbolo}{str(resul)}")
                if simbolo=="<=":
                    plt.fill_between(x, operacion, where=operacion<=operacion, alpha=0.5)
                elif simbolo==">=":
                    plt.fill_between(x, operacion, where=operacion>=operacion, alpha=0.5)
            else:
                posi=0
                operacion=np.arange(2000)*0
                resultado=resul/(rX1*-1)
                for b in range(len(x)):
                    if resultado==x[b]:
                        operacion[b]=maxY
                        posi=b
                        break
                    if x[b]>resultado and b!=0:
                        operacion[b-1]=maxY
                        posi=b-1
                        break

                for c in range(len(operacion)):
                    if simbolo == "<=":
                        if c>=posi:
                            operacion[c]=maxY
                    elif simbolo == ">=":
                        if c<=posi:
                            operacion[c]=maxY
                allYs.append(operacion)
                plt.plot(x, operacion, label=f"{str(rX1*-1)}X1+{str(rX2)}X2={str(resul)}")
                if simbolo=="<=":
                    plt.fill_between(x, operacion, where=operacion<=operacion, alpha=0.5)
                elif simbolo==">=":
                    plt.fill_between(x, operacion, where=operacion>=operacion, alpha=0.5)
        plt.xlim((0, maxX))
        plt.ylim((0, maxY))
        pX1=float(formaCanonica['x1'])
        pX2=float(formaCanonica['x2'])
        if pX2!=0.0:
            funcionObjetivo=(resFobj/pX2)+(((pX1*-1)/pX2)*x)
        else:
            funcionObjetivo=np.arange(2000)*0
        plt.plot(x,funcionObjetivo,color="black", label=f"Fun. Obj:{str(pX1)}X1+{str(pX2)}X2={str(resFobj)}")
        plt.xlabel('X1')
        plt.ylabel('X2')
        puntos="Puntos:\n"
        for a in range(len(newPuntos)):
            plt.scatter(newPuntos[a][0],newPuntos[a][1], color="#333333")
            puntos+=f"[ {newPuntos[a][0]} , {newPuntos[a][1]} ]\n"
        plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
        plt.savefig('grafica.png')
        """
        Fin Grafica
        """
        resultados={"resFunObj":resultadoFunObj,"puntos": newPuntos}
        print(resultados)
        return json.dumps(resultados)
if __name__=='__main__':
    app.run(debug=True)