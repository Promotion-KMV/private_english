command = '/home/vlad/english/myenv/bin/gunicorn'
pythonpath = '/home/vlad/english/private_english'
bind = '0.0.0.0:8001'
#bind = '178.154.244.182:8001'
workers = 5
user = 'vlad'
limit_request_fields = 32000
limit_request_field_size = 0
timeout=240
raw_env = 'DJANGO_SETTINGS_MODULE=english.settings'
