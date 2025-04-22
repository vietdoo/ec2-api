from enum import StrEnum
from typing import Literal, cast


class Platforms(StrEnum):
    github = "github"


class PaymentProcessor(StrEnum):
    stripe = "stripe"


class AccountType(StrEnum):
    stripe = "stripe"
    open_collective = "open_collective"

    def get_display_name(self) -> str:
        return {
            AccountType.stripe: "Stripe Connect Express",
            AccountType.open_collective: "Open Collective",
        }[self]


class SubscriptionRecurringInterval(StrEnum):
    month = "month"
    year = "year"

    def as_literal(self) -> Literal["month", "year"]:
        return cast(Literal["month", "year"], self.value)


class SubscriptionProrationBehavior(StrEnum):
    invoice = "invoice"
    prorate = "prorate"

    def to_stripe(self) -> Literal["always_invoice", "create_prorations"]:
        if self == SubscriptionProrationBehavior.invoice:
            return "always_invoice"
        if self == SubscriptionProrationBehavior.prorate:
            return "create_prorations"
        raise ValueError(f"Invalid proration behavior: {self}")


class TokenType(StrEnum):
    client_secret = "vec2_client_secret"
    client_registration_token = "vec2_client_registration_token"
    authorization_code = "vec2_authorization_code"
    access_token = "vec2_access_token"
    refresh_token = "vec2_refresh_token"
    personal_access_token = "vec2_personal_access_token"
    organization_access_token = "vec2_organization_access_token"
    customer_session_token = "vec2_customer_session_token"
    user_session_token = "vec2_user_session_token"
