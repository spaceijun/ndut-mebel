from flask import Blueprint, jsonify
from models.database_manager import DatabaseManager
from validators.katalog_validator import KatalogValidator

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/materials')
def api_materials():
    """API endpoint untuk mendapatkan data material"""
    materials = DatabaseManager.get_all_materials()
    return jsonify({
        'success': True,
        'data': materials,
        'count': len(materials)
    })

@api_bp.route('/material/<int:material_id>')
def api_material_detail(material_id):
    """API endpoint untuk mendapatkan detail material berdasarkan ID"""
    material = DatabaseManager.get_material_by_id(material_id)
    if material:
        return jsonify({
            'success': True,
            'data': material
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Material tidak ditemukan'
        }), 404

@api_bp.route('/katalogs')
def api_katalogs():
    """API endpoint untuk mendapatkan data katalog"""
    katalogs = KatalogValidator.get_all_katalog()
    return jsonify({
        'success': True,
        'data': katalogs,
        'count': len(katalogs)
    })