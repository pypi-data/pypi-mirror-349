from .auth import Auth
from .surface import Surface
from .component import Component
from .city import City
from .errors import RequestError
from .order import Order
from .financing import Financing
from .responses import RegisterResponse
from typing import Literal
import requests
import os


class FortlevSolarClient:
    """
    Client for interacting with the Fortlev Solar API. Provides methods for authentication
    and retrieving data related to surfaces, components, cities, and orders.

    Attributes:
        base_url (str): The base URL of the Fortlev Solar API.

    Methods:
        register: Register a new partner in the Fortlev Solar
        authenticate: Authenticates the user and sets authorization headers.
        surfaces: Retrieves a list of available surfaces.
        components: Retrieves a list of available components.
        cities: Retrieves a list of cities with specific details.
        orders: Retrieves orders based on given parameters.
        financing: Retrieves financing options based on the specified investment value.
    """

    BASE_URLS = {
        "DEV": "https://homolog.fortlevsolar.app/api",
        "PROD": "https://fortlevsolar.app/api",
    }

    def __init__(self, env: Literal["DEV", "PROD"] = "PROD") -> None:
        if env not in self.BASE_URLS:
            raise ValueError(f"Invalid environment: {env}. Use 'PROD' or 'DEV'.")
        self.base_url = self.BASE_URLS[env]
        self._username = os.getenv("FORTLEV_SOLAR_USERNAME")
        self._password = os.getenv("FORTLEV_SOLAR_PWD")
        self._auth = None
        self._headers = None

    def register(
        self, name: str, email: str, phone_number: str, cnpj: str, pwd: str
    ) -> RegisterResponse:
        """Register a new partner in Fortlev Solar.

        This method sends a request to [POST] /user/sign-up

        Args:
            name (str): The name of the user to be registered.
            email (str): The email address of the user. Must be a valid email format.
            phone_number (str): The user's phone number. Must contain 11 digits.
            cnpj (str): The CNPJ number of the user or company. Must follow CNPJ formatting rules.
            pwd (str): The password for the user's account. Must meet specified complexity requirements.

        Returns:
            SignUpResponse: An instance containing a message and the validation status of the email.

        Raises:
            RequestError: If the registration request fails or if the server returns an error response.
        """
        url = f"{self.base_url}/user/sign-up"
        _json = {
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "cnpj": cnpj,
            "password": pwd,
        }
        response = requests.post(url=url, json=_json)
        if response.status_code == 200:
            is_valid = response.json().get("email", {}).get("status")
            message = response.json().get("message", "Unknown message")
            return RegisterResponse(message=message, is_valid=is_valid)
        raise RequestError(
            status_code=response.status_code,
            error_message=response.json().get("detail", "Unknown error"),
        )

    def authenticate(self, username: str, pwd: str) -> Auth:
        """
        Authenticates the client with the provided username and password.

        This method sends a request to [POST] /user/login

        Args:
            username (str): The username for authentication.
            pwd (str): The password for authentication.

        Returns:
            Auth: The authentication details if successful.

        Raises:
            RequestError: If the authentication fails.
        """
        url = f"{self.base_url}/user/login"
        form_body = {"username": username, "password": pwd}
        response = requests.post(url=url, data=form_body)
        if response.status_code == 200:
            self._auth = Auth(
                access_token=response.json().get("access_token"),
                scope=response.json().get("scope"),
                token_type=response.json().get("token_type"),
            )
            token = f"{self._auth.token_type} {self._auth.access_token}"
            self._headers = {"Authorization": token}
            self._username = username
            self._password = pwd
            return self._auth
        raise RequestError(
            status_code=response.status_code,
            error_message=response.json().get("detail", "Unknown error"),
        )

    def _check_auth(self) -> None:
        """
        Checks if the client is authenticated. Raises an error if not authenticated.
        Additionally, it verifies if the token has expired and renews it if necessary.

        Raises:
            RequestError: If the client is not authenticated.
        """
        if self._auth is None:
            raise RequestError(
                status_code=401,
                error_message="User is not authenticated. Please call authenticate().",
            )
        if self._auth.is_expired():
            self.authenticate(username=self._username, pwd=self._password)

    def base_get_request(
        self, endpoint: str, Model, query_params: dict = {}
    ) -> list[object]:
        """
        Sends a GET request to the specified endpoint with optional query parameters.

        Args:
            endpoint (str): The endpoint to request data from.
            Model (type): The model class to parse the response data into.
            query_params (dict, Optional): Optional query parameters for the request.

        Returns:
            list[Model]: A list of instances of the specified Model parsed from the response.

        Raises:
            RequestError: If the request fails.
        """
        self._check_auth()
        url = f"{self.base_url}/{self._auth.scope}/{endpoint}"
        response = requests.get(url=url, headers=self._headers, params=query_params)
        if response.status_code == 200:
            docs = response.json().get("docs")
            return [Model.from_dict(doc) for doc in docs]
        raise RequestError(
            status_code=response.status_code,
            error_message=response.json().get("detail", "Unknown error"),
        )

    def surfaces(self, query_params: dict = {}) -> list[Surface]:
        """
        Retrieves a list of available surfaces.

        This method sends a request to [GET] /surface

        Args:
            query_params (dict, Optional): Optional query parameters for filtering the surfaces.

        Returns:
            list[Surface]: A list of Surface instances.
        """
        return self.base_get_request(
            endpoint="surface/", Model=Surface, query_params=query_params
        )

    def components(self, query_params: dict = {}) -> list[Component]:
        """
        Retrieves a list of available components.

        This method sends a request to [GET] /component/all

        Args:
            query_params (dict, Optional): Optional query parameters for filtering the components.

        Returns:
            list[Component]: A list of Component instances.
        """
        return self.base_get_request(
            endpoint="component/all", Model=Component, query_params=query_params
        )

    def cities(self, query_params: dict = {}) -> list[City]:
        """
        Retrieves a list of cities with specific details.

        This method sends a request to [GET] /brazilian-city

        Args:
            query_params (dict, Optional): Optional query parameters for filtering the cities.

        Returns:
            list[City]: A list of City instances.
        """
        return self.base_get_request(
            endpoint="brazilian-city/", Model=City, query_params=query_params
        )

    def orders(
        self,
        power: float = 0,
        voltage: Literal["220", "380", "+"] = "220",
        phase: Literal[1, 2, 3] = 1,
        surface: str = None,
        city: str = None,
    ) -> list[Order]:
        """Retrieves a list of orders based on the given parameters.

        This method sends a request to [POST] /order

        Args:
            power (float, Optional): The target power for the order. Defaults to 0.
            voltage (Literal["220", "380", "+"], Optional): The voltage type. Defaults to "220".
            phase (Literal[1, 2, 3], Optional): The phase (1, 2, or 3). Defaults to 1.
            surface (str, Optional): The surface ID for the order. If None, no specific surface will be used. Defaults to None.
            city (str, Optional): The city ID for the order. If None, the user's registered city will be used. Defaults to None.

        Returns:
            list[Order]: A list of Order instances.

        Raises:
            RequestError: If the client is not authenticated or the API request fails.

        Tip:
            You can generate a catalog of available kits by setting `power=0`.

        Examples:
            Authenticate and retrieve a list of orders:

            >>> client = FortlevSolarClient()
            >>> client.authenticate(username="username", pwd="password")
            >>> orders = client.orders(power=5.0, voltage="220", phase=1, surface="surface_id", city="city_id")

        """
        self._check_auth()
        _json = {
            "target_power": power,
            "voltage": voltage,
            "phase": phase,
            "surface": surface,
            "brazilian_city": city,
        }
        response = requests.post(
            url=f"{self.base_url}/{self._auth.scope}/order/",
            headers=self._headers,
            json=_json,
        )
        if response.status_code == 200:
            return [Order.from_dict(order) for order in response.json()]
        raise RequestError(
            status_code=response.status_code,
            error_message=response.json().get("detail", "Unknown error"),
        )

    def financing(
        self,
        value: float,
        entry_value: float = 0,
        grace: Literal[1, 2, 3, 4, 5, 6] = 1,
    ) -> list[Financing]:
        """Retrieves financing options based on the specified investment value.

        This method sends a request to [POST] /financing/simplified

        Args:
            value (float): The total investment value.
            entry_value (float, optional): The upfront entry value. Defaults to 0.
            grace (Literal[1, 2, 3, 4, 5, 6], optional): The number of grace months before starting payments. Defaults to 1.

        Returns:
            list[Financing]: A list of Financing instances representing the available financing options.

        Raises:
            RequestError: If the request fails or if the API returns an error response.

        Examples:
            Authenticate and retrieve a list of financing:

            >>> client = FortlevSolarClient()
            >>> client.authenticate(username="username", pwd="password")
            >>> financing = client.financing(value=15000, entry_value=5000, grace=3)

        """
        _json = {"investment_value": value, "entry_value": entry_value, "grace": grace}
        response = requests.post(
            url=f"{self.base_url}/{self._auth.scope}/financing/simplified",
            headers=self._headers,
            json=_json,
        )
        if response.status_code == 200:
            return [Financing.from_dict(financing) for financing in response.json()]
        raise RequestError(
            status_code=response.status_code,
            error_message=response.json().get("detail", "Unknown error"),
        )
