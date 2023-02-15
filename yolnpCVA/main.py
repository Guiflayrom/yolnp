# Librarys

from src.domain.plate.service import PlateService
from src.domain.cva.service import CVAService
from flask import Flask,send_file, request, Response
from src.infrastructure.plate.ioc import register_ioc
from marshmallow.exceptions import ValidationError
from src.infrastructure.cva.model import CVAModel
from dotenv import load_dotenv
from flask_cors import CORS
from os import getenv
import threading
import json

# Flask Configuration

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

# External Configuration

load_dotenv()
CORS(app,origins=['http://localhost:3000','http://127.0.0.1:3000','http://localhost:8000','http://127.0.0.1:8000',])
register_ioc()
plate_service = PlateService()
cva_service = CVAService()
auth_key = getenv('PROJECT_AUTHORIZATION_KEY')

# Controllers

def auth_valid() -> bool:
    try:
        if request.headers.get('X-API-Key') != auth_key: return False
    except: return False   
    else: return True

@app.route("/cva/start/",methods=['POST'])
def start_cva() -> Response:
    """Create a file called Thread, while this file exist, the the proccess will continue
    """
    if not auth_valid(): return Response(json.dumps({'status':'Not authorized'}),401,mimetype='application/json')    
    try:
        data = CVAModel.Schema().load(dict(request.json.items())) #This is for check if all post params are there, else gonna raise ValidationError
        if not cva_service.is_thread(data): return Response(json.dumps({"status":"instance already running"}), status=400, mimetype='application/json') 
        
        threading.Thread(
            target=cva_service.start_cva_service,
            args=(data,),
            daemon=True
        ).start()

        return Response(json.dumps({'status':'ok'}), status=200, mimetype='application/json')
    
    except ValidationError:
        return Response(json.dumps({"status":"json is not valid"}),status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"status":"something went wrong\n"+str(e)}),status=500, mimetype='application/json')


@app.route("/cva/stop/<camera_id>/",methods=['GET'])
def stop_cva(camera_id) -> Response:
    """It'll delete the Thread file, therefore, stopping the proccess.
    """
    if not auth_valid(): return Response(json.dumps({'status':'Not authorized'}),401,mimetype='application/json')    
    try:
        cva_service.stop_cva_service(camera_id)
    except Exception as e: 
        return Response(json.dumps({"status":"something went wrong"}),status=500, mimetype='application/json')
    return Response(json.dumps({"status":"ok"}), status=200, mimetype='application/json')

@app.route('/cva/camera/<camera_id>/stream/',methods=['GET'])
def get_camerastream(camera_id) -> Response: 
    """It'll read all "frame.jpg", that is generate each frame proccessing
    """
    # if not auth_valid(): return Response(json.dumps({'status':'Not authorized'}),401,mimetype='application/json')    
    return Response(cva_service.get_stream(camera_id),mimetype='multipart/x-mixed-replace; boundary=frame',headers={'X-Frame-Options':'ALLOW-FROM=http://localhost:3000'})

@app.route('/cva/camera/<camera_id>/thumbnail/',methods=['GET'])
def get_mini(camera_id) -> Response:
    """It'll get the last frame
    """
    if not auth_valid(): return Response(json.dumps({'status':'Not authorized'}),401,mimetype='application/json')   
    status,content = cva_service.get_mini(camera_id)
    if status == 200: return send_file(
                content[0],
                mimetype=content[1],
                as_attachment=True,
                download_name=content[2]
            )    
    elif status == 404 or status == 500: return Response(json.dumps(content), status=404, mimetype='application/json')    

# App execution

app.run(host='localhost',port=8061,debug=True)