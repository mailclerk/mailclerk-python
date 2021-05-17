<p align="center">
  <img src="https://github.com/mailclerk/mailclerk-ruby/blob/main/mailclerk.png?raw=true" alt="Mailclerk Logo"/>
</p>

# Mailclerk Python

Mailclerk helps anyone on your team design great emails, improve their performance, and free up developer time. [Learn more](https://mailclerk.app/)

<!-- Tocer[start]: Auto-generated, don't remove. -->

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [API Key & URL](#api-key--url)
- [Usage](#usage)
- [Testing](#testing)
- [Varying API Keys](#changing-api-keys)
- [Package Tests](#package-tests)
- [Versioning](#versioning)
- [Code of Conduct](#code-of-conduct)
- [Contributions](#contributions)
- [License](#license)
- [History](#history)

<!-- Tocer[finish]: Auto-generated, don't remove. -->

## Requirements

1. Python 2.7+ or Python 3.4+

## Setup

To install, run:

```
pip install mailclerk
```

## API Key & URL

To set the Mailclerk API Key (begins with `mc_`), you can provide it as an
environmental variable: `MAILCLERK_API_KEY`. Alternatively, you can
set it directly on the Mailclerk module:

```
import mailclerk
mailclerk.api_key = "mc_yourprivatekey"
```

_If you are using version control like git, we strongly recommend storing your
production API keys in environmental variables_.

The default API endpoint is `https://api.mailclerk.app`. To change this, you
can provide a `MAILCLERK_API_URL` ENV variable or set `mailclerk.mailclerk_url`.

## Usage

You'll need an active account and at least one template (in the example `welcome-email`).

To send an email to "alice@example.com":

```
mailclerk.deliver("welcome-email", "alice@example.com")
```

If the template has any dynamic data, you can include it in the third parameter
as a hash:

```
mailclerk.deliver("welcome-email", "alice@example.com", { name: "Alice" })
```

See [Mailclerk documentation](https://dashboard.mailclerk.app/docs) for more details.

## Testing

Your Mailclerk environment has two API keys: a production key (beginning with `mc_live`)
and a test key (beginning with `mc_test`). If you use the test key, emails will
not be delivered, but will show up in the logs on your Mailclerk account and can be
previewed there. This replaces tools like [naomi](https://github.com/edwinlunando/django-naomi) for previewing emails in development.

To avoid cluttering up your Mailclerk test logs with sends triggered by your
automated test suite, call `mailclerk.outbox.enable()` in the file that
configures your tests. For example, in Django, add it to the test environment-specific
section of your `settings.py` file.

This will also enable utility methods which you can use to write tests that check
emails are sent with the correct data:

```python
# Number of emails "sent"
len(mailclerk.outbox)

# Returns all emails of matching a template or email recipient. See method
mailclerk.outbox.filter(template="welcome-email")
mailclerk.outbox.filter(recipient_email="gilles@example.com")

# Returns the most recent email:
email = mailclerk.outbox[-1]
email.template        # "welcome-email"
email.recipient_email # "gilles@example.com"
email.subject         # "Welcome to Acme, Gilles"
email.html            # "<html><body>..."
```

In between test cases (for example, the `setUp()` method of a unittest case), you should clear the stored emails by calling `mailclerk.outbox.reset()`.

The emails have the following attributes:

| Attribute         | Description                                                                |
| ----------------- | -------------------------------------------------------------------------- |
| `template`        | Slug of the template sent (1st argument to `mailclerk.deliver`)            |
| `recipient`       | Hash representing the send recipient (2nd argument to `mailclerk.deliver`) |
| `recipient_email` | Email of the send recipient                                                |
| `recipient_name`  | Name of the send recipient (nil if not specified)                          |
| `data`            | Dynamic data for the send (3rd argument to `mailclerk.deliver`)            |
| `options`         | Options specified for the send (4th argument to `mailclerk.deliver`)       |
| `from`            | From Mailclerk: Hash with `name` and `address` of the sender               |
| `subject`         | From Mailclerk: Text of the send's subject line                            |
| `preheader`       | From Mailclerk: Text of the send's preheader                               |
| `html`            | From Mailclerk: Rendered body HTML for the send                            |
| `text`            | From Mailclerk: Rendered plaintext version of the send                     |
| `headers`         | From Mailclerk: Extra email headers (e.g. `reply-to`)                      |

See the [Mailclerk testing documentation](https://dashboard.mailclerk.app/docs#testing)
for more details.

## Varying API Keys

If you need to use multiple API keys, you can also initialize `mailclerk.MailclerkAPIClient`
instances with different keys. This:

```
mc_client = mailclerk.MailclerkAPIClient("mc_yourprivatekey")
mc_client.deliver("welcome-email", "bob@example.com")
```

Is equivalent to this:

```
mailclerk.api_key = "mc_yourprivatekey"
mailclerk.deliver("welcome-email", "bob@example.com")
```

## Package Tests

Install test dependencies:

```
pip install .[test]
```

Run with:

```
python -m unittest discover
```

## Versioning

Read [Semantic Versioning](https://semver.org) for details. Briefly, it means:

- Major (X.y.z) - Incremented for any backwards incompatible public API changes.
- Minor (x.Y.z) - Incremented for new, backwards compatible, public API enhancements/fixes.
- Patch (x.y.Z) - Incremented for small, backwards compatible, bug fixes.

## Code of Conduct

Please note that this project is released with a [CODE OF CONDUCT](CODE_OF_CONDUCT.md). By
participating in this project you agree to abide by its terms.

## Contributions

Read [CONTRIBUTING](CONTRIBUTING.md) for details.

## License

Copyright 2021 [Mailclerk](https://mailclerk.app/).
Read [LICENSE](LICENSE.md) for details.

## History

Read [CHANGES](CHANGES.md) for details.
Built with [Gemsmith](https://github.com/bkuhlmann/gemsmith).
