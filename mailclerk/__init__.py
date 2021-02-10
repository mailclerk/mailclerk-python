import os

# Version of the Mailclerk python package
__version__ = "1.0.0"

api_key = os.environ.get("MAILCLERK_API_KEY")
api_url = os.environ.get("MAILCLERK_API_URL", "https://api.mailclerk.app")

from .api_client import MailclerkAPIClient, MailclerkError

def deliver(template_slug, recipient, data = {}, options = {}):
    client = MailclerkAPIClient(api_key, api_url)
    return client.deliver(template_slug, recipient, data, options)