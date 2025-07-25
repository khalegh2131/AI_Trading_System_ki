# D:\AI\AI_Trading_System_ki\vpn\config.py

VPN_CONFIG = {
    'subscription_urls': [
        'https://raw.githubusercontent.com/freefq/free/master/v2',
        # می‌تونی لینک‌های دیگه رو اضافه کنی
    ],
    'test_endpoints': {
        'binance': 'https://api.binance.com/api/v3/ping',
        'coindesk': 'https://www.coindesk.com',
        'google': 'https://www.google.com'
    },
    'connection_timeout': 10,
    'test_timeout': 5,
    'max_servers_to_test': 10
}