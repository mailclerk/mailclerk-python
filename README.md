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
- [Varying API Keys](#changing-api-keys)
- [Tests](#tests)
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

## Tests

Tests aren't currently implemented.

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
