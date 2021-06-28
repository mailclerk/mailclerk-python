import requests, base64, time
import uuid

from mailclerk import __version__, outbox
from .errors import MailclerkError, MailclerkAPIError, MailclerkUnknownAPIError

class MailclerkAPIClient():
    def __init__(self, api_key, api_url):
        self.api_url = api_url
        self.api_key = api_key
        
        if self.api_key == None or self.api_key == "":
            raise MailclerkError("No Mailclerk API Key provided. Set `mailclerk.api_key`")

        self.version_label = "Mailclerk Python %s" % __version__
        
    def deliver(self, template, recipient, data = {}, options = {}):            
        token = base64.b64encode(("%s:" % self.api_key).encode("utf-8")).decode('utf-8')
        
        options = dict(options)

        if "idempotency_key" not in options:
            options["idempotency_key"] = str(uuid.uuid4())

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

        
        def send_request():
            response = requests.post(
                "%s/deliver" % self.api_url,
                json={
                    "template": template,
                    "recipient": recipient,
                    "data": data,
                    "options": options
                },
                headers={
                    'X-Client-Version': self.version_label,
                    'Authorization': "Basic %s" % token
                }
            )
            
            if response.status_code >= 400:
                try:
                    description = "Mailclerk API Error: %s" % response.json()["message"]
                except Exception as e:
                    # No message or not JSON encodable
                    raise MailclerkUnknownAPIError(
                        "Mailclerk API Unknown Error. Status: %s" % response.status_code,
                        http_status=response.status_code,
                        http_response=response
                    )

                raise MailclerkAPIError(
                    description,
                    http_status=response.status_code,
                    http_response=response
                )
            else:
                return response
                    
        # Try to make the request up to three times
        RETRIES = 3
        for iter in range(RETRIES):
            try:
                response = send_request()
            except MailclerkUnknownAPIError as e:
                if iter < RETRIES - 1:
                    time.sleep(3) # Sleep three seconds, then try again
                    # Try again
                    continue
                else:
                    # Give up, raise the exception
                    raise e

            # Assuming no unknow error, break the loop
            break

        if outbox.enabled:
            outbox.add_send(params, response.json()["delivery"])
        
        return response