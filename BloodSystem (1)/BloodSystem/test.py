import unittest
from datetime import datetime, timedelta, date


def validate_blood_type(blood_type):
    """Validate if blood type is valid"""
    valid_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    if blood_type.upper() in valid_types:
        return True, blood_type.upper()
    return False, "Invalid blood type"


def check_donor_eligibility(eligibility_status):
    """Check if donor is eligible to donate"""
    if eligibility_status.lower() == 'eligible':
        return True, "Eligible to donate"
    return False, "Not eligible to donate"


def check_inventory_stock(quantity, min_stock_level):
    """Check if blood inventory stock is low"""
    if quantity <= min_stock_level:
        return "Low Stock"
    return "In Stock"


def calculate_donation_total(donations):
    """Calculate total quantity of donations"""
    total = 0
    for donation in donations:
        total += donation.get('quantity', 0)
    return total


def calculate_average_donations(total_donations, total_donors):
    """Calculate average donations per donor"""
    if total_donors == 0:
        return 0.0
    return round(total_donations / total_donors, 2)


def get_date_range(period):
    """Get date range based on period (today, week, month, all)"""
    today = datetime.now()
    if period == "today":
        from_date = today.strftime("%Y-%m-%d")
        to_date = today.strftime("%Y-%m-%d")
    elif period == "week":
        from_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        to_date = today.strftime("%Y-%m-%d")
    elif period == "month":
        from_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        to_date = today.strftime("%Y-%m-%d")
    elif period == "all":
        from_date = "2020-01-01"
        to_date = today.strftime("%Y-%m-%d")
    else:
        return None, None
    return from_date, to_date


def validate_age_for_donation(date_of_birth):
    """Validate if donor age is between 18 and 65"""
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    
    if age < 18:
        return False, "Donor must be at least 18 years old"
    elif age > 65:
        return False, "Donor must be 65 years old or younger"
    return True, age


def check_blood_compatibility(required_type, available_type):
    """Check if blood types are compatible for transfusion"""
    
    compatibility_map = {
        'A+': ['A+', 'A-', 'O+', 'O-'],
        'A-': ['A-', 'O-'],
        'B+': ['B+', 'B-', 'O+', 'O-'],
        'B-': ['B-', 'O-'],
        'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        'AB-': ['AB-', 'A-', 'B-', 'O-'],
        'O+': ['O+', 'O-'],
        'O-': ['O-']
    }
    
    required = required_type.upper()
    available = available_type.upper()
    
    if required in compatibility_map and available in compatibility_map[required]:
        return True, "Compatible"
    return False, "Not compatible"


def validate_required_fields(fields):
    """Validate that required fields are not empty"""
    for field_name, field_value in fields.items():
        if not field_value or not str(field_value).strip():
            return False, f"{field_name} is required"
    return True, "All fields valid"


def check_donation_interval(last_donation_date, days_required=56):
    """Check if enough days have passed since last donation"""
    if not last_donation_date:
        return True, "No previous donation"
    
    today = date.today()
    days_since = (today - last_donation_date).days
    
    if days_since >= days_required:
        return True, f"{days_since} days since last donation"
    return False, f"Must wait {days_required - days_since} more days"


def calculate_inventory_percentage(quantity, min_stock_level, max_capacity=100):
    """Calculate inventory percentage based on quantity and capacity"""
    if max_capacity == 0:
        return 0.0
    percentage = (quantity / max_capacity) * 100
    return round(percentage, 2)


class BloodSystemTests(unittest.TestCase):

    def test_validate_blood_type_valid(self):
        """valid blood type should return True and uppercase value"""
        is_valid, result = validate_blood_type("A+")
        self.assertTrue(is_valid)
        self.assertEqual(result, "A+")

    def test_validate_blood_type_invalid(self):
        """invalid blood type should return False with error message"""
        is_valid, result = validate_blood_type("X+")
        self.assertFalse(is_valid)
        self.assertEqual(result, "Invalid blood type")

    def test_validate_blood_type_lowercase(self):
        """lowercase blood type should be converted to uppercase"""
        is_valid, result = validate_blood_type("o-")
        self.assertTrue(is_valid)
        self.assertEqual(result, "O-")

    def test_check_donor_eligibility_eligible(self):
        """eligible status should return True"""
        is_eligible, message = check_donor_eligibility("Eligible")
        self.assertTrue(is_eligible)
        self.assertEqual(message, "Eligible to donate")

    def test_check_donor_eligibility_not_eligible(self):
        """not eligible status should return False"""
        is_eligible, message = check_donor_eligibility("Not Eligible")
        self.assertFalse(is_eligible)
        self.assertEqual(message, "Not eligible to donate")

    def test_check_inventory_stock_low(self):
        """stock below minimum should return Low Stock"""
        status = check_inventory_stock(5, 10)
        self.assertEqual(status, "Low Stock")

    def test_check_inventory_stock_in_stock(self):
        """stock above minimum should return In Stock"""
        status = check_inventory_stock(15, 10)
        self.assertEqual(status, "In Stock")

    def test_check_inventory_stock_equal(self):
        """stock equal to minimum should return Low Stock"""
        status = check_inventory_stock(10, 10)
        self.assertEqual(status, "Low Stock")

    def test_calculate_donation_total(self):
        """donation total should sum all donation quantities"""
        donations = [
            {'donation_id': 1, 'quantity': 1, 'blood_type': 'A+'},
            {'donation_id': 2, 'quantity': 1, 'blood_type': 'B+'},
            {'donation_id': 3, 'quantity': 1, 'blood_type': 'O+'}
        ]
        total = calculate_donation_total(donations)
        self.assertEqual(total, 3)

    def test_calculate_donation_total_empty(self):
        """empty donations list should return zero"""
        donations = []
        total = calculate_donation_total(donations)
        self.assertEqual(total, 0)

    def test_calculate_average_donations(self):
        """average donations should divide total by donors"""
        avg = calculate_average_donations(20, 5)
        self.assertEqual(avg, 4.0)

    def test_calculate_average_donations_zero_donors(self):
        """average donations with zero donors should return zero"""
        avg = calculate_average_donations(20, 0)
        self.assertEqual(avg, 0.0)

    def test_get_date_range_today(self):
        """today period should return today's date for both"""
        from_date, to_date = get_date_range("today")
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(from_date, today)
        self.assertEqual(to_date, today)

    def test_get_date_range_week(self):
        """week period should return 7 days ago to today"""
        from_date, to_date = get_date_range("week")
        today = datetime.now()
        expected_from = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        expected_to = today.strftime("%Y-%m-%d")
        self.assertEqual(from_date, expected_from)
        self.assertEqual(to_date, expected_to)

    def test_get_date_range_month(self):
        """month period should return 30 days ago to today"""
        from_date, to_date = get_date_range("month")
        today = datetime.now()
        expected_from = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        expected_to = today.strftime("%Y-%m-%d")
        self.assertEqual(from_date, expected_from)
        self.assertEqual(to_date, expected_to)

    def test_get_date_range_all(self):
        """all period should return 2020-01-01 to today"""
        from_date, to_date = get_date_range("all")
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(from_date, "2020-01-01")
        self.assertEqual(to_date, today)

    def test_validate_age_for_donation_valid(self):
        """age between 18 and 65 should be valid"""
        birth_date = date(1990, 5, 15)
        is_valid, result = validate_age_for_donation(birth_date)
        self.assertTrue(is_valid)
        self.assertIsInstance(result, int)

    def test_validate_age_for_donation_too_young(self):
        """age below 18 should be invalid"""
        birth_date = date(2010, 1, 1)
        is_valid, message = validate_age_for_donation(birth_date)
        self.assertFalse(is_valid)
        self.assertIn("18 years old", message)

    def test_validate_age_for_donation_too_old(self):
        """age above 65 should be invalid"""
        birth_date = date(1950, 1, 1)
        is_valid, message = validate_age_for_donation(birth_date)
        self.assertFalse(is_valid)
        self.assertIn("65 years old", message)

    def test_check_blood_compatibility_same_type(self):
        """same blood type should be compatible"""
        is_compatible, message = check_blood_compatibility("A+", "A+")
        self.assertTrue(is_compatible)
        self.assertEqual(message, "Compatible")

    def test_check_blood_compatibility_compatible(self):
        """compatible blood types should return True"""
        is_compatible, message = check_blood_compatibility("A+", "O-")
        self.assertTrue(is_compatible)
        self.assertEqual(message, "Compatible")

    def test_check_blood_compatibility_not_compatible(self):
        """incompatible blood types should return False"""
        is_compatible, message = check_blood_compatibility("A+", "B+")
        self.assertFalse(is_compatible)
        self.assertEqual(message, "Not compatible")

    def test_check_blood_compatibility_universal_recipient(self):
        """AB+ should accept all blood types"""
        is_compatible, message = check_blood_compatibility("AB+", "O-")
        self.assertTrue(is_compatible)
        self.assertEqual(message, "Compatible")

    def test_check_blood_compatibility_universal_donor(self):
        """O- should be compatible with all types"""
        is_compatible, message = check_blood_compatibility("A+", "O-")
        self.assertTrue(is_compatible)
        self.assertEqual(message, "Compatible")

    def test_validate_required_fields_valid(self):
        """all required fields filled should return True"""
        fields = {
            'full_name': 'John Doe',
            'blood_type': 'A+',
            'date_of_birth': '1990-01-01'
        }
        is_valid, message = validate_required_fields(fields)
        self.assertTrue(is_valid)
        self.assertEqual(message, "All fields valid")

    def test_validate_required_fields_empty(self):
        """empty required field should return False"""
        fields = {
            'full_name': '',
            'blood_type': 'A+',
            'date_of_birth': '1990-01-01'
        }
        is_valid, message = validate_required_fields(fields)
        self.assertFalse(is_valid)
        self.assertIn("is required", message)

    def test_validate_required_fields_whitespace(self):
        """whitespace only field should return False"""
        fields = {
            'full_name': '   ',
            'blood_type': 'A+',
            'date_of_birth': '1990-01-01'
        }
        is_valid, message = validate_required_fields(fields)
        self.assertFalse(is_valid)
        self.assertIn("is required", message)

    def test_check_donation_interval_no_previous(self):
        """no previous donation should allow donation"""
        is_allowed, message = check_donation_interval(None)
        self.assertTrue(is_allowed)
        self.assertEqual(message, "No previous donation")

    def test_check_donation_interval_sufficient_days(self):
        """sufficient days since last donation should allow donation"""
        last_donation = date.today() - timedelta(days=60)
        is_allowed, message = check_donation_interval(last_donation)
        self.assertTrue(is_allowed)
        self.assertIn("days since last donation", message)

    def test_check_donation_interval_insufficient_days(self):
        """insufficient days since last donation should not allow donation"""
        last_donation = date.today() - timedelta(days=30)
        is_allowed, message = check_donation_interval(last_donation)
        self.assertFalse(is_allowed)
        self.assertIn("more days", message)

    def test_calculate_inventory_percentage(self):
        """inventory percentage should calculate correctly"""
        percentage = calculate_inventory_percentage(50, 10, 100)
        self.assertEqual(percentage, 50.0)

    def test_calculate_inventory_percentage_zero_capacity(self):
        """zero capacity should return zero percentage"""
        percentage = calculate_inventory_percentage(50, 10, 0)
        self.assertEqual(percentage, 0.0)

    def test_calculate_inventory_percentage_full(self):
        """full inventory should return 100%"""
        percentage = calculate_inventory_percentage(100, 10, 100)
        self.assertEqual(percentage, 100.0)


if __name__ == "__main__":
    unittest.main()

