import os
from flask import Flask, jsonify, render_template, request
from src.timeseries import analyse_history
app=Flask(__name__)
DEMO=[
    {'date':'2026-10-12','resting_hr':68,'hrv_ms':58,'sleep_hours':7.4,'steps':9300,'exercise_minutes':32,'spo2':98},
    {'date':'2026-10-13','resting_hr':69,'hrv_ms':56,'sleep_hours':7.1,'steps':8800,'exercise_minutes':28,'spo2':98},
    {'date':'2026-10-14','resting_hr':70,'hrv_ms':55,'sleep_hours':6.9,'steps':8100,'exercise_minutes':24,'spo2':98},
    {'date':'2026-10-15','resting_hr':71,'hrv_ms':53,'sleep_hours':6.8,'steps':7600,'exercise_minutes':22,'spo2':97},
    {'date':'2026-10-16','resting_hr':72,'hrv_ms':51,'sleep_hours':6.7,'steps':7200,'exercise_minutes':18,'spo2':98},
    {'date':'2026-10-17','resting_hr':73,'hrv_ms':49,'sleep_hours':6.6,'steps':6900,'exercise_minutes':20,'spo2':97},
    {'date':'2026-10-18','resting_hr':74,'hrv_ms':48,'sleep_hours':6.5,'steps':6400,'exercise_minutes':15,'spo2':97},
    {'date':'2026-10-19','resting_hr':76,'hrv_ms':46,'sleep_hours':6.3,'steps':6100,'exercise_minutes':14,'spo2':97},
    {'date':'2026-10-20','resting_hr':75,'hrv_ms':47,'sleep_hours':6.5,'steps':6500,'exercise_minutes':16,'spo2':97},
    {'date':'2026-10-21','resting_hr':77,'hrv_ms':44,'sleep_hours':6.1,'steps':5900,'exercise_minutes':12,'spo2':96},
    {'date':'2026-10-22','resting_hr':78,'hrv_ms':43,'sleep_hours':6.0,'steps':5700,'exercise_minutes':10,'spo2':96},
    {'date':'2026-10-23','resting_hr':79,'hrv_ms':42,'sleep_hours':5.9,'steps':5400,'exercise_minutes':12,'spo2':96},
    {'date':'2026-10-24','resting_hr':80,'hrv_ms':40,'sleep_hours':5.8,'steps':5100,'exercise_minutes':8,'spo2':96},
    {'date':'2026-10-25','resting_hr':81,'hrv_ms':39,'sleep_hours':5.7,'steps':4900,'exercise_minutes':8,'spo2':95},
]
@app.get('/')
def index(): return render_template('index.html')
@app.get('/health')
def health(): return jsonify({'status':'ok','service':'wearable-wellness-dashboard'})
@app.get('/api/demo')
def demo(): return jsonify(analyse_history(42,DEMO))
@app.post('/api/analyse')
def analyse():
    p=request.get_json(silent=True) or {}
    try: result=analyse_history(int(p.get('age',42)),p.get('readings') or [])
    except (TypeError,ValueError) as exc: return jsonify({'error':str(exc)}),400
    return jsonify(result)
from src.advanced import register_advanced
from src.platform import init_platform
register_advanced(app); init_platform(app,'pulselens')
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.getenv('PORT','5000')),debug=os.getenv('FLASK_DEBUG')=='1')
