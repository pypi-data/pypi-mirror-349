from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_findings_by_project_source import GetFindingsByProjectSource
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    suppressed: Union[Unset, bool] = UNSET,
    source: Union[Unset, GetFindingsByProjectSource] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: dict[str, Any] = {}

    params["suppressed"] = suppressed

    json_source: Union[Unset, str] = UNSET
    if not isinstance(source, Unset):
        json_source = source.value

    params["source"] = json_source

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/finding/project/{uuid}".format(
            uuid=uuid,
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Any]:
    if response.status_code == 401:
        return None
    if response.status_code == 403:
        return None
    if response.status_code == 404:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    suppressed: Union[Unset, bool] = UNSET,
    source: Union[Unset, GetFindingsByProjectSource] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Returns a list of all findings for a specific project or generates SARIF file if Accept:
    application/sarif+json header is provided

     <p>Requires permission <strong>VIEW_VULNERABILITY</strong></p>

    Args:
        uuid (UUID):
        suppressed (Union[Unset, bool]):
        source (Union[Unset, GetFindingsByProjectSource]):
        accept (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        suppressed=suppressed,
        source=source,
        accept=accept,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    suppressed: Union[Unset, bool] = UNSET,
    source: Union[Unset, GetFindingsByProjectSource] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Returns a list of all findings for a specific project or generates SARIF file if Accept:
    application/sarif+json header is provided

     <p>Requires permission <strong>VIEW_VULNERABILITY</strong></p>

    Args:
        uuid (UUID):
        suppressed (Union[Unset, bool]):
        source (Union[Unset, GetFindingsByProjectSource]):
        accept (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        suppressed=suppressed,
        source=source,
        accept=accept,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
