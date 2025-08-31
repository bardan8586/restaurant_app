#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os
from app import create_app

# Create the Flask application
app = create_app('production')

if __name__ == "__main__":
    # This is for development only
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
