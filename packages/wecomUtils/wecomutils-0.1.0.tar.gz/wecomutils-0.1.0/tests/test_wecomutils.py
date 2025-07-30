#!/usr/bin/env python3
"""
Simple test script for wecomUtils package.
"""

import sys
import os

# Add project root to path if running directly
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import wecomUtils
    from wecomUtils.db_manager import DBManager
    
    # Print package information
    print(f"Successfully imported wecomUtils from: {wecomUtils.__file__}")
    
    # Test database functionality
    try:
        # Replace with actual test parameters appropriate for your setup
        result = DBManager.execute_query("SELECT 1")
        print(f"Database query test result: {result}")
    except Exception as e:
        print(f"Database test error: {str(e)}")
    
    # Test other components - uncomment and modify as needed based on your actual package
    # from wecomUtils.storage import StorageService
    # storage = StorageService()
    # print(f"Storage service initialized: {storage}")
    
    print("All imports successful!")

except ImportError as e:
    print(f"Import error: {str(e)}")
    print("Make sure the package is installed or in your PYTHONPATH")
    sys.exit(1)

if __name__ == "__main__":
    print("Test completed!") 