from flask import Blueprint, jsonify, request
from .forecast import project_history

def register_advanced(app):
    bp=Blueprint('pulselens_advanced',__name__)
    @bp.post('/api/forecast')
    def forecast():
        p=request.get_json(silent=True) or {}; rows=p.get('readings') or []
        try: result=project_history(rows,p.get('days',7))
        except (ValueError,TypeError,KeyError) as exc: return jsonify({'error':str(exc)}),400
        return jsonify(result)
    app.register_blueprint(bp)
