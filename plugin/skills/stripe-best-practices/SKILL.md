---
name: stripe-best-practices
description: >-
  Stripe integration decisions: sandboxes, Checkout Sessions vs PaymentIntents,
  Connect (Accounts v2), billing and subscriptions, Stripe Tax, Treasury, API
  key and webhook security. Use when you plan, build, test, review, or migrate
  a Stripe integration.
---

Latest Stripe API version: **2026-09-30.endive**. Always use the latest API version and SDK, unless the user specifies a different version.

Default development and test environment:

- For new integration development, use separate [sandboxes](https://docs.stripe.com/sandboxes.md). Do not use the shared test mode sandbox of the account.
- Sandboxes isolate settings and test data from live mode.
- Use separate sandboxes for local development and for CI.
- For stronger isolation, give sandboxes to specific development teams or test scenarios.
- Use the shared test mode sandbox only in these conditions: an existing integration depends on it, or a necessary feature does not support general sandboxes.

Latest SDK versions:

| Language | Latest version |
| --- | --- |
| Ruby | 20.0.0 |
| Python | 16.0.0 |
| Node.js | 23.0.0 |
| PHP | 22.0.0 |
| Java | 34.0.0 |
| Go | 87.0.0 |
| .NET | 53.0.0 |

If you do not have a Stripe account, use the CLI to make a sandbox test account. No registration is necessary.

1. Install the Stripe CLI: `npm i -g @stripe/cli`.
2. Run `stripe sandbox create`. It makes test API keys for you.
3. Tell the user that [a sandbox is a Stripe test environment](https://docs.stripe.com/sandboxes.md).

If you use `stripe sandbox create`, do not use MCP. If you must use MCP after sandbox creation, first make sure that `stripe sandbox claim` ran.

For CLI auth checks, use `stripe whoami --format json`. Do not run `stripe config --list`.

Default API key: always recommend a [restricted API key (RAK)](https://docs.stripe.com/keys.md#manage-your-api-keys) (`rk_` prefix). Do not recommend a secret key (`sk_` prefix).

## Integration routing

| Building… | Recommended API | Details |
| --- | --- | --- |
| One-time payments | Checkout Sessions | <references/payments.md> |
| Custom payment form with embedded UI | Checkout Sessions + Payment Element | <references/payments.md> |
| Saving a payment method for later | Setup Intents | <references/payments.md> |
| Connect platform or marketplace | Accounts v2 (`/v2/core/accounts`) | <references/connect.md> |
| Usage-based billing (new integration) | Metronome | <references/billing.md> |
| Subscriptions or recurring billing | Billing APIs + Checkout Sessions | <references/billing.md> |
| Sales tax, VAT, or GST compliance | Stripe Tax + Registrations API | <references/tax.md> |
| Embedded financial accounts / banking | v2 Financial Accounts | <references/treasury.md> |
| Security (key management, RAKs, webhooks, OAuth, 2FA, Connect liability) | See security reference | <references/security.md> |

Before you answer an integration question or write code, read the applicable reference file.

## Critical rules

- *Before you enable `automatic_tax: { enabled: true }`* (or calculate tax for a custom PaymentIntent):
  1. Read the [tax reference](references/tax.md).
  2. Make sure that the user has an active registration.

  Without a registration, Stripe does not calculate or collect tax, but the user thinks that tax is on. This is the most common Stripe Tax mistake.

- *Do not include `payment_method_types` in a Stripe API call.* There is one exception: Terminal (in-person payments) integrations must pass `payment_method_types: ['card_present']` on the PaymentIntent.
  - For all other integrations, do not use this parameter. This enables dynamic payment methods. Then you configure payment method settings in the Dashboard, and Stripe shows each customer the most applicable eligible payment methods to increase conversion.
  - To select which payment methods you accept, use [payment_method_configurations](https://docs.stripe.com/payments/payment-method-configurations.md) or `excluded_payment_method_types`. Do not use `payment_method_types`.

- When a PaymentIntent or SetupIntent integration needs an explicit allowlist, use `allowed_payment_method_types`. Do not use `payment_method_types`.

- *Do not tell the user that webhooks are optional.*
  - Use webhooks for all payment integrations. They are necessary for subscriptions and asynchronous payment methods.
  - Do fulfillment in a handler for `checkout.session.completed` and `checkout.session.async_payment_succeeded` (gated on `payment_status`). Do not do fulfillment on the success page.
  - Refer to <references/payments.md>.

- On API version `2026-03-25.dahlia` or later, pass the parameter `integration_identifier` to `checkout.sessions.create`. It tags sessions with a custom label, so you can track and compare checkout flows in the Dashboard. The label must end with a suffix of 8 random letters.

- *Always make a `StripeClient` instance and call methods on that instance.* Do **not** use the deprecated global/module-level API key pattern (`stripe.api_key = …`, `Stripe.setApiKey`, `stripe.Key = …`, `StripeConfiguration.ApiKey = …`). All current SDKs deprecate the global pattern.

## Key documentation

When the request of the user does not fit one domain above, read:

- [Integration Options](https://docs.stripe.com/payments/payment-methods/integration-options.md) — Start here when you design an integration.
- [API Tour](https://docs.stripe.com/payments-api/tour.md) — Overview of the Stripe API.
- [Go Live Checklist](https://docs.stripe.com/get-started/checklist/go-live.md) — Review it before launch.
