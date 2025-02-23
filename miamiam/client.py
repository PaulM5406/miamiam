from datetime import datetime
from http import HTTPStatus
from typing import Any

import httpx
import structlog
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .models import Establishment
from .settings import settings

logger = structlog.get_logger()


class InseeClient:
    """Client for interacting with the INSEE SIRENE API."""

    def __init__(self) -> None:
        self.base_url = settings.api_url
        self._token: str | None = None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPError)),
    )
    async def _get_token(self) -> str:
        """Get OAuth2 token from INSEE authentication service."""
        if self._token is not None:
            return self._token

        auth = httpx.BasicAuth(settings.client_id, settings.client_secret)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/token",
                # form encoding
                data={"grant_type": "client_credentials", "validity_period": 604800},
                auth=auth,
                timeout=5.0,
            )
            response.raise_for_status()
            data = response.json()
            self._token = data["access_token"]
            return self._token

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPError)),
    )
    async def search_establishments(self, from_date: datetime) -> list[Establishment]:
        """Search for new food & beverage establishments."""
        token = await self._get_token()

        # NAF codes for restaurants, cafes, and pubs
        naf_codes = ["56.10A", "56.10B", "56.30Z"]
        naf_query = " OR ".join(naf_codes)

        query: dict[str, str] = {
            "q": f"(activitePrincipaleUniteLegale:{naf_query})",
            "debut": from_date.strftime("%Y-%m-%d"),
            "nombre": "100",
        }

        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api-sirene/3.11/siren/123456789",
                params=query,
                headers=headers,
                timeout=5.0,
            )
            if response.status_code == HTTPStatus.UNAUTHORIZED:
                self._token = None
                return await self.search_establishments(from_date)
            response.raise_for_status()

        return self._parse_response(response.json())

    def _parse_response(self, data: dict[str, Any]) -> list[Establishment]:
        """
        Parse the raw JSON response from the INSEE API into Establishment objects.
        """
        establishments = []
        for item in data.get("etablissements", []):
            try:
                establishments.append(
                    Establishment(
                        siret=item["siret"],
                        name=item["uniteLegale"]["denominationUniteLegale"],
                        address=item["adresseEtablissement"]["numeroVoieEtablissement"]
                        + " "
                        + item["adresseEtablissement"]["typeVoieEtablissement"]
                        + " "
                        + item["adresseEtablissement"]["libelleVoieEtablissement"],
                        postal_code=item["adresseEtablissement"]["codePostalEtablissement"],
                        city=item["adresseEtablissement"]["libelleCommuneEtablissement"],
                        activity_code=item["uniteLegale"]["activitePrincipaleUniteLegale"],
                        creation_date=datetime.strptime(
                            item["dateCreationEtablissement"], "%Y-%m-%d"
                        ),
                    )
                )
            except KeyError as e:
                logger.error("Failed to parse establishment", error=str(e))
                continue

        return establishments
