import unittest
from pyticoop.dolibarr.exceptions import DolibarrRequestError

class TestDolibarrRequestError(unittest.TestCase):
    def test_init_with_message(self):
        error_message = "An error occurred"
        error = DolibarrRequestError(error_message)
        self.assertEqual(error.message, error_message)
        self.assertIsNone(error.status_code)

    def test_init_with_message_and_status_code(self):
        error_message = "Resource not found"
        status_code = 404
        error = DolibarrRequestError(error_message, status_code)
        self.assertEqual(error.message, error_message)
        self.assertEqual(error.status_code, status_code)

    def test_raise_exception(self):
        error_message = "Unauthorized access"
        status_code = 401
        with self.assertRaises(DolibarrRequestError) as context:
            raise DolibarrRequestError(error_message, status_code)
        self.assertEqual(str(context.exception), error_message)
        self.assertEqual(context.exception.status_code, status_code)

if __name__ == '__main__':
    unittest.main()