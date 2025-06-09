import re

class AuthValidator:
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email:
            return False, "Email is required"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        if len(email) > 100:
            return False, "Email is too long (max 100 characters)"
        
        return True, "Valid email"
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if not password:
            return False, "Password is required"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if len(password) > 255:
            return False, "Password is too long (max 255 characters)"
        
        # Optional: Add more password strength requirements
        # has_upper = any(c.isupper() for c in password)
        # has_lower = any(c.islower() for c in password)
        # has_digit = any(c.isdigit() for c in password)
        # has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        # if not (has_upper and has_lower and has_digit):
        #     return False, "Password must contain uppercase, lowercase, and digit"
        
        return True, "Valid password"
    
    @staticmethod
    def validate_name(name):
        """Validate name"""
        if not name:
            return False, "Name is required"
        
        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters long"
        
        if len(name) > 100:
            return False, "Name is too long (max 100 characters)"
        
        # Check if name contains only letters, spaces, and common name characters
        name_pattern = r'^[a-zA-Z\s\'-\.]+$'
        if not re.match(name_pattern, name.strip()):
            return False, "Name contains invalid characters"
        
        return True, "Valid name"
    
    @staticmethod
    def validate_login(email, password):
        """Validate login form data"""
        # Validate email
        email_valid, email_message = AuthValidator.validate_email(email)
        if not email_valid:
            return {
                'valid': False,
                'message': email_message,
                'field': 'email'
            }
        
        # Validate password
        password_valid, password_message = AuthValidator.validate_password(password)
        if not password_valid:
            return {
                'valid': False,
                'message': password_message,
                'field': 'password'
            }
        
        return {
            'valid': True,
            'message': 'Valid login data'
        }
    
    @staticmethod
    def validate_register(name, email, password):
        """Validate registration form data"""
        # Validate name
        name_valid, name_message = AuthValidator.validate_name(name)
        if not name_valid:
            return {
                'valid': False,
                'message': name_message,
                'field': 'name'
            }
        
        # Validate email
        email_valid, email_message = AuthValidator.validate_email(email)
        if not email_valid:
            return {
                'valid': False,
                'message': email_message,
                'field': 'email'
            }
        
        # Validate password
        password_valid, password_message = AuthValidator.validate_password(password)
        if not password_valid:
            return {
                'valid': False,
                'message': password_message,
                'field': 'password'
            }
        
        return {
            'valid': True,
            'message': 'Valid registration data'
        }