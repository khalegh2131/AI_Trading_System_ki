# D:\AI\AI_Trading_System_ki\security\config.py

SECURITY_CONFIG = {
    'encryption': {
        'algorithm': 'AES',
        'key_length': 256,
        'salt': 'secure_trading_system_salt_16bytes'
    },
    'authentication': {
        'session_timeout': 3600,  # 1 hour
        'max_login_attempts': 5,
        'lockout_duration': 300   # 5 minutes
    },
    'logging': {
        'audit_log_file': 'logs/audit.log',
        'security_log_level': 'INFO'
    },
    'api_protection': {
        'rate_limit': 100,        # requests per minute
        'ip_blacklist': [],
        'require_https': True
    }
}