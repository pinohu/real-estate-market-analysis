"""
OAuth and 2FA authentication module.
"""

import os
import pyotp
import qrcode
from io import BytesIO
import base64
from typing import Optional, Dict, Any
from flask import current_app, session, url_for, redirect, request
from flask_login import current_user, login_user, logout_user
from authlib.integrations.flask_client import OAuth
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class OAuthManager:
    """Manages OAuth authentication"""
    
    def __init__(self, app):
        self.oauth = OAuth(app)
        self._setup_providers()
    
    def _setup_providers(self):
        """Set up OAuth providers"""
        # Google OAuth
        self.oauth.register(
            name='google',
            client_id=current_app.config['GOOGLE_CLIENT_ID'],
            client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'}
        )
        
        # GitHub OAuth
        self.oauth.register(
            name='github',
            client_id=current_app.config['GITHUB_CLIENT_ID'],
            client_secret=current_app.config['GITHUB_CLIENT_SECRET'],
            access_token_url='https://github.com/login/oauth/access_token',
            access_token_params=None,
            authorize_url='https://github.com/login/oauth/authorize',
            authorize_params=None,
            api_base_url='https://api.github.com/',
            client_kwargs={'scope': 'user:email'}
        )
    
    def login(self, provider: str) -> str:
        """Initiate OAuth login"""
        redirect_uri = url_for('auth.oauth_callback', provider=provider, _external=True)
        return self.oauth.providers[provider].authorize_redirect(redirect_uri)
    
    def callback(self, provider: str) -> Optional[Dict[str, Any]]:
        """Handle OAuth callback"""
        try:
            token = self.oauth.providers[provider].authorize_access_token()
            user_info = self._get_user_info(provider, token)
            return user_info
        except Exception as e:
            logger.error(f"OAuth callback failed: {str(e)}")
            return None
    
    def _get_user_info(self, provider: str, token: Dict[str, Any]) -> Dict[str, Any]:
        """Get user information from OAuth provider"""
        if provider == 'google':
            resp = self.oauth.google.get('userinfo')
            user_info = resp.json()
            return {
                'email': user_info['email'],
                'name': user_info.get('name'),
                'picture': user_info.get('picture'),
                'provider': 'google'
            }
        elif provider == 'github':
            resp = self.oauth.github.get('user')
            user_info = resp.json()
            return {
                'email': user_info['email'],
                'name': user_info.get('name'),
                'picture': user_info.get('avatar_url'),
                'provider': 'github'
            }
        return {}

class TwoFactorAuth:
    """Manages two-factor authentication"""
    
    def __init__(self, user):
        self.user = user
        self.secret = None
        self.totp = None
    
    def generate_secret(self) -> str:
        """Generate a new 2FA secret"""
        self.secret = pyotp.random_base32()
        self.totp = pyotp.TOTP(self.secret)
        return self.secret
    
    def generate_qr_code(self) -> str:
        """Generate QR code for 2FA setup"""
        if not self.secret:
            self.generate_secret()
        
        # Create provisioning URI
        provisioning_uri = self.totp.provisioning_uri(
            self.user.email,
            issuer_name="Real Estate Strategist"
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        # Convert to base64
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def verify_code(self, code: str) -> bool:
        """Verify 2FA code"""
        if not self.totp:
            self.totp = pyotp.TOTP(self.secret)
        return self.totp.verify(code)
    
    def is_enabled(self) -> bool:
        """Check if 2FA is enabled for user"""
        return bool(self.user.two_factor_secret)
    
    def enable(self) -> bool:
        """Enable 2FA for user"""
        if not self.secret:
            return False
        
        self.user.two_factor_secret = self.secret
        self.user.two_factor_enabled = True
        return True
    
    def disable(self) -> bool:
        """Disable 2FA for user"""
        self.user.two_factor_secret = None
        self.user.two_factor_enabled = False
        return True

class SessionManager:
    """Manages user sessions and security"""
    
    @staticmethod
    def create_session(user_id: str, remember: bool = False) -> Dict[str, Any]:
        """Create a new user session"""
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat(),
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string
        }
        
        if remember:
            session_data['expires_at'] = (datetime.utcnow() + timedelta(days=30)).isoformat()
        else:
            session_data['expires_at'] = (datetime.utcnow() + timedelta(hours=12)).isoformat()
        
        return session_data
    
    @staticmethod
    def update_session(session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update session with new activity"""
        session_data['last_activity'] = datetime.utcnow().isoformat()
        return session_data
    
    @staticmethod
    def is_session_valid(session_data: Dict[str, Any]) -> bool:
        """Check if session is valid"""
        if not session_data:
            return False
        
        expires_at = datetime.fromisoformat(session_data['expires_at'])
        return datetime.utcnow() < expires_at
    
    @staticmethod
    def invalidate_session(session_id: str):
        """Invalidate a session"""
        session.pop(session_id, None)
    
    @staticmethod
    def get_active_sessions(user_id: str) -> list:
        """Get all active sessions for a user"""
        return [
            session_data for session_id, session_data in session.items()
            if session_data.get('user_id') == user_id and SessionManager.is_session_valid(session_data)
        ] 