from flask import Blueprint, render_template, request, jsonify
from validators.material_validator import MaterialValidator
from models.database_manager import DatabaseManager

# Pastikan blueprint dibuat dengan benar
material_bp = Blueprint('material', __name__, url_prefix='/material')

@material_bp.route('/')
def material_index():
    """Halaman material - daftar material"""
    return render_template('material.html')

@material_bp.route('/add')
def add_material():
    """Halaman tambah material"""
    return render_template('add_material.html')

@material_bp.route('/submit', methods=['POST'])
def submit_material():
    """Proses submit data material"""
    try:
        # Ambil data dari form
        form_data = {
            'level': request.form.get('level'),
            'part_code': request.form.get('partCode'),
            'description': request.form.get('description'),
            'lot_size': request.form.get('lotSize'),
            'uom': request.form.get('uom'),
            'status': request.form.get('status')
        }
        
        # Debug: Print form data
        print(f"Form data received: {form_data}")
        
        # Validasi setiap field
        errors = {}
        validated_data = {}
        
        # Validasi Level
        is_valid, result = MaterialValidator.validate_level(form_data['level'])
        if not is_valid:
            errors['level'] = result
        else:
            validated_data['level'] = result
        
        # Validasi Part Code
        is_valid, result = MaterialValidator.validate_part_code(form_data['part_code'])
        if not is_valid:
            errors['part_code'] = result
        else:
            # Cek duplikasi part code hanya jika validasi format berhasil
            if DatabaseManager.check_part_code_exists(result):
                errors['part_code'] = "Part code sudah ada dalam database"
            else:
                validated_data['part_code'] = result
        
        # Validasi Description
        is_valid, result = MaterialValidator.validate_description(form_data['description'])
        if not is_valid:
            errors['description'] = result
        else:
            validated_data['description'] = result
        
        # Validasi Lot Size
        is_valid, result = MaterialValidator.validate_lot_size(form_data['lot_size'])
        if not is_valid:
            errors['lot_size'] = result
        else:
            validated_data['lot_size'] = result
        
        # Validasi UOM
        is_valid, result = MaterialValidator.validate_uom(form_data['uom'])
        if not is_valid:
            errors['uom'] = result
        else:
            validated_data['uom'] = result
        
        # Validasi Status
        is_valid, result = MaterialValidator.validate_status(form_data['status'])
        if not is_valid:
            errors['status'] = result
        else:
            validated_data['status'] = result
        
        # Debug: Print validation results
        print(f"Validation errors: {errors}")
        print(f"Validated data: {validated_data}")
        
        # Jika ada error, return dengan pesan error
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        # Pastikan semua data yang diperlukan ada
        required_fields = ['level', 'part_code', 'description', 'lot_size', 'uom', 'status']
        for field in required_fields:
            if field not in validated_data:
                return jsonify({
                    'success': False,
                    'message': f'Field {field} tidak valid atau kosong'
                }), 400
        
        # Simpan ke database
        success, message = DatabaseManager.insert_material(validated_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'part_code': validated_data['part_code'],
                'redirect': '/material?success=true&message=' + message
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 500
    
    except Exception as e:
        print(f"Error in submit_material: {e}")
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan pada server: {str(e)}'
        }), 500

# Route tambahan untuk debugging
@material_bp.route('/test')
def test_route():
    """Route untuk testing blueprint"""
    return "Material blueprint is working!"