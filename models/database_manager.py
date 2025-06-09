import mysql.connector
from mysql.connector import Error
from config.database import DB_CONFIG

class DatabaseManager:
    @staticmethod
    def get_connection():
        """Membuat koneksi ke database"""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None
    
    @staticmethod
    def create_users_table():
        """Create users table if not exists"""
        try:
            connection = DatabaseManager.get_connection()
            if not connection:
                print("Failed to connect to database")
                return False
                
            cursor = connection.cursor()
            
            create_table_query = """
            CREATE TABLE IF NOT EXISTS `users` (
              `id` int NOT NULL AUTO_INCREMENT,
              `name` varchar(100) NOT NULL,
              `email` varchar(100) NOT NULL,
              `password` varchar(255) NOT NULL,
              `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              UNIQUE KEY `unique_email` (`email`),
              KEY `idx_email` (`email`),
              KEY `idx_created_at` (`created_at`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """
            
            cursor.execute(create_table_query)
            connection.commit()
            cursor.close()
            connection.close()
            
            print("Users table created successfully")
            return True
            
        except Exception as e:
            print(f"Error creating users table: {e}")
            return False
    
    @staticmethod
    def check_part_code_exists(part_code):
        """Cek apakah part code sudah ada"""
        connection = DatabaseManager.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM materials WHERE part_code = %s", (part_code,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"Error checking part code: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    @staticmethod
    def insert_material(data):
        """Insert data material ke database"""
        connection = DatabaseManager.get_connection()
        if not connection:
            return False, "Gagal terhubung ke database"
        
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO materials (level, part_code, description, lot_size, uom, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                data['level'],
                data['part_code'],
                data['description'],
                data['lot_size'],
                data['uom'],
                data['status']
            )
            
            cursor.execute(query, values)
            connection.commit()
            return True, "Data berhasil disimpan"
        
        except Error as e:
            if connection.is_connected():
                connection.rollback()
            print(f"Error inserting data: {e}")
            if "Duplicate entry" in str(e):
                return False, "Part code sudah ada dalam database"
            elif "Data too long" in str(e):
                return False, "Data terlalu panjang untuk field yang ditentukan"
            return False, f"Gagal menyimpan data ke database: {str(e)}"
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    @staticmethod
    def get_all_materials():
        """Ambil semua data material"""
        connection = DatabaseManager.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, level, part_code, description, lot_size, uom, status, 
                       created_at, updated_at
                FROM materials 
                ORDER BY created_at DESC
            """)
            materials = cursor.fetchall()
            
            # Convert datetime objects to string for JSON serialization
            for material in materials:
                if material.get('created_at'):
                    material['created_at'] = material['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                if material.get('updated_at'):
                    material['updated_at'] = material['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
            
            return materials
        except Error as e:
            print(f"Error fetching materials: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    @staticmethod
    def get_material_by_id(material_id):
        """Ambil data material berdasarkan ID"""
        connection = DatabaseManager.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, level, part_code, description, lot_size, uom, status, 
                       created_at, updated_at
                FROM materials 
                WHERE id = %s
            """, (material_id,))
            material = cursor.fetchone()
            
            if material:
                # Convert datetime objects to string
                if material.get('created_at'):
                    material['created_at'] = material['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                if material.get('updated_at'):
                    material['updated_at'] = material['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
            
            return material
        except Error as e:
            print(f"Error fetching material by ID: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()