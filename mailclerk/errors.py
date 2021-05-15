class MailclerkError(Exception):
    pass
    
class MailclerkAPIError(MailclerkError):
    def __init__(self, description, http_status=None, http_response=None):
        super(MailclerkError, self).__init__(description)
        
        self.http_status = http_status
        self.http_response = http_response
