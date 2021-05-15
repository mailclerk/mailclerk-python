import re

class MailclerkOutbox:
    def __init__(self):
        self.enabled = False
        self._sends = []
        
    def __len__(self):
        return len(self._sends)
    
    def reset(self):
        self._sends = []

    def enable(self):
        self.enabled = True
        
    def add_send(self, request, response):
        data = dict()
        data.update(request)
        data.update(response)
        
        email = OutboxEmail(
            OutboxStruct.recursive_init(data)
        )

        self._sends.append(email)
    
    def __getitem__(self, index):
        return self._sends[index]
        
    # Not just an alias for 'select'
    def filter(self, *args, **kwargs):
        def filter_by(email):
            for key, val in kwargs.items():
                if getattr(email, key) != val:
                    return False
            return True
            
        return list(filter(filter_by, self._sends))

class OutboxStruct(dict):
    @classmethod
    def recursive_init(cls, data):
        for key, value in data.items():
            if isinstance(data[key], dict):
                data[key] = cls.recursive_init(data[key])

        return cls(data)

    def __getattr__(self, key):
        return self.get(key)

class OutboxEmail(dict):
    def __init__(self, data):
        self._data = data
                
    def __getattr__(self, key):
        return self._data.get(key)

    @property
    def recipient_email(self):
        return self.parse_recipient()["address"]

    @property
    def recipient_name(self):
        return self.parse_recipient()["name"]
        
    @property
    def from_sender(self):
        # "from" is a reserved keyword
        return self._data["from"]

    def parse_recipient(self):
        if not self.recipient:
            return {}

        if isinstance(self.recipient, OutboxStruct):
            return self.recipient

        text = self.recipient.strip()

        if re.match("^[^<]+<[^<]+>$", text):
            parts = text.split("<", 2)

            name = parts[0].strip().replace('"', "")
            address = parts[1].strip().replace(">", "")

            return {
                "name": name,
                "address": address
            }
        else:
            return {
                "name": None,
                "address": text
            }
        

#   class OutboxEmail < OpenStruct
# 
#     def self.recursive_init(data)
# 
#       data.each do |key, val|
#         if val.is_a?(Hash)
#           data[key] = self.recursive_init(val)
#         else
#           data[key] = val
#         end
#       end
# 
#       return OpenStruct.new(data)
#     end
# 
#     # Custom getters
# 
# 
#     private
# 
#   end
# end