
# CLIENT_ID = 'user name'
# CLIENT_SECRET = 'password'


import importlib.util
spec = importlib.util.spec_from_file_location("credentials", "c:/data-api-python_credentials.py")

if not spec:
    raise Exception('no spec : (')

module = importlib.util.module_from_spec(spec)

if not spec.loader:
    raise Exception('no spec.loader is None : (')

spec.loader.exec_module(module)

CLIENT_ID = module.CLIENT_ID
CLIENT_SECRET = module.CLIENT_SECRET

__all__ = ['CLIENT_ID', 'CLIENT_SECRET']
