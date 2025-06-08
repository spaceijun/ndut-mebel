from flask import Blueprint, render_template, request, jsonify
from validators.katalog_validator import KatalogValidator

katalog_bp = Blueprint('katalog', __name__)

@katalog_bp.route('/katalog')
def katalog_index():
    """Halaman katalog - daftar barang"""
    return render_template('katalog.html')

@katalog_bp.route('/katalog/add')
def add_katalog():
    """Halaman tambah katalog"""
    return render_template('add_katalog.html')

@katalog_bp.route('/katalog/submit', methods=['POST'])
def submit_katalog():
    """Proses submit data katalog"""
    try:
        # Ambil data dari form
        form_data = {
            'kode_barang': request.form.get('kodeBarang'),
            'name_product': request.form.get('nameProduct'),
            'stok': request.form.get('stok'),
            'uom': request.form.get('uom'),
            'status': request.form.get('status')
        }
        
        # Debug: Print form data
        print(f"Katalog form data received: {form_data}")
        
        # Validasi setiap field
        errors = {}
        validated_data = {}
        
        # Validasi Kode Barang
        is_valid, result = KatalogValidator.validate_kode_barang(form_data['kode_barang'])
        if not is_valid:
            errors['kode_barang'] = result
        else:
            # Cek duplikasi kode barang
            if KatalogValidator.check_kode_barang_exists(result):
                errors['kode_barang'] = "Kode barang sudah ada dalam database"
            else:
                validated_data['kode_barang'] = result
        
        # Validasi Name Product
        is_valid, result = KatalogValidator.validate_name_product(form_data['name_product'])
        if not is_valid:
            errors['name_product'] = result
        else:
            validated_data['name_product'] = result
        
        # Validasi Stok
        is_valid, result = KatalogValidator.validate_stok(form_data['stok'])
        if not is_valid:
            errors['stok'] = result
        else:
            validated_data['stok'] = result
        
        # Validasi UOM
        is_valid, result = KatalogValidator.validate_uom(form_data['uom'])
        if not is_valid:
            errors['uom'] = result
        else:
            validated_data['uom'] = result
        
        # Validasi Status
        is_valid, result = KatalogValidator.validate_status(form_data['status'])
        if not is_valid:
            errors['status'] = result
        else:
            validated_data['status'] = result
        
        # Debug: Print validation results
        print(f"Katalog validation errors: {errors}")
        print(f"Katalog validated data: {validated_data}")
        
        # Jika ada error, return dengan pesan error
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        # Pastikan semua data yang diperlukan ada
        required_fields = ['kode_barang', 'name_product', 'stok', 'uom', 'status']
        for field in required_fields:
            if field not in validated_data:
                return jsonify({
                    'success': False,
                    'message': f'Field {field} tidak valid atau kosong'
                }), 400
        
        # Simpan ke database
        success, message = KatalogValidator.insert_katalog(validated_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'kode_barang': validated_data['kode_barang'],
                'redirect': '/katalog?success=true&message=' + message
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 500
    
    except Exception as e:
        print(f"Error in submit_katalog: {e}")
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan pada server: {str(e)}'
        }), 500