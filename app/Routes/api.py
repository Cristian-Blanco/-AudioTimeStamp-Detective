from flask import request
from app import app
from app.Controllers import AudioDetectionController, AudioStorageController, StoredAudioDetectionController
from app.Middleware import AudioDetectionMiddleware, AudioStorageMiddleware, StoredAudioDetectionMiddleware, OptionalInputMiddleware
from app.Utils import ResponseHttp

@app.before_request
def before_request():
    endpoint_middlewares = {
        'audio_detection': (OptionalInputMiddleware, AudioDetectionMiddleware),
        'audio_storage': (AudioStorageMiddleware,),
        'stored_audio_detection': (OptionalInputMiddleware, StoredAudioDetectionMiddleware)
    }
    endpoint = request.endpoint
    middlewares = endpoint_middlewares.get(endpoint, ())

    for middleware in middlewares:
        result = middleware.invokable(request=request)
        if result['error']:
            return ResponseHttp.error_message(message=result['message'], status_code=400)
    
@app.route('/audio-detection', methods=['POST'])
def audio_detection():
    return AudioDetectionController.invokable(request=request)

@app.route('/audio-storage', methods=['POST'])
def audio_storage():
    return AudioStorageController.invokable(request=request)

@app.route('/stored-audio-detection', methods=['POST'])
def stored_audio_detection():
    return StoredAudioDetectionController.invokable(request=request)