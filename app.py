from flask import Flask, render_template, jsonify, session, redirect, url_for, request
from datetime import timedelta
from dotenv import load_dotenv
import os
import logging
import sys
import traceback
from functools import wraps

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

def login_required(f):
    """Decorator untuk memastikan user sudah login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Jika akses via AJAX/API, return JSON response
            if request.is_json or request.headers.get('Content-Type') == 'application/json':
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Silakan login untuk mengakses halaman ini',
                    'redirect': url_for('auth_bp.login')
                }), 401
            else:
                # Jika akses via browser, redirect ke halaman login
                return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def create_app():
    app = Flask(__name__)
    
    # Konfigurasi authentication
    app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')  # Ganti dengan secret key yang aman
    app.permanent_session_lifetime = timedelta(days=7)  # Session berlaku 7 hari
    
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
        
        # Register authentication blueprint
        try:
            from routes.auth_routes import auth_bp
            app.register_blueprint(auth_bp)
            logger.info("[OK] Auth blueprint registered")
        except ImportError as e:
            logger.error(f"Failed to import auth blueprint: {e}")
            logger.error("Expected file: routes/auth_routes.py")
        
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
    
    # Register context processor untuk template
    try:
        from middleware.auth_middleware import AuthContext
        app.context_processor(AuthContext.inject_auth_context)
        logger.info("[OK] Auth context processor registered")
    except ImportError as e:
        logger.error(f"Failed to import auth middleware: {e}")
    
    # Context processor untuk menambahkan informasi login ke template
    @app.context_processor
    def inject_user_info():
        """Inject user information ke semua template"""
        return {
            'is_logged_in': 'user_id' in session,
            'user_id': session.get('user_id'),
            'username': session.get('username', ''),
            'protected_routes': ['/material/add', '/katalog/add', '/katalog', '/materials']
        }
    
    # Main route - Updated with conditional access
    @app.route('/')
    def index():
        """Halaman utama - index yang bisa diakses tanpa login"""
        try:
            logger.info("Accessing index page")
            # Tampilkan halaman index untuk semua user (login/tidak login)
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Error loading index page: {e}")
            return f"Error loading index page: {str(e)}", 500
    
    # ============= PROTECTED ROUTES UNTUK MATERIAL =============
    @app.route('/materials')
    @login_required
    def materials():
        """Halaman tabel data material - hanya untuk user yang login"""
        try:
            logger.info(f"User {session.get('username')} accessing materials page")
            return render_template('materials.html')
        except Exception as e:
            logger.error(f"Error loading materials page: {e}")
            return f"Error loading materials page: {str(e)}", 500
    
    @app.route('/material/add')
    @login_required
    def add_material():
        """Halaman tambah data material - hanya untuk user yang login"""
        try:
            logger.info(f"User {session.get('username')} accessing add material page")
            return render_template('add_material.html')
        except Exception as e:
            logger.error(f"Error loading add material page: {e}")
            return f"Error loading add material page: {str(e)}", 500
    
    # ============= PROTECTED ROUTES UNTUK KATALOG =============
    @app.route('/katalog')
    @login_required
    def katalog():
        """Halaman katalog - hanya untuk user yang login"""
        try:
            logger.info(f"User {session.get('username')} accessing katalog page")
            return render_template('katalog.html')
        except Exception as e:
            logger.error(f"Error loading katalog page: {e}")
            return f"Error loading katalog page: {str(e)}", 500
    
    @app.route('/katalog/add')
    @login_required
    def add_katalog():
        """Halaman tambah katalog - hanya untuk user yang login"""
        try:
            logger.info(f"User {session.get('username')} accessing add katalog page")
            return render_template('add_katalog.html')
        except Exception as e:
            logger.error(f"Error loading add katalog page: {e}")
            return f"Error loading add katalog page: {str(e)}", 500
    
    # ============= PUBLIC ROUTES =============
    # Kursi route (public)
    @app.route('/kursi')
    def kursi():
        """Halaman kursi - public access"""
        try:
            logger.info("Accessing kursi page")
            return render_template('produk.html')
        except Exception as e:
            logger.error(f"Error loading kursi page: {e}")
            return f"Error loading kursi page: {str(e)}", 500

    # Deskripsi (public)
    @app.route('/deskripsi')
    def deskripsi():
        """Halaman deskripsi produk - public access"""
        try:
            logger.info("Accessing deskripsi page")
            return render_template('deskripsi.html')
        except Exception as e:
            logger.error(f"Error loading deskripsi page: {e}")
            return f"Error loading deskripsi page: {str(e)}", 500
    
    # Deskripsi2 (public)
    @app.route('/deskripsi2')
    def deskripsi2():
        """Halaman deskripsi produk 2 - public access"""
        try:
            logger.info("Accessing deskripsi2 page")
            return render_template('deskripsi2.html')
        except Exception as e:
            logger.error(f"Error loading deskripsi2 page: {e}")
            return f"Error loading deskripsi2 page: {str(e)}", 500  
    
    # ============= UTILITY ROUTES =============
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
                'flask_debug': app.debug,
                'session_active': 'user_id' in session,
                'user_id': session.get('user_id', 'Not logged in')
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
        protected_routes = []
        public_routes = []
        
        for rule in app.url_map.iter_rules():
            route_info = {
                'endpoint': rule.endpoint,
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                'rule': rule.rule
            }
            routes.append(route_info)
            
            # Categorize routes
            if rule.rule in ['/katalog/add', '/material/add', '/katalog', '/materials']:
                protected_routes.append(route_info)
            else:
                public_routes.append(route_info)
        
        return jsonify({
            'total_routes': len(routes),
            'protected_routes': protected_routes,
            'public_routes': public_routes,
            'current_user': session.get('user_id', 'Not logged in'),
            'session_active': 'user_id' in session
        })
    
    # Route untuk cek status login
    @app.route('/api/auth/status')
    def auth_status():
        """API endpoint untuk cek status login"""
        return jsonify({
            'is_logged_in': 'user_id' in session,
            'user_id': session.get('user_id'),
            'username': session.get('username', ''),
            'session_expires': session.permanent
        })
    
    # Log routes setelah semua blueprint terdaftar
    def log_routes():
        logger.info("=== REGISTERED ROUTES ===")
        logger.info("PROTECTED ROUTES (Login Required):")
        protected = ['/katalog/add', '/material/add', '/katalog', '/materials']
        
        for rule in app.url_map.iter_rules():
            methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
            status = "[PROTECTED]" if rule.rule in protected else "[PUBLIC]   "
            logger.info(f"{status} {methods:8} {rule.rule:30} -> {rule.endpoint}")
        logger.info("=========================")
    
    # Call log_routes function setelah setup selesai
    with app.app_context():
        log_routes()
    
    # ============= ERROR HANDLERS =============
    @app.errorhandler(404)
    def not_found(error):
        """Handler untuk 404 error"""
        logger.warning(f"404 error: {error}")
        return jsonify({
            'error': 'Page not found',
            'message': 'The requested page could not be found.',
            'available_routes': [rule.rule for rule in app.url_map.iter_rules()],
            'is_logged_in': 'user_id' in session
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handler untuk 500 error"""
        logger.error(f"500 error: {error}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An internal server error occurred.'
        }), 500
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handler untuk 401 error (Unauthorized)"""
        logger.warning(f"401 error: {error}")
        return jsonify({
            'error': 'Authentication required',
            'message': 'Silakan login untuk mengakses halaman ini',
            'login_url': url_for('auth_bp.login')
        }), 401
    
    return app

if __name__ == '__main__':
    try:
        app = create_app()
        logger.info("Starting Flask development server...")
        
        # Debug info sebelum start
        logger.info(f"Flask app name: {app.name}")
        logger.info(f"Flask debug mode: {app.debug}")
        logger.info(f"Flask secret key set: {'Yes' if app.secret_key else 'No'}")
        
        # Info mengenai protected routes
        logger.info("=== PROTECTED ROUTES INFO ===")
        logger.info("Routes yang memerlukan login:")
        logger.info("- /katalog/add")
        logger.info("- /material/add") 
        logger.info("- /katalog")
        logger.info("- /materials")
        logger.info("=============================")
        
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        logger.error(traceback.format_exc())