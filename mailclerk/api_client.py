import requests, base64

from mailclerk import __version__, outbox
from .errors import MailclerkError, MailclerkAPIError

class MailclerkAPIClient():
    def __init__(self, api_key, api_url):
        self.api_url = api_url
        self.api_key = api_key
        
        if self.api_key == None or self.api_key == "":
            raise MailclerkError("No Mailclerk API Key provided. Set `mailclerk.api_key`")

        self.version_label = "Mailclerk Python %s" % __version__
        
    def deliver(self, template, recipient, data = {}, options = {}):            
        token = base64.b64encode(("%s:" % self.api_key).encode("utf-8")).decode('utf-8')
        
        if outbox.enabled:
            options = dict(options)
            options["local_outbox"] = True
        
        params = {
            "template": template,
            "recipient": recipient,
            "data": data,
            "options": options
        }

        response = requests.post(
            "%s/deliver" % self.api_url,
            json=params,
            headers={
                'X-Client-Version': self.version_label,
                'Authorization': "Basic %s" % token
            }
        )
        
        if response.status_code >= 400:
            try:
                description = "Mailclerk API Error: %s" % response.json()["message"]
            except:
                description = "Mailclerk API Unknown Error"
                
            raise MailclerkAPIError(
                description,
                http_status=response.status_code,
                http_response=response
            )
            
        if outbox.enabled:
            outbox.add_send(params, response.json()["delivery"])
        
        return response