import mailclerk

from unittest import TestCase

class TestInit(TestCase):
    def test_init(self):
        def should_raise():
            mailclerk.MailclerkAPIClient("", "")
            
        self.assertRaises(mailclerk.MailclerkError, should_raise)
        mailclerk.MailclerkAPIClient("mc_live_123", "https://api.mailclerk.app") # ok