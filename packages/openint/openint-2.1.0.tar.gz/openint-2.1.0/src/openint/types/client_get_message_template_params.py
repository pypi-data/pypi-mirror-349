# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientGetMessageTemplateParams"]


class ClientGetMessageTemplateParams(TypedDict, total=False):
    customer_id: Required[Annotated[str, PropertyInfo(alias="customerId")]]

    language: Literal["javascript"]

    use_environment_variables: Annotated[bool, PropertyInfo(alias="useEnvironmentVariables")]
