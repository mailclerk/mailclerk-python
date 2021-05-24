from dotenv import load_dotenv
load_dotenv()

import mailclerk
import os

mailclerk.api_key = os.environ.get("MAILCLERK_TEST_API_KEY")
mailclerk.api_url = os.environ.get("MAILCLERK_TEST_API_URL")
mailclerk.outbox.enable()

TEST_TEMPLATE = os.environ.get("TEST_TEMPLATE")

from unittest import TestCase

class TestOutbox(TestCase):        
    def setUp(self):
        mailclerk.outbox.reset()

    def test_send_works(self):
        mailclerk.deliver(
            TEST_TEMPLATE,
            "john@example.com"
        )
        self.assertEqual(len(mailclerk.outbox), 1)        
    
    def test_sends_slice(self):
        mailclerk.deliver(
            TEST_TEMPLATE,
            "john@example.com"
        )
        mailclerk.deliver(
            TEST_TEMPLATE,
            "mark@example.com"
        )
        mailclerk.deliver(
            TEST_TEMPLATE,
            "mary@example.com"
        )
        self.assertEqual(
            [x.recipient_email for x in mailclerk.outbox[0:2]],
            ["john@example.com", "mark@example.com"]
        )

    def test_send_values(self):
        mailclerk.deliver(
            TEST_TEMPLATE,
            "jane@example.com",
            { "flag": 10 },
            { "foo": "bar"  }
        )
        self.assertEqual(len(mailclerk.outbox), 1)
        email = mailclerk.outbox[0]
        
        # Originating locally
        self.assertEqual(email.template, TEST_TEMPLATE)
        self.assertEqual(email.recipient, "jane@example.com")
        self.assertEqual(email.recipient_email, "jane@example.com")
        self.assertIsNone(email.recipient_name)
        self.assertIsNotNone(email.data)
        self.assertEqual(email.data.flag, 10)
        self.assertEqual(email.data["flag"], 10)
        self.assertIsNotNone(email.options)
        self.assertEqual(email.options.foo, "bar")
        
        # Originating on the server
        self.assertIsNotNone(email.from_sender)
        self.assertIsNotNone(email.from_sender.address)
        self.assertIsNotNone(email.subject)
        self.assertIsNotNone(email.html)
        self.assertIn("<html", email.html)
        self.assertIsNotNone(email.text)
 
    def test_composite_email(self):
        mailclerk.deliver(
            TEST_TEMPLATE,
            "Alex Green <alex@example.com>"
        )
        email = mailclerk.outbox[0]
     
        self.assertEqual(email.recipient, "Alex Green <alex@example.com>")
        self.assertEqual(email.recipient_email, "alex@example.com")
        self.assertEqual(email.recipient_name, "Alex Green")

    def test_composite_email(self):
        mailclerk.deliver(
            TEST_TEMPLATE,
            { "name": "Alex Green", "address": "alex@example.com" }
        )
        email = mailclerk.outbox[0]

        self.assertEqual(email.recipient.name, "Alex Green")
        self.assertEqual(email.recipient_email, "alex@example.com")
        self.assertEqual(email.recipient_name, "Alex Green")

    def test_filter(self):

        mailclerk.deliver(
            TEST_TEMPLATE,
            "jane@example.com",
            { "flag": 10 },
            { "foo": "bar"  }
        )

        mailclerk.deliver(
            TEST_TEMPLATE,
            "faye@example.com",
            { "person": { "name": "Mugsby" } },
            { "foo": "bar"  }
        )

        # Fetching by name
        self.assertEqual(len(mailclerk.outbox.filter(
          template=TEST_TEMPLATE
        )), 2)

        self.assertEqual(len(mailclerk.outbox.filter(
          template="other-template"
        )), 0)

        # Fetching by recipient_email

        self.assertEqual(len(mailclerk.outbox.filter(
          recipient_email="jane@example.com"
        )), 1)

        self.assertEqual(mailclerk.outbox.filter(
          recipient_email="jane@example.com"
        )[0].data.flag, 10)

        # Multiple conditions

        self.assertEqual(len(mailclerk.outbox.filter(
          recipient_email="jane@example.com",
          template=TEST_TEMPLATE
        )), 1)