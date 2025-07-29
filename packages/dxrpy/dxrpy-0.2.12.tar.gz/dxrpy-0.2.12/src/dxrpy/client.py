from dxrpy.dxr_client import DXRHttpClient
from .index import Index
from .on_demand_classifier import OnDemandClassifier
from .document_categories import DocumentCategories
from dotenv import load_dotenv
import os

load_dotenv()


class DXRClient:
    """
    DXRClient is a client for interacting with the DXR API.

    Attributes:
        _on_demand_classifier (OnDemandClassifier): Lazy-loaded on-demand classifier.
        _index (Index): Lazy-loaded index.
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
        ignore_ssl: bool = False,
    ):
        """
        Initializes the DXRClient with the given base URL, API key, and SSL verification option.

        Args:
            base_url (str): The base URL for the DXR API.
            api_key (str): The API key for authenticating with the DXR API.
            ignore_ssl (bool): Whether to ignore SSL certificate verification.
        """
        api_url = api_url or os.getenv("DXR_BASE_URL")
        api_key = api_key or os.getenv("DXR_API_KEY")

        if not api_url or not api_key:
            raise ValueError("api_url and api_key must be provided.")

        DXRHttpClient.get_instance(api_url, api_key, ignore_ssl)
        self._on_demand_classifier = None
        self._index = None
        self._document_categories = None

    @property
    def on_demand_classifier(self):
        """
        Lazy-loads and returns the on-demand classifier.

        Returns:
            OnDemandClassifier: The on-demand classifier.
        """
        if self._on_demand_classifier is None:
            self._on_demand_classifier = OnDemandClassifier()
        return self._on_demand_classifier

    @property
    def index(self):
        """
        Lazy-loads and returns the index.

        Returns:
            Index: The index.
        """
        if self._index is None:
            self._index = Index()
        return self._index

    @property
    def document_categories(self):
        """
        Lazy-loads and returns the document categories.

        Returns:
            DocumentCategories: The document categories.
        """
        if self._document_categories is None:
            self._document_categories = DocumentCategories()
        return self._document_categories
