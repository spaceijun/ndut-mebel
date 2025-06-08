from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
import logging
import sys
import traceback

# Load environment variables
load_dotenv()

# Setup logging dengan encoding yang tepat untuk Windows
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app_debug.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    logger.info("Starting Flask application...")
    
    # Test database connection saat startup
    try:
        logger.info("Testing database connection...")
        from models.database_manager import DatabaseManager
        
        # Test connection
        connection = DatabaseManager.get_connection()
        if connection:
            logger.info("[OK] Database connection successful")
            connection.close()
        else:
            logger.error("[ERROR] Database connection failed")
            
    except Exception as e:
        logger.error(f"[ERROR] Database connection test failed: {e}")
        logger.error(traceback.format_exc())
    
    # Register blueprints with error handling
    try:
        logger.info("Registering blueprints...")
        
        # PERBAIKAN: Import dari file yang benar
        try:
            from routes.material import material_bp  # Jika file bernama material.py
            app.register_blueprint(material_bp)
            logger.info("[OK] Material blueprint registered")
        except ImportError:
            try:
                from routes.material_routes import material_bp  # Jika file bernama material_routes.py
                app.register_blueprint(material_bp)
                logger.info("[OK] Material blueprint registered")
            except ImportError as e:
                logger.error(f"Failed to import material blueprint: {e}")
                logger.error("Expected file: routes/material.py or routes/material_routes.py")
        
        # Blueprint lainnya (opsional)
        try:
            from routes.katalog_routes import katalog_bp
            app.register_blueprint(katalog_bp)
            logger.info("[OK] Katalog blueprint registered")
        except ImportError as e:
            logger.warning(f"Katalog blueprint not found: {e}")
        
        try:
            from routes.api_routes import api_bp
            app.register_blueprint(api_bp)
            logger.info("[OK] API blueprint registered")
        except ImportError as e:
            logger.warning(f"API blueprint not found: {e}")
            
    except Exception as e:
        logger.error(f"Error registering blueprints: {e}")
        logger.error(traceback.format_exc())
    
    # Main route
    @app.route('/')
    def index():
        """Halaman utama - index"""
        try:
            logger.info("Accessing index page")
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Error loading index page: {e}")
            return f"Error loading index page: {str(e)}", 500
    
    # Kursi route
    @app.route('/kursi')
    def kursi():
        """Halaman kursi"""
        try:
            logger.info("Accessing kursi page")
            return render_template('produk.html')
        except Exception as e:
            logger.error(f"Error loading kursi page: {e}")
            return f"Error loading kursi page: {str(e)}", 500

    # Deskripsi
    @app.route('/deskripsi')
    def deskripsi():
        """Halaman deskripsi produk"""
        try:
            logger.info("Accessing deskripsi page")
            return render_template('deskripsi.html')
        except Exception as e:
            logger.error(f"Error loading deskripsi page: {e}")
            return f"Error loading deskripsi page: {str(e)}", 500
    
    # Deskripsi2
    @app.route('/deskripsi2')
    def deskripsi2():
        """Halaman deskripsi produk 2"""
        try:
            logger.info("Accessing deskripsi2 page")
            return render_template('deskripsi2.html')
        except Exception as e:
            logger.error(f"Error loading deskripsi2 page: {e}")
            return f"Error loading deskripsi2 page: {str(e)}", 500  
    
    # Health check route
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        try:
            # Test database connection
            from models.database_manager import DatabaseManager
            connection = DatabaseManager.get_connection()
            db_status = "OK" if connection else "FAILED"
            if connection:
                connection.close()
            
            return jsonify({
                'status': 'OK',
                'database': db_status,
                'python_version': sys.version,
                'flask_debug': app.debug
            })
        except Exception as e:
            return jsonify({
                'status': 'ERROR',
                'error': str(e)
            }), 500
    
    # Debug route untuk melihat semua routes
    @app.route('/debug/routes')
    def debug_routes():
        """Debug route untuk melihat semua registered routes"""
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                'rule': rule.rule
            })
        return jsonify({
            'total_routes': len(routes),
            'routes': routes
        })
    
    # Log routes setelah semua blueprint terdaftar
    def log_routes():
        logger.info("=== REGISTERED ROUTES ===")
        for rule in app.url_map.iter_rules():
            methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
            logger.info(f"{methods:8} {rule.rule:30} -> {rule.endpoint}")
        logger.info("=========================")
    
    # Call log_routes function setelah setup selesai
    with app.app_context():
        log_routes()
    
    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handler untuk 404 error"""
        logger.warning(f"404 error: {error}")
        return jsonify({
            'error': 'Page not found',
            'message': 'The requested page could not be found.',
            'available_routes': [rule.rule for rule in app.url_map.iter_rules()]
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handler untuk 500 error"""
        logger.error(f"500 error: {error}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An internal server error occurred.'
        }), 500
    
    return app

if __name__ == '__main__':
    try:
        app = create_app()
        logger.info("Starting Flask development server...")
        
        # Debug info sebelum start
        logger.info(f"Flask app name: {app.name}")
        logger.info(f"Flask debug mode: {app.debug}")
        logger.info(f"Flask secret key set: {'Yes' if app.secret_key else 'No'}")
        
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        logger.error(traceback.format_exc())