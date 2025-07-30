from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    show_inactive: Union[Unset, bool] = UNSET,
    show_suppressed: Union[Unset, bool] = UNSET,
    severity: Union[Unset, str] = UNSET,
    analysis_status: Union[Unset, str] = UNSET,
    vendor_response: Union[Unset, str] = UNSET,
    publish_date_from: Union[Unset, str] = UNSET,
    publish_date_to: Union[Unset, str] = UNSET,
    attributed_on_date_from: Union[Unset, str] = UNSET,
    attributed_on_date_to: Union[Unset, str] = UNSET,
    text_search_field: Union[Unset, str] = UNSET,
    text_search_input: Union[Unset, str] = UNSET,
    cvssv_2_from: Union[Unset, str] = UNSET,
    cvssv_2_to: Union[Unset, str] = UNSET,
    cvssv_3_from: Union[Unset, str] = UNSET,
    cvssv_3_to: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["showInactive"] = show_inactive

    params["showSuppressed"] = show_suppressed

    params["severity"] = severity

    params["analysisStatus"] = analysis_status

    params["vendorResponse"] = vendor_response

    params["publishDateFrom"] = publish_date_from

    params["publishDateTo"] = publish_date_to

    params["attributedOnDateFrom"] = attributed_on_date_from

    params["attributedOnDateTo"] = attributed_on_date_to

    params["textSearchField"] = text_search_field

    params["textSearchInput"] = text_search_input

    params["cvssv2From"] = cvssv_2_from

    params["cvssv2To"] = cvssv_2_to

    params["cvssv3From"] = cvssv_3_from

    params["cvssv3To"] = cvssv_3_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/finding",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Any]:
    if response.status_code == 401:
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
    *,
    client: AuthenticatedClient,
    show_inactive: Union[Unset, bool] = UNSET,
    show_suppressed: Union[Unset, bool] = UNSET,
    severity: Union[Unset, str] = UNSET,
    analysis_status: Union[Unset, str] = UNSET,
    vendor_response: Union[Unset, str] = UNSET,
    publish_date_from: Union[Unset, str] = UNSET,
    publish_date_to: Union[Unset, str] = UNSET,
    attributed_on_date_from: Union[Unset, str] = UNSET,
    attributed_on_date_to: Union[Unset, str] = UNSET,
    text_search_field: Union[Unset, str] = UNSET,
    text_search_input: Union[Unset, str] = UNSET,
    cvssv_2_from: Union[Unset, str] = UNSET,
    cvssv_2_to: Union[Unset, str] = UNSET,
    cvssv_3_from: Union[Unset, str] = UNSET,
    cvssv_3_to: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Returns a list of all findings

     <p>Requires permission <strong>VIEW_VULNERABILITY</strong></p>

    Args:
        show_inactive (Union[Unset, bool]):
        show_suppressed (Union[Unset, bool]):
        severity (Union[Unset, str]):
        analysis_status (Union[Unset, str]):
        vendor_response (Union[Unset, str]):
        publish_date_from (Union[Unset, str]):
        publish_date_to (Union[Unset, str]):
        attributed_on_date_from (Union[Unset, str]):
        attributed_on_date_to (Union[Unset, str]):
        text_search_field (Union[Unset, str]):
        text_search_input (Union[Unset, str]):
        cvssv_2_from (Union[Unset, str]):
        cvssv_2_to (Union[Unset, str]):
        cvssv_3_from (Union[Unset, str]):
        cvssv_3_to (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        show_inactive=show_inactive,
        show_suppressed=show_suppressed,
        severity=severity,
        analysis_status=analysis_status,
        vendor_response=vendor_response,
        publish_date_from=publish_date_from,
        publish_date_to=publish_date_to,
        attributed_on_date_from=attributed_on_date_from,
        attributed_on_date_to=attributed_on_date_to,
        text_search_field=text_search_field,
        text_search_input=text_search_input,
        cvssv_2_from=cvssv_2_from,
        cvssv_2_to=cvssv_2_to,
        cvssv_3_from=cvssv_3_from,
        cvssv_3_to=cvssv_3_to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    show_inactive: Union[Unset, bool] = UNSET,
    show_suppressed: Union[Unset, bool] = UNSET,
    severity: Union[Unset, str] = UNSET,
    analysis_status: Union[Unset, str] = UNSET,
    vendor_response: Union[Unset, str] = UNSET,
    publish_date_from: Union[Unset, str] = UNSET,
    publish_date_to: Union[Unset, str] = UNSET,
    attributed_on_date_from: Union[Unset, str] = UNSET,
    attributed_on_date_to: Union[Unset, str] = UNSET,
    text_search_field: Union[Unset, str] = UNSET,
    text_search_input: Union[Unset, str] = UNSET,
    cvssv_2_from: Union[Unset, str] = UNSET,
    cvssv_2_to: Union[Unset, str] = UNSET,
    cvssv_3_from: Union[Unset, str] = UNSET,
    cvssv_3_to: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Returns a list of all findings

     <p>Requires permission <strong>VIEW_VULNERABILITY</strong></p>

    Args:
        show_inactive (Union[Unset, bool]):
        show_suppressed (Union[Unset, bool]):
        severity (Union[Unset, str]):
        analysis_status (Union[Unset, str]):
        vendor_response (Union[Unset, str]):
        publish_date_from (Union[Unset, str]):
        publish_date_to (Union[Unset, str]):
        attributed_on_date_from (Union[Unset, str]):
        attributed_on_date_to (Union[Unset, str]):
        text_search_field (Union[Unset, str]):
        text_search_input (Union[Unset, str]):
        cvssv_2_from (Union[Unset, str]):
        cvssv_2_to (Union[Unset, str]):
        cvssv_3_from (Union[Unset, str]):
        cvssv_3_to (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        show_inactive=show_inactive,
        show_suppressed=show_suppressed,
        severity=severity,
        analysis_status=analysis_status,
        vendor_response=vendor_response,
        publish_date_from=publish_date_from,
        publish_date_to=publish_date_to,
        attributed_on_date_from=attributed_on_date_from,
        attributed_on_date_to=attributed_on_date_to,
        text_search_field=text_search_field,
        text_search_input=text_search_input,
        cvssv_2_from=cvssv_2_from,
        cvssv_2_to=cvssv_2_to,
        cvssv_3_from=cvssv_3_from,
        cvssv_3_to=cvssv_3_to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
