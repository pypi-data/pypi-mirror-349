from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import TypedDict
from zoneinfo import ZoneInfo

import requests
from loguru import logger
from requests.models import Response

Utilization = TypedDict(
    "Utilization",
    {
        "id": int,
        "capacity": int,
        "volume": int,
        "percentage": float,
        "emission": int,
        "emissionfactor": float,
        "validfrom": str,
        "validto": str,
    },
)
Result = TypedDict(
    "Result", {"hydra:totalItems": int, "hydra:member": list[Utilization]}
)


@dataclass
class EnergyData:
    co2_amount: float
    datetime_ams: datetime = field(init=False)
    datetime: datetime
    date_str: str = field(init=False)

    def __post_init__(self):
        self.datetime_ams = self.datetime.astimezone(ZoneInfo("Europe/Amsterdam"))
        self.date_str = self.datetime_ams.strftime("%a %d, %H:%M")


class API:
    def __init__(self, api_url, api_key, user_agent):
        self._base_url = api_url
        self._api_key = api_key
        self._user_agent = user_agent
        self._session = requests.Session()
        self._session.headers.update(self._headers)
        logger.debug("Set up to listen to api at {}", self._base_url)

    def get_data(self) -> EnergyData:
        # See https://ned.nl/nl/handleiding-api and https://ned.nl/nl/definities
        r: Result = self._get("/utilizations").json()
        utilization: Utilization = r["hydra:member"][0]

        return EnergyData(
            datetime=datetime.fromisoformat(utilization["validto"]),
            co2_amount=utilization["emissionfactor"],
        )

    def _get(self, url: str) -> Response:
        r = self._session.get(
            f"{self._base_url}{url}",
            params=self._params,
            timeout=15,
        )
        r.raise_for_status()
        return r

    @property
    def _params(self) -> dict:
        """The correct parameters for the Ned API. For more
        information about these params, check out the file
        CO2Monitor.org.

        """
        start = datetime.today().date()
        end = start + timedelta(days=1)
        return {
            "page": 1,
            "itemsPerPage": 1,
            "type": 27,  # ElectricityMix, see https://ned.nl/nl/definities
            "activity": 1,  # Providing
            "point": 0,  # ElectricityMix does not support local regions
            "granularity": 4,  # Most granular view supported
            "granularitytimezone": 0,  # UTC
            "classification": 2,  # Current status
            "validfrom[before]": end.isoformat(),
            "validfrom[after]": start.isoformat(),
            "order[validfrom]": "desc",
        }

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "user-agent": self._user_agent,
            "X-AUTH-TOKEN": self._api_key,
        }
