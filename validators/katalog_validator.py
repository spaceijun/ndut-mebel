import re
import mysql.connector
from mysql.connector import Error
from config.database import DB_CONFIG

class KatalogValidator:
    # Stok Barang
    @staticmethod
    def validate_stok(stok):
        """Validasi stok (angka positif)"""
        try:
            stok = int(stok)
            if stok <= 0:
                return False, "Stok harus lebih dari 0"
            if stok > 9999:
                return False, "Stok maksimal 9999"
            return True, stok
        except (ValueError, TypeError):
            return False, "Stok harus berupa angka"

    # Kode Barang
    @staticmethod
    def validate_kode_barang(kode_barang):
        """Validasi kode barang (huruf kapital dan angka, maks 20 karakter)"""
        if not kode_barang or len(kode_barang.strip()) == 0:
            return False, "Kode Barang tidak boleh kosong"
        
        kode_barang = kode_barang.strip().upper()
        if len(kode_barang) > 20:
            return False, "Kode Barang maksimal 20 karakter"
        
        if not re.match(r'^[A-Z0-9]+$', kode_barang):
            return False, "Kode Barang hanya boleh huruf kapital dan angka"
        
        return True, kode_barang

    # Validation Produk Name
    @staticmethod
    def validate_name_product(name_product):
        """Validasi Nama Produk (tidak kosong, maks 200 karakter)"""
        if not name_product or len(name_product.strip()) == 0:
            return False, "Nama Produk tidak boleh kosong"
        
        name_product = name_product.strip()
        if len(name_product) > 200:
            return False, "Nama Produk maksimal 200 karakter"
        
        return True, name_product

    # Validation UOM
    @staticmethod
    def validate_uom(uom):
        """Validasi UOM"""
        valid_uoms = ['Pcs', 'Log', 'Kg', 'Ltr', 'M', 'M2', 'M3', 'Set', 'Box', 'Roll']
        if uom not in valid_uoms:
            return False, f"UOM harus salah satu dari: {', '.join(valid_uoms)}"
        return True, uom

    # Validation Status
    @staticmethod
    def validate_status(status):
        """Validasi status"""
        valid_statuses = ['Tersedia', 'Tidak Tersedia']
        if status not in valid_statuses:
            return False, f"Status harus salah satu dari: {', '.join(valid_statuses)}"
        return True, status

    # Tambahan method untuk validasi kode barang sudah ada di database
    @staticmethod
    def check_kode_barang_exists(kode_barang):
        """Cek apakah kode barang sudah ada"""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM katalog WHERE kode_barang = %s", (kode_barang,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"Error checking kode barang: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # Method untuk insert data katalog
    @staticmethod
    def insert_katalog(data):
        """Insert data katalog ke database"""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            query = """
                INSERT INTO katalog (kode_barang, name_product, stok, uom, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                data['kode_barang'],
                data['name_product'],
                data['stok'],
                data['uom'],
                data['status']
            )
            
            cursor.execute(query, values)
            connection.commit()
            return True, "Data berhasil disimpan"
        
        except Error as e:
            if connection.is_connected():
                connection.rollback()
            print(f"Error inserting katalog data: {e}")
            if "Duplicate entry" in str(e):
                return False, "Kode barang sudah ada dalam database"
            elif "Data too long" in str(e):
                return False, "Data terlalu panjang untuk field yang ditentukan"
            return False, f"Gagal menyimpan data ke database: {str(e)}"
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # Method untuk get all katalog
    @staticmethod
    def get_all_katalog():
        """Ambil semua data katalog"""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, kode_barang, name_product, stok, uom, status, 
                       created_at, updated_at
                FROM katalog 
                ORDER BY created_at DESC
            """)
            katalogs = cursor.fetchall()
            
            # Convert datetime objects to string for JSON serialization
            for katalog in katalogs:
                if katalog.get('created_at'):
                    katalog['created_at'] = katalog['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                if katalog.get('updated_at'):
                    katalog['updated_at'] = katalog['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
            
            return katalogs
        except Error as e:
            print(f"Error fetching katalogs: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()