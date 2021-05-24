import os

# Version of the Mailclerk python package
__version__ = "1.1.0"

api_key = os.environ.get("MAILCLERK_API_KEY")
api_url = os.environ.get("MAILCLERK_API_URL", "https://api.mailclerk.app")

from .errors import MailclerkError
from .outbox import MailclerkOutbox

outbox = MailclerkOutbox()

from .api_client import MailclerkAPIClient

def deliver(template_slug, recipient, data = {}, options = {}):
    client = MailclerkAPIClient(api_key, api_url)
    return client.deliver(template_slug, recipient, data, options)