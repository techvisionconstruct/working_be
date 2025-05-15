import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the installed packages to the path
vercel_python_path = Path(__file__).parent.parent / ".vercel" / "python"
sys.path.insert(0, str(vercel_python_path))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../.vercel/python')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# Vercel requires this handler function
def handler(request, response):
    return application(request, response)

app = application