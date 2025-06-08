import re

class MaterialValidator:
    @staticmethod
    def validate_level(level):
        """Validasi level (0-4)"""
        try:
            level = int(level)
            if 0 <= level <= 4:
                return True, level
            else:
                return False, "Level harus antara 0-4"
        except (ValueError, TypeError):
            return False, "Level harus berupa angka"
    
    @staticmethod
    def validate_part_code(part_code):
        """Validasi part code (huruf kapital dan angka, maks 20 karakter)"""
        if not part_code or len(part_code.strip()) == 0:
            return False, "Part code tidak boleh kosong"
        
        part_code = part_code.strip().upper()
        if len(part_code) > 20:
            return False, "Part code maksimal 20 karakter"
        
        if not re.match(r'^[A-Z0-9]+$', part_code):
            return False, "Part code hanya boleh huruf kapital dan angka"
        
        return True, part_code

    @staticmethod
    def validate_description(description):
        """Validasi deskripsi (tidak kosong, maks 200 karakter)"""
        if not description or len(description.strip()) == 0:
            return False, "Deskripsi tidak boleh kosong"
        
        description = description.strip()
        if len(description) > 200:
            return False, "Deskripsi maksimal 200 karakter"
        
        return True, description
    
    @staticmethod
    def validate_lot_size(lot_size):
        """Validasi lot size (angka positif)"""
        try:
            lot_size = int(lot_size)
            if lot_size <= 0:
                return False, "Lot size harus lebih dari 0"
            if lot_size > 9999:
                return False, "Lot size maksimal 9999"
            return True, lot_size
        except (ValueError, TypeError):
            return False, "Lot size harus berupa angka"
    
    @staticmethod
    def validate_uom(uom):
        """Validasi UOM"""
        valid_uoms = ['Pcs', 'Log', 'Kg', 'Ltr', 'M', 'M2', 'M3', 'Set', 'Box', 'Roll']
        if uom not in valid_uoms:
            return False, f"UOM harus salah satu dari: {', '.join(valid_uoms)}"
        return True, uom
    
    @staticmethod
    def validate_status(status):
        """Validasi status"""
        valid_statuses = ['Buy', 'Make', 'Transfer', 'Phantom']
        if status not in valid_statuses:
            return False, f"Status harus salah satu dari: {', '.join(valid_statuses)}"
        return True, status