import unittest
import os
from unittest import IsolatedAsyncioTestCase
from tools.rs_staff import get_access_token, get_staff_info
from dotenv import load_dotenv

load_dotenv()

zgh = os.getenv("TEST_ZGH")
xm = os.getenv("TEST_XM")
sj = os.getenv("TEST_SJ")

class TestRsStaff(IsolatedAsyncioTestCase):
    async def test_get_access_token(self):
        """Test that access token is returned with expected structure"""
        token = await get_access_token()
        
        # Verify token structure
        self.assertIsInstance(token, dict)
        self.assertIn('access_token', token)
        self.assertIn('token_type', token)
        self.assertIn('refresh_token', token)
        self.assertIn('expires_in', token)
        self.assertIn('scope', token)
        self.assertIn('license', token)
        
        # Verify token values
        self.assertEqual(token['token_type'], 'bearer')
        self.assertEqual(token['license'], 'made by pangu')

    async def test_get_staff_info(self):
        """Test staff info retrieval with valid parameters"""
        staff_info = await get_staff_info(zgh=zgh)
        
        # Verify response structure
        self.assertIsInstance(staff_info, list)
        self.assertGreater(len(staff_info), 0)
        
        # Verify sample fields
        first_result = staff_info[0]
        self.assertIn('职工号', first_result)
        self.assertIn('姓名', first_result)
        self.assertEqual(first_result['职工号'], zgh)

    async def test_get_staff_info_with_multiple_params(self):
        """Test staff info retrieval with multiple parameters"""
        staff_info = await get_staff_info(
            zgh=zgh,
            xm=xm,
            sj=sj
        )
        
        self.assertIsInstance(staff_info, list)
        self.assertGreater(len(staff_info), 0)

    async def test_get_staff_info_empty_params(self):
        """Test staff info retrieval with empty parameters"""
        with self.assertRaises(Exception):
            await get_staff_info(zgh="")

if __name__ == '__main__':
    unittest.main()
