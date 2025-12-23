#!/usr/bin/env python3
"""
Vercel serverless function entry point
"""

import sys
import os

# Add the xhs-queue-server directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'xhs-queue-server'))

from server import app

# Vercel expects the app to be available at module level
handler = app