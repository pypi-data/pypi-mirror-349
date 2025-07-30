from universal_mcp.applications import APIApplication
from universal_mcp.integrations import Integration
import httpx

class HttpToolsApp(APIApplication):
    """
    Base class for Universal MCP Applications.
    """

    def __init__(self, integration: Integration = None, **kwargs) -> None:
        """
        Initialize the HttpToolsApp.

        Args:
            integration (Integration, optional): Integration instance to use. Example: Integration().
            **kwargs: Additional keyword arguments for the parent APIApplication.
        """
        super().__init__(name="http-tools", integration=integration, **kwargs)

    def http_get(self, url: str, headers: dict = None, query_params: dict = None):
        """
        Perform a GET request to the specified URL with optional parameters.

        Args:
            url (str): The URL to send the GET request to. Example: "https://api.example.com/data"
            headers (dict, optional): Optional HTTP headers to include in the request. Example: {"Authorization": "Bearer token"}
            query_params (dict, optional): Optional dictionary of query parameters to include in the request. Example: {"page": 1}

        Returns:
            dict: The JSON response from the GET request.
        """
        response = httpx.get(url, params=query_params, headers=headers)
        return response.json()

    def http_post(self, url: str, headers: dict = None, body: dict = None):
        """
        Perform a POST request to the specified URL with optional parameters.

        Args:
            url (str): The URL to send the POST request to. Example: "https://api.example.com/data"
            headers (dict, optional): Optional HTTP headers to include in the request. Example: {"Content-Type": "application/json"}
            body (dict, optional): Optional JSON body to include in the request. Example: {"name": "John"}

        Returns:
            dict: The JSON response from the POST request.
        """
        response = httpx.post(url, json=body, headers=headers)
        return response.json()
    
    def http_put(self, url: str, headers: dict = None, body: dict = None):
        """
        Perform a PUT request to the specified URL with optional parameters.

        Args:
            url (str): The URL to send the PUT request to. Example: "https://api.example.com/data/1"
            headers (dict, optional): Optional HTTP headers to include in the request. Example: {"Authorization": "Bearer token"}
            body (dict, optional): Optional JSON body to include in the request. Example: {"name": "Jane"}

        Returns:
            dict: The JSON response from the PUT request.
        """
        response = httpx.put(url, json=body, headers=headers)
        return response.json()
    
    def http_delete(self, url: str, headers: dict = None, body: dict = None):
        """
        Perform a DELETE request to the specified URL with optional parameters.

        Args:
            url (str): The URL to send the DELETE request to. Example: "https://api.example.com/data/1"
            headers (dict, optional): Optional HTTP headers to include in the request. Example: {"Authorization": "Bearer token"}
            body (dict, optional): Optional JSON body to include in the request. Example: {"reason": "obsolete"}

        Returns:
            dict: The JSON response from the DELETE request.
        """
        response = httpx.delete(url, json=body, headers=headers)
        return response.json()
    
    def http_patch(self, url: str, headers: dict = None, body: dict = None):
        """
        Perform a PATCH request to the specified URL with optional parameters.

        Args:
            url (str): The URL to send the PATCH request to. Example: "https://api.example.com/data/1"
            headers (dict, optional): Optional HTTP headers to include in the request. Example: {"Authorization": "Bearer token"}
            body (dict, optional): Optional JSON body to include in the request. Example: {"status": "active"}

        Returns:
            dict: The JSON response from the PATCH request.
        """
        response = httpx.patch(url, json=body, headers=headers)
        return response.json()
    
    def list_tools(self):
        """
        Lists the available tools (methods) for this application.
        """
        return [self.http_get, self.http_post, self.http_put, self.http_delete, self.http_patch]
