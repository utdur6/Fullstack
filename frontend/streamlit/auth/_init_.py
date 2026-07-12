# auth/__init__.py
from .state import *

__all__ = ['is_authenticated', 'require_login', 'save_auth', 'clear_auth', 'current_profile', 'is_admin']