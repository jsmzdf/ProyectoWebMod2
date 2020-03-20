import csv
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from numpy.core._multiarray_umath import ndarray
import ML
import Estadistica
import Arreglar

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html', methods=['GET', 'POST'])
def rindex():
    if request.method == 'POST':
        return render_template('index.html')


@app.route('/Visualizacion.html', methods=['GET', 'POST'])
def data():
    try:
        df = pd.DataFrame(request.files['files'])
        df.to_csv('pruebaas.csv', index=False)
        dfc = pd.read_csv('pruebaas.csv', sep=',', header=None)
        cv = Arreglar.arre(df).reparaCSV()
        print(type(cv['fixedacidity'][0]))
        Estadistica.Estadis(cv)
        p = pd.DataFrame(Estadistica.Estadis(cv).varPorItem().T, columns=cv.columns, index=['Varianza'])
        print(p)
        p1 = Estadistica.Estadis(cv).calcularVarPorRegistro()
        p2: ndarray = Estadistica.Estadis(cv).corrIteTest()
        p3 = Estadistica.Estadis(cv).correIteTestCorreg()
        p4 = Estadistica.Estadis(cv).calculardesviacion()
        p5 = Estadistica.Estadis(cv).calcularVarianza()
        p7 = Estadistica.Estadis(cv).calcularCovarianza()
        p8 = Estadistica.Estadis(cv).calcularCorrela()
        p6 = Estadistica.Estadis(cv).calcularMedia()
        p9 = Estadistica.Estadis(cv).mostrarResumen()
        print(p2)
        print(p3)
        print(p9)

        return render_template('Visualizacion.html', tables=[p.to_html(classes='data', header="true")],
                               tables1=[pd.DataFrame(p2.T, index=cv.columns, columns=['IH']).to_html(classes='data',
                                                                                                     header="true")],
                               tables2=[pd.DataFrame(p3.T, index=cv.columns, columns=['IHC']).to_html(classes='data',
                                                                                                      header="true")],
                               tables3=[pd.DataFrame(p8.T, index=cv.columns, columns=cv.columns).to_html(classes='data',
                                                                                                         header="true")],
                               tables4=[pd.DataFrame(p9).to_html(classes='data', header="true")],
                               data=cv.to_html())
    except:
        dfc = pd.read_csv('pruebaas.csv', sep=',', header=None)
        cv = Arreglar.arre(dfc).reparaCSV()

        Estadistica.Estadis(cv)
        p = pd.DataFrame(Estadistica.Estadis(cv).varPorItem().T, columns=cv.columns, index=['Varianza'])

        Estadistica.Estadis(cv).calcularVarPorRegistro()
        p2: ndarray = Estadistica.Estadis(cv).corrIteTest()
        p3 = Estadistica.Estadis(cv).correIteTestCorreg()
        Estadistica.Estadis(cv).calculardesviacion()
        Estadistica.Estadis(cv).calcularVarianza()
        Estadistica.Estadis(cv).calcularCovarianza()
        p8 = Estadistica.Estadis(cv).calcularCorrela()
        Estadistica.Estadis(cv).calcularMedia()
        p9 = Estadistica.Estadis(cv).mostrarResumen()
        return render_template('Visualizacion.html', tables=[p.to_html(classes='data', header="true")],
                               tables1=[pd.DataFrame(p2.T, index=cv.columns, columns=['IH']).to_html(classes='data',
                                                                                                     header="true")],
                               tables2=[pd.DataFrame(p3.T, index=cv.columns, columns=['IHC']).to_html(classes='data',
                                                                                                      header="true")],
                               tables3=[pd.DataFrame(p8.T, index=cv.columns, columns=cv.columns).to_html(classes='data',
                                                                                                         header="true")],
                               tables4=[pd.DataFrame(p9).to_html(classes='data', header="true")],
                               data=cv.to_html())


@app.route('/ML.html', methods=['POST','GET'])
def ml():
    if request.method == 'POST'  :
        mf = pd.DataFrame(np.zeros((3, 5)))
        dfc = pd.read_csv('pruebaas.csv', sep=',', header=None)
        cv = Arreglar.arre(dfc).reparaCSV()
        sem = request.form.get('semilla')
        press = request.form.get('pres')
        tess = request.form.get('tes')
        if request.form.get('ann'):
            mf, ps, rcs, f1sc, acs, s = ML.Proceso(cv, float(sem), float(press),float(tess), ML.Proceso.ann()).it()
        if request.form.get('knn'):
            mf, ps, rcs, f1sc, acs, s = ML.Proceso(cv,float(sem), float(press),float(tess), ML.Proceso.KNN()).it()
        if request.form.get('svc'):
            mf, ps, rcs, f1sc, acs, s = ML.Proceso(cv, float(sem), float(press),float(tess), ML.Proceso.svc()).it()
        if request.form.get('lg'):
            mf, ps, rcs, f1sc, acs, s = ML.Proceso(cv, float(sem), float(press),float(tess), ML.Proceso.LG()).it()
        return render_template('ML.html', data=pd.DataFrame(mf).to_html(),
                               tables=[pd.DataFrame(ps).to_html(classes='data', header="true")],
                               tables1=[pd.DataFrame(rcs).to_html(classes='data', header="true")],
                               tables2=[pd.DataFrame(f1sc).to_html(classes='data', header="true")],
                               tables3=[pd.DataFrame([acs,s],index=["acuary","score"]).to_html(classes='data', header="true")],)




@app.route('/InfoData')
def infodata():
    return 'info data'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
