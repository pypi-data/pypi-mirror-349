from typing import Any, Dict, Optional
from universal_mcp.applications import APIApplication
from universal_mcp.integrations import Integration
from loguru import logger

class ApolloApp(APIApplication):
    def __init__(self, integration: Integration = None, **kwargs) -> None:
        super().__init__(name='apollo', integration=integration, **kwargs)
        self.base_url = "https://api.apollo.io/api/v1"

    def _get_headers(self) -> Dict[str, str]:
        """
        Get the headers for Apollo API requests.
        Overrides the base class method to use X-Api-Key.
        """
        if not self.integration:
            logger.warning("ApolloApp: No integration configured, returning empty headers.")
            return {}
        
        # ApiKeyIntegration's get_credentials() returns a dict like:
        # {'api_key': 'your_actual_key_value'}
        credentials = self.integration.get_credentials()
        
        # The key in the credentials dict from ApiKeyIntegration is 'api_key'
        api_key = credentials.get("api_key") or credentials.get("API_KEY") or credentials.get("apiKey")
        
        if not api_key:
            logger.error("ApolloApp: API key not found in integration credentials for Apollo.")
            # You might want to raise an error here if an API key is absolutely required
            # For example: raise ValueError("API key is missing for Apollo integration.")
            return { # Or return minimal headers if some calls might not need auth (unlikely for Apollo)
                "Content-Type": "application/json",
                "Cache-Control": "no-cache"
            }

        logger.debug("ApolloApp: Using X-Api-Key for authentication.")
        return {
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache" # Often good practice for APIs
        }

    def people_enrichment(self, first_name: Optional[str] = None, last_name: Optional[str] = None, name: Optional[str] = None, email: Optional[str] = None, hashed_email: Optional[str] = None, organization_name: Optional[str] = None, domain: Optional[str] = None, id: Optional[str] = None, linkedin_url: Optional[str] = None, reveal_personal_emails: Optional[bool] = None, reveal_phone_number: Optional[bool] = None, webhook_url: Optional[str] = None) -> dict[str, Any]:
        """
        Matches a person's profile based on provided identifiers such as name, email, organization, or LinkedIn URL, with options to reveal personal emails and phone numbers.

        Args:
            first_name (string): The first_name query parameter specifies the first name used to match people in the POST /people/match operation.
            last_name (string): The last_name parameter, provided in the query string of the POST request, specifies the person's last name to match against records in the system.
            name (string): Name of the person to match, provided as a query parameter in the POST request.
            email (string): The email address used as a query parameter to identify or match a person in the POST /people/match request.
            hashed_email (string): Hashed email address used as a query parameter to identify or match a person in the POST /people/match operation.
            organization_name (string): The name of the organization to match people against, provided as a query string parameter.
            domain (string): The domain to match people against, provided as a query string parameter.
            id (string): The unique identifier for the person to be matched, provided as a query string parameter.
            linkedin_url (string): The LinkedIn profile URL of the person to be matched.
            reveal_personal_emails (boolean): Optional boolean query parameter indicating whether to include personal emails in the response, defaulting to false.
            reveal_phone_number (boolean): Boolean query parameter to indicate whether to include the person's phone number in the response, defaulting to false.
            webhook_url (string): Specifies the HTTPS endpoint URL to which webhook event notifications will be sent when a matching operation is completed.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            People, important
        """
        request_body_data = None
        url = f"{self.base_url}/people/match"
        query_params = {k: v for k, v in [('first_name', first_name), ('last_name', last_name), ('name', name), ('email', email), ('hashed_email', hashed_email), ('organization_name', organization_name), ('domain', domain), ('id', id), ('linkedin_url', linkedin_url), ('reveal_personal_emails', reveal_personal_emails), ('reveal_phone_number', reveal_phone_number), ('webhook_url', webhook_url)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def bulk_people_enrichment(self, reveal_personal_emails: Optional[bool] = None, reveal_phone_number: Optional[bool] = None, webhook_url: Optional[str] = None, details: Optional[list[dict[str, Any]]] = None) -> dict[str, Any]:
        """
        Performs a bulk matching operation for people records using posted data, with options to reveal personal emails or phone numbers and specify a webhook URL for result delivery.

        Args:
            reveal_personal_emails (boolean): Indicates whether to include personal emails in the bulk match results for people, defaulting to false if not specified.
            reveal_phone_number (boolean): If set to true, includes the phone number in the bulk match response; defaults to false.
            webhook_url (string): Specifies the URL to which webhook notifications are sent when the bulk match operation completes.
            details (array): Provide info for each person you want to enrich as an object within this array. Add up to 10 people.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            People    
        """
        request_body_data = None
        request_body_data = {
            'details': details,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/people/bulk_match"
        query_params = {k: v for k, v in [('reveal_personal_emails', reveal_personal_emails), ('reveal_phone_number', reveal_phone_number), ('webhook_url', webhook_url)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def organization_enrichment(self, domain: str) -> dict[str, Any]:
        """
        Retrieves enriched organizational data such as industry, revenue, employee count, funding details, and contact information based on a provided domain.

        Args:
            domain (string): The domain name of the organization to enrich information for, provided as a required query string parameter.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Organizations    
        """
        url = f"{self.base_url}/organizations/enrich"
        query_params = {k: v for k, v in [('domain', domain)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def bulk_organization_enrichment(self, domains_: list[str]) -> dict[str, Any]:
        """
        Enriches multiple organization profiles by accepting a list of domains and returns detailed data for each, allowing for efficient bulk processing.

        Args:
            domains_ (array): An array of domain names to be enriched in bulk for organizational information.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Organizations    
        """
        request_body_data = None
        url = f"{self.base_url}/organizations/bulk_enrich"
        query_params = {k: v for k, v in [('domains[]', domains_)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def people_search(self, person_titles_: Optional[list[str]] = None, include_similar_titles: Optional[bool] = None, person_locations_: Optional[list[str]] = None, person_seniorities_: Optional[list[str]] = None, organization_locations_: Optional[list[str]] = None, q_organization_domains_list_: Optional[list[str]] = None, contact_email_status_: Optional[list[str]] = None, organization_ids_: Optional[list[str]] = None, organization_num_employees_ranges_: Optional[list[str]] = None, q_keywords: Optional[str] = None, page: Optional[int] = None, per_page: Optional[int] = None) -> dict[str, Any]:
        """
        Searches for people by specified criteria such as titles, locations, seniorities, organization details, and additional filters, returning paginated results via a POST request.

        Args:
            person_titles_ (array): An array of person titles to filter the search results by.
            include_similar_titles (boolean): Include similar titles in the search results when set to true; optional boolean query parameter. Example: 'true'.
            person_locations_ (array): An array of location identifiers to filter the search results by specific person locations.
            person_seniorities_ (array): An optional array of seniority levels to filter the people in the search results.
            organization_locations_ (array): An array of organization location identifiers to filter the search results by specific locations.
            q_organization_domains_list_ (array): An optional query parameter array to filter search results by one or more organization domain names.
            contact_email_status_ (array): Filter results to only include people whose contact email status matches any of the specified values from the provided array.
            organization_ids_ (array): An array of organization IDs to filter search results by organization membership.
            organization_num_employees_ranges_ (array): An array of employee count ranges used to filter organizations by their number of employees in the search query.
            q_keywords (string): Keyword search query for filtering results in the mixed people search operation.
            page (integer): The "page" parameter is an integer query parameter used to specify the page number for pagination in the search results.
            per_page (integer): Number of results to return per page in the search response; optional integer query parameter.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            People    
        """
        request_body_data = None
        url = f"{self.base_url}/mixed_people/search"
        query_params = {k: v for k, v in [('person_titles[]', person_titles_), ('include_similar_titles', include_similar_titles), ('person_locations[]', person_locations_), ('person_seniorities[]', person_seniorities_), ('organization_locations[]', organization_locations_), ('q_organization_domains_list[]', q_organization_domains_list_), ('contact_email_status[]', contact_email_status_), ('organization_ids[]', organization_ids_), ('organization_num_employees_ranges[]', organization_num_employees_ranges_), ('q_keywords', q_keywords), ('page', page), ('per_page', per_page)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def organization_search(self, organization_num_employees_ranges_: Optional[list[str]] = None, organization_locations_: Optional[list[str]] = None, organization_not_locations_: Optional[list[str]] = None, revenue_range_min: Optional[int] = None, revenue_range_max: Optional[int] = None, currently_using_any_of_technology_uids_: Optional[list[str]] = None, q_organization_keyword_tags_: Optional[list[str]] = None, q_organization_name: Optional[str] = None, organization_ids_: Optional[list[str]] = None, page: Optional[int] = None, per_page: Optional[int] = None) -> dict[str, Any]:
        """
        Searches for mixed companies based on various filters such as employee ranges, locations, revenue, technologies used, keywords, and pagination parameters.

        Args:
            organization_num_employees_ranges_ (array): An array of employee count ranges used to filter organizations by their number of employees in the search query.
            organization_locations_ (array): An array of organization location identifiers to filter the search results by specific locations.
            organization_not_locations_ (array): An array of location identifiers to exclude from the organization search results.
            revenue_range_min (integer): Minimum revenue value (integer) to filter companies by their revenue range in the search query.
            revenue_range_max (integer): The maximum revenue value for filtering companies in the search results.
            currently_using_any_of_technology_uids_ (array): An array of technology unique identifiers (UIDs) to filter companies currently using any of the specified technologies.
            q_organization_keyword_tags_ (array): An array of keyword tags to filter and search organizations by relevant descriptors.
            q_organization_name (string): Filter the search results by the organization name specified.
            organization_ids_ (array): An array of organization IDs to filter the search results by specific organizations.
            page (integer): The page parameter specifies the page number of results to retrieve in the search query for paginated responses.
            per_page (integer): The number of results to return per page in the paginated response.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Organizations    
        """
        request_body_data = None
        url = f"{self.base_url}/mixed_companies/search"
        query_params = {k: v for k, v in [('organization_num_employees_ranges[]', organization_num_employees_ranges_), ('organization_locations[]', organization_locations_), ('organization_not_locations[]', organization_not_locations_), ('revenue_range[min]', revenue_range_min), ('revenue_range[max]', revenue_range_max), ('currently_using_any_of_technology_uids[]', currently_using_any_of_technology_uids_), ('q_organization_keyword_tags[]', q_organization_keyword_tags_), ('q_organization_name', q_organization_name), ('organization_ids[]', organization_ids_), ('page', page), ('per_page', per_page)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def organization_jobs_postings(self, organization_id: str, page: Optional[int] = None, per_page: Optional[int] = None) -> dict[str, Any]:
        """
        Retrieves a paginated list of job postings for the specified organization by organization_id.

        Args:
            organization_id (string): organization_id
            page (integer): The "page" parameter specifies the page number for pagination when retrieving job postings for a specific organization.
            per_page (integer): The number of job postings to return per page in the paginated response.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Organizations    
        """
        if organization_id is None:
            raise ValueError("Missing required parameter 'organization_id'.")
        url = f"{self.base_url}/organizations/{organization_id}/job_postings"
        query_params = {k: v for k, v in [('page', page), ('per_page', per_page)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def create_an_account(self, name: Optional[str] = None, domain: Optional[str] = None, owner_id: Optional[str] = None, account_stage_id: Optional[str] = None, phone: Optional[str] = None, raw_address: Optional[str] = None) -> dict[str, Any]:
        """
        Creates a new account resource using provided query parameters such as name, domain, owner ID, account stage ID, phone, and raw address.

        Args:
            name (string): Optional string parameter used to specify the name associated with the account being created.
            domain (string): The domain query parameter specifies the domain associated with the account being created.
            owner_id (string): Specifies the identifier of the account owner for the POST operation at the "/accounts" path.
            account_stage_id (string): Identifies the account stage by its unique ID for filtering or processing accounts in the POST request.
            phone (string): Optional phone number provided as a string to be used during the account creation process.
            raw_address (string): The raw_address query parameter is a string representing the unprocessed or original address input to be used in the account creation request.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Accounts    
        """
        request_body_data = None
        url = f"{self.base_url}/accounts"
        query_params = {k: v for k, v in [('name', name), ('domain', domain), ('owner_id', owner_id), ('account_stage_id', account_stage_id), ('phone', phone), ('raw_address', raw_address)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def update_an_account(self, account_id: str, name: Optional[str] = None, domain: Optional[str] = None, owner_id: Optional[str] = None, account_stage_id: Optional[str] = None, raw_address: Optional[str] = None, phone: Optional[str] = None) -> dict[str, Any]:
        """
        Updates the account identified by {account_id} with new provided values or replaces its details if required, supporting various account attributes as query parameters[1][2][5].

        Args:
            account_id (string): account_id
            name (string): Optional query parameter to specify the name associated with the account during the update operation.
            domain (string): The domain query parameter specifies the domain associated with the account to be updated.
            owner_id (string): Specifies the unique identifier of the owner as a query string parameter for updating an account.
            account_stage_id (string): The `account_stage_id` query parameter specifies the identifier of the stage to which the account should be updated.
            raw_address (string): The raw_address query parameter is a string representing the unstructured or original address data to update for the specified account.
            phone (string): The phone number to update for the specified account, provided as a query string parameter.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Accounts    
        """
        if account_id is None:
            raise ValueError("Missing required parameter 'account_id'.")
        request_body_data = None
        url = f"{self.base_url}/accounts/{account_id}"
        query_params = {k: v for k, v in [('name', name), ('domain', domain), ('owner_id', owner_id), ('account_stage_id', account_stage_id), ('raw_address', raw_address), ('phone', phone)] if v is not None}
        response = self._put(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def search_for_accounts(self, q_organization_name: Optional[str] = None, account_stage_ids_: Optional[list[str]] = None, sort_by_field: Optional[str] = None, sort_ascending: Optional[bool] = None, page: Optional[int] = None, per_page: Optional[int] = None) -> dict[str, Any]:
        """
        Searches for accounts using the specified organization name, account stages, and sorting preferences, returning a paginated list of results.

        Args:
            q_organization_name (string): Search for accounts by specifying the organization name in this query parameter.
            account_stage_ids_ (array): Filter accounts by specifying one or more account stage IDs to include in the search results.
            sort_by_field (string): The "sort_by_field" query parameter specifies the name of the field by which the search results should be sorted in the account search operation.
            sort_ascending (boolean): If true, results will be sorted in ascending order; defaults to false (descending order).
            page (integer): The page query parameter specifies the page number of the search results to retrieve for the accounts search operation.
            per_page (integer): Controls the number of results returned per page in the search results.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Accounts    
        """
        request_body_data = None
        url = f"{self.base_url}/accounts/search"
        query_params = {k: v for k, v in [('q_organization_name', q_organization_name), ('account_stage_ids[]', account_stage_ids_), ('sort_by_field', sort_by_field), ('sort_ascending', sort_ascending), ('page', page), ('per_page', per_page)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def update_account_stage(self, account_ids_: list[str], account_stage_id: str) -> dict[str, Any]:
        """
        Updates multiple accounts in bulk using the provided account IDs and stage ID.

        Args:
            account_ids_ (array): Array of account IDs to be updated in bulk, passed as query parameters and required for the operation.
            account_stage_id (string): Specifies the unique identifier of the account stage to apply in the bulk update operation.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Accounts    
        """
        request_body_data = None
        url = f"{self.base_url}/accounts/bulk_update"
        query_params = {k: v for k, v in [('account_ids[]', account_ids_), ('account_stage_id', account_stage_id)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def update_account_ownership(self, account_ids_: list[str], owner_id: str) -> dict[str, Any]:
        """
        Updates the owners of multiple accounts by specifying the account IDs and the new owner ID via a POST request.

        Args:
            account_ids_ (array): Array of account IDs to update owners for, specified as query parameters for POST /accounts/update_owners, required.
            owner_id (string): The unique identifier of the owner to update, passed as a required query parameter.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:        
            Accounts    
        """
        request_body_data = None
        url = f"{self.base_url}/accounts/update_owners"
        query_params = {k: v for k, v in [('account_ids[]', account_ids_), ('owner_id', owner_id)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def list_account_stages(self) -> dict[str, Any]:
        """
        Retrieves a list of account stages available in the system.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Accounts    
        """
        url = f"{self.base_url}/account_stages"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def create_a_contact(self, first_name: Optional[str] = None, last_name: Optional[str] = None, organization_name: Optional[str] = None, title: Optional[str] = None, account_id: Optional[str] = None, email: Optional[str] = None, website_url: Optional[str] = None, label_names_: Optional[list[str]] = None, contact_stage_id: Optional[str] = None, present_raw_address: Optional[str] = None, direct_phone: Optional[str] = None, corporate_phone: Optional[str] = None, mobile_phone: Optional[str] = None, home_phone: Optional[str] = None, other_phone: Optional[str] = None) -> dict[str, Any]:
        """
        Creates a new contact record with provided details such as name, organization, title, email, account ID, phone numbers, address, and labels, returning a success or error response.

        Args:
            first_name (string): The first_name query parameter specifies the contact's first name as a string for the POST /contacts operation.
            last_name (string): The last_name query parameter specifies the contact's last name as a string for the POST /contacts operation.
            organization_name (string): Specifies the name of the organization to associate with the contact being created.
            title (string): The "title" query parameter is a string used to specify the title associated with the contact being created.
            account_id (string): Identifies the account associated with the contact being created.
            email (string): The email address to associate with the new contact, provided as a query string parameter.
            website_url (string): The website_url query parameter specifies the URL of the contact's website to be associated when creating a contact.
            label_names_ (array): An array of label names to assign to the contact, passed as query parameters.
            contact_stage_id (string): The contact_stage_id query parameter specifies the identifier of the contact stage to assign to the new contact.
            present_raw_address (string): Indicates whether to include the raw address in the contact information.
            direct_phone (string): The direct_phone query parameter specifies the direct phone number associated with the contact being created.
            corporate_phone (string): Optional string parameter to specify the corporate phone number of a contact.
            mobile_phone (string): The mobile_phone query parameter is a string used to specify the contact's mobile phone number when creating a new contact via the POST /contacts endpoint.
            home_phone (string): The home_phone query parameter is a string representing the contact's home phone number to be included when creating a new contact.
            other_phone (string): Additional phone number for the contact provided as a query parameter.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Contacts    
        """
        request_body_data = None
        url = f"{self.base_url}/contacts"
        query_params = {k: v for k, v in [('first_name', first_name), ('last_name', last_name), ('organization_name', organization_name), ('title', title), ('account_id', account_id), ('email', email), ('website_url', website_url), ('label_names[]', label_names_), ('contact_stage_id', contact_stage_id), ('present_raw_address', present_raw_address), ('direct_phone', direct_phone), ('corporate_phone', corporate_phone), ('mobile_phone', mobile_phone), ('home_phone', home_phone), ('other_phone', other_phone)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def update_a_contact(self, contact_id: str, first_name: Optional[str] = None, last_name: Optional[str] = None, organization_name: Optional[str] = None, title: Optional[str] = None, account_id: Optional[str] = None, email: Optional[str] = None, website_url: Optional[str] = None, label_names_: Optional[list[str]] = None, contact_stage_id: Optional[str] = None, present_raw_address: Optional[str] = None, direct_phone: Optional[str] = None, corporate_phone: Optional[str] = None, mobile_phone: Optional[str] = None, home_phone: Optional[str] = None, other_phone: Optional[str] = None) -> dict[str, Any]:
        """
        Updates an existing contact identified by contact_id with provided details such as name, organization, email, phone numbers, and labels.

        Args:
            contact_id (string): contact_id
            first_name (string): The first_name query parameter specifies the contact's first name to update for the given contact_id.
            last_name (string): The last name of the contact to update, provided as a string in the query parameters.
            organization_name (string): The organization_name query parameter specifies the name of the organization associated with the contact to be updated.
            title (string): A string query parameter used to specify the title, typically associated with a contact's role or designation, for the PUT operation at the /contacts/{contact_id} endpoint.
            account_id (string): Unique identifier of the account associated with the contact, used for authentication and authorization purposes.
            email (string): Optional string parameter for specifying the email address associated with the contact, used in the query for updating a contact via the PUT operation.
            website_url (string): The website_url query parameter specifies the contact's website URL to be updated or set.
            label_names_ (array): An array of label names to be assigned to the contact, passed as separate query parameters.
            contact_stage_id (string): The contact_stage_id query parameter specifies the unique identifier of the stage to assign to the contact.
            present_raw_address (string): The raw present address of the contact to update, provided as a string in the query parameters.
            direct_phone (string): Specifies the direct phone number to be updated for the contact, provided as a string in the query string.
            corporate_phone (string): The corporate_phone query parameter specifies the contact's corporate phone number as a string for updating the contact information.
            mobile_phone (string): The mobile_phone query parameter specifies the updated mobile phone number for the contact identified by contact_id.
            home_phone (string): The home_phone query parameter specifies the contact's home phone number to be updated.
            other_phone (string): Optional phone number for an alternative or secondary contact method, included as a query parameter.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Contacts    
        """
        if contact_id is None:
            raise ValueError("Missing required parameter 'contact_id'.")
        request_body_data = None
        url = f"{self.base_url}/contacts/{contact_id}"
        query_params = {k: v for k, v in [('first_name', first_name), ('last_name', last_name), ('organization_name', organization_name), ('title', title), ('account_id', account_id), ('email', email), ('website_url', website_url), ('label_names[]', label_names_), ('contact_stage_id', contact_stage_id), ('present_raw_address', present_raw_address), ('direct_phone', direct_phone), ('corporate_phone', corporate_phone), ('mobile_phone', mobile_phone), ('home_phone', home_phone), ('other_phone', other_phone)] if v is not None}
        response = self._put(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def search_for_contacts(self, q_keywords: Optional[str] = None, contact_stage_ids_: Optional[list[str]] = None, sort_by_field: Optional[str] = None, sort_ascending: Optional[bool] = None, per_page: Optional[int] = None, page: Optional[int] = None) -> dict[str, Any]:
        """
        Searches contacts based on keywords, contact stage IDs, and other query parameters, returning a paginated and sortable list of matching contacts.

        Args:
            q_keywords (string): String parameter for specifying keywords to search for in contacts.
            contact_stage_ids_ (array): Array of contact stage IDs to filter contacts by their associated stages in the search query.
            sort_by_field (string): The "sort_by_field" query parameter specifies the field name by which the search results for contacts should be sorted.
            sort_ascending (boolean): Determines whether search results are sorted in ascending order; defaults to false if omitted.
            per_page (integer): The number of results to return per page in the search response.
            page (integer): The page query parameter specifies the integer page number for paginated search results in the contacts search operation.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Contacts    
        """
        request_body_data = None
        url = f"{self.base_url}/contacts/search"
        query_params = {k: v for k, v in [('q_keywords', q_keywords), ('contact_stage_ids[]', contact_stage_ids_), ('sort_by_field', sort_by_field), ('sort_ascending', sort_ascending), ('per_page', per_page), ('page', page)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def update_contact_stage(self, contact_ids_: list[str], contact_stage_id: str) -> dict[str, Any]:
        """
        Updates the stages of specified contacts using their IDs and a target stage ID.

        Args:
            contact_ids_ (array): Array of contact IDs to specify which contacts' stages should be updated in the request.
            contact_stage_id (string): The unique identifier of the contact stage to update, provided as a required query parameter.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Contacts    
        """
        request_body_data = None
        url = f"{self.base_url}/contacts/update_stages"
        query_params = {k: v for k, v in [('contact_ids[]', contact_ids_), ('contact_stage_id', contact_stage_id)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def update_contact_ownership(self, contact_ids_: list[str], owner_id: str) -> dict[str, Any]:
        """
        Updates the owners of multiple contacts by assigning a specified owner ID to the given list of contact IDs.

        Args:
            contact_ids_ (array): Array of contact IDs to specify which contacts' owners should be updated.
            owner_id (string): The "owner_id" parameter is a required string value passed in the query string, specifying the ID of the owner to be updated in the contact.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Contacts    
        """
        request_body_data = None
        url = f"{self.base_url}/contacts/update_owners"
        query_params = {k: v for k, v in [('contact_ids[]', contact_ids_), ('owner_id', owner_id)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def list_contact_stages(self) -> Any:
        """
        Retrieves a list of available contact stages from the system.

        Returns:
            Any: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Contacts    
        """
        url = f"{self.base_url}/contact_stages"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def create_deal(self, name: str, owner_id: Optional[str] = None, account_id: Optional[str] = None, amount: Optional[str] = None, opportunity_stage_id: Optional[str] = None, closed_date: Optional[str] = None) -> dict[str, Any]:
        """
        Creates a new opportunity with the specified parameters such as name, owner ID, account ID, amount, opportunity stage ID, and closed date.

        Args:
            name (string): The "name" query parameter is a required string specifying the name associated with the opportunity to be created.
            owner_id (string): The owner_id query parameter specifies the ID of the user who will be assigned as the owner of the opportunity.
            account_id (string): Unique identifier for the account associated with the opportunity, passed as a string query parameter.
            amount (string): Specifies the monetary amount, as a string, associated with the opportunity when creating or modifying it via a POST request.
            opportunity_stage_id (string): Unique identifier for the opportunity stage, passed as a query parameter.
            closed_date (string): The date when the opportunity was closed, provided as a string in the query parameters.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Deals    
        """
        request_body_data = None
        url = f"{self.base_url}/opportunities"
        query_params = {k: v for k, v in [('name', name), ('owner_id', owner_id), ('account_id', account_id), ('amount', amount), ('opportunity_stage_id', opportunity_stage_id), ('closed_date', closed_date)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def list_all_deals(self, sort_by_field: Optional[str] = None, page: Optional[int] = None, per_page: Optional[int] = None) -> dict[str, Any]:
        """
        Searches for opportunities with optional sorting and pagination parameters and returns the matching results.

        Args:
            sort_by_field (string): Specifies the field by which the search results for opportunities should be sorted.
            page (integer): Specifies the page number of results to retrieve from a paginated list of opportunities.
            per_page (integer): The number of results to return per page in the paginated response.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Deals    
        """
        url = f"{self.base_url}/opportunities/search"
        query_params = {k: v for k, v in [('sort_by_field', sort_by_field), ('page', page), ('per_page', per_page)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def update_deal(self, opportunity_id: str, owner_id: Optional[str] = None, name: Optional[str] = None, amount: Optional[str] = None, opportunity_stage_id: Optional[str] = None, closed_date: Optional[str] = None, is_closed: Optional[bool] = None, is_won: Optional[bool] = None, source: Optional[str] = None, account_id: Optional[str] = None) -> dict[str, Any]:
        """
        Updates an opportunity with the specified `opportunity_id` by applying partial modifications using query parameters to change attributes such as owner, name, amount, stage, and status.

        Args:
            opportunity_id (string): opportunity_id
            owner_id (string): The owner_id query parameter specifies the ID of the user to be assigned as the owner of the opportunity; if omitted, the user performing the action will be assigned as the owner.
            name (string): The "name" query parameter is a string used to update or modify the name attribute of the specified opportunity.
            amount (string): Optional amount to update for the specified opportunity, provided as a string query parameter.
            opportunity_stage_id (string): The ID of the opportunity stage to update, provided as a query parameter.
            closed_date (string): Specifies the date when the opportunity was closed, formatted as a string, and must be passed as a query parameter.
            is_closed (boolean): Specifies whether the opportunity should be marked as closed (true) or open (false) when updating the opportunity.
            is_won (boolean): Specifies whether to mark the opportunity as won (true) or not (false) in the PATCH operation.
            source (string): Specifies the source of the update for the opportunity, passed as a string query parameter.
            account_id (string): account_id is a string query parameter specifying the unique identifier of the account associated with the opportunity to be updated.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Deals    
        """
        if opportunity_id is None:
            raise ValueError("Missing required parameter 'opportunity_id'.")
        request_body_data = None
        url = f"{self.base_url}/opportunities/{opportunity_id}"
        query_params = {k: v for k, v in [('owner_id', owner_id), ('name', name), ('amount', amount), ('opportunity_stage_id', opportunity_stage_id), ('closed_date', closed_date), ('is_closed', is_closed), ('is_won', is_won), ('source', source), ('account_id', account_id)] if v is not None}
        response = self._patch(url, data=request_body_data, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def list_deal_stages(self) -> dict[str, Any]:
        """
        Retrieves a list of opportunity stages representing different phases in the sales pipeline, such as New Lead, Negotiating, and Closed.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:        
            Deals    
        """
        url = f"{self.base_url}/opportunity_stages"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def add_contacts_to_sequence(self, sequence_id: str, emailer_campaign_id: str, contact_ids_: list[str], send_email_from_email_account_id: str, sequence_no_email: Optional[bool] = None, sequence_unverified_email: Optional[bool] = None, sequence_job_change: Optional[bool] = None, sequence_active_in_other_campaigns: Optional[bool] = None, sequence_finished_in_other_campaigns: Optional[bool] = None, user_id: Optional[str] = None) -> dict[str, Any]:
        """
        Adds specified contact IDs to an emailer campaign sequence with options to control email sending behavior and filtering criteria.

        Args:
            sequence_id (string): sequence_id
            emailer_campaign_id (string): The unique identifier of the emailer campaign to which the contact IDs will be added, provided as a required string query parameter.
            contact_ids_ (array): Array of contact IDs to be added to the email campaign sequence, provided as query parameters.
            send_email_from_email_account_id (string): The ID of the email account from which the email will be sent, provided as a required query parameter.
            sequence_no_email (boolean): When set to true, the sequence_no_email parameter prevents sending emails to the added contacts in the specified sequence; defaults to false.
            sequence_unverified_email (boolean): Include this parameter as true to add contacts with unverified email addresses to the sequence; defaults to false.
            sequence_job_change (boolean): Indicates whether the addition of contact IDs should trigger a sequence job change; defaults to false.
            sequence_active_in_other_campaigns (boolean): Indicates whether the contact IDs should also be checked for active presence in other email sequences.
            sequence_finished_in_other_campaigns (boolean): Determines whether to include contacts who have already completed the sequence in other campaigns (default: false).
            user_id (string): The user ID to associate with the contact IDs being added, provided as a query string parameter.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Contacts    
        """
        if sequence_id is None:
            raise ValueError("Missing required parameter 'sequence_id'.")
        request_body_data = None
        url = f"{self.base_url}/emailer_campaigns/{sequence_id}/add_contact_ids"
        query_params = {k: v for k, v in [('emailer_campaign_id', emailer_campaign_id), ('contact_ids[]', contact_ids_), ('send_email_from_email_account_id', send_email_from_email_account_id), ('sequence_no_email', sequence_no_email), ('sequence_unverified_email', sequence_unverified_email), ('sequence_job_change', sequence_job_change), ('sequence_active_in_other_campaigns', sequence_active_in_other_campaigns), ('sequence_finished_in_other_campaigns', sequence_finished_in_other_campaigns), ('user_id', user_id)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def update_contact_status_sequence(self, emailer_campaign_ids_: list[str], contact_ids_: list[str], mode: str) -> dict[str, Any]:
        """
        Removes or stops specified contacts from one or more emailer campaigns based on the provided mode.

        Args:
            emailer_campaign_ids_ (array): **Required array of emailer campaign IDs to remove or stop contacts from.**
            contact_ids_ (array): Array of contact IDs to be removed or stopped in the emailer campaign, provided as query parameters.
            mode (string): Mode query parameter specifying the action type to remove or stop contact IDs in the emailer campaign.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Contacts    
        """
        request_body_data = None
        url = f"{self.base_url}/emailer_campaigns/remove_or_stop_contact_ids"
        query_params = {k: v for k, v in [('emailer_campaign_ids[]', emailer_campaign_ids_), ('contact_ids[]', contact_ids_), ('mode', mode)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def create_task(self, user_id: str, contact_ids_: list[str], priority: str, due_at: str, type: str, status: str, note: Optional[str] = None) -> Any:
        """
        Creates multiple tasks in bulk by specifying user ID, contact IDs, priority, due date, type, status, and an optional note in a single POST request.

        Args:
            user_id (string): Specifies the unique identifier of the user for whom the bulk tasks are being created.
            contact_ids_ (array): Array of contact IDs to associate with the tasks being created in bulk.
            priority (string): The priority query parameter specifies the urgency level for the bulk creation of tasks and is required for the POST /tasks/bulk_create operation.
            due_at (string): Due date for all tasks to be created, specified as a string in the query parameters.
            type (string): The "type" query parameter specifies the category or classification of tasks to be created in bulk and is required for the POST /tasks/bulk_create operation.
            status (string): The status query parameter specifies the current state to assign to all tasks being created in bulk.
            note (string): Optional string query parameter to add a note or comment associated with the bulk task creation request.

        Returns:
            Any: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Tasks    
        """
        request_body_data = None
        url = f"{self.base_url}/tasks/bulk_create"
        query_params = {k: v for k, v in [('user_id', user_id), ('contact_ids[]', contact_ids_), ('priority', priority), ('due_at', due_at), ('type', type), ('status', status), ('note', note)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def search_tasks(self, sort_by_field: Optional[str] = None, open_factor_names_: Optional[list[str]] = None, page: Optional[int] = None, per_page: Optional[int] = None) -> dict[str, Any]:
        """
        Searches for tasks based on specified criteria including sorting, filtering by open factor names, and supports pagination through page and per_page parameters.

        Args:
            sort_by_field (string): Specifies the field to sort the search results by for the task search operation.
            open_factor_names_ (array): Array of factor names to filter open tasks by, specified as query parameters.
            page (integer): The page query parameter specifies the page number for paginated search results in the POST /tasks/search operation.
            per_page (integer): The "per_page" query parameter specifies the maximum number of task results to return on a single page in the search response.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Tasks    
        """
        request_body_data = None
        url = f"{self.base_url}/tasks/search"
        query_params = {k: v for k, v in [('sort_by_field', sort_by_field), ('open_factor_names[]', open_factor_names_), ('page', page), ('per_page', per_page)] if v is not None}
        response = self._post(url, data=request_body_data, params=query_params, content_type='application/json')
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def get_a_list_of_users(self, page: Optional[int] = None, per_page: Optional[int] = None) -> dict[str, Any]:
        """
        Searches for users using query parameters for pagination and returns matching results if successful.

        Args:
            page (integer): Specifies the page number of paginated results for the user search operation.
            per_page (integer): The "per_page" query parameter specifies the maximum number of user records to return per page in the search results.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Users    
        """
        url = f"{self.base_url}/users/search"
        query_params = {k: v for k, v in [('page', page), ('per_page', per_page)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def get_a_list_of_email_accounts(self) -> dict[str, Any]:
        """
        Retrieves a list of email accounts accessible to the user.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Email Accounts    
        """
        url = f"{self.base_url}/email_accounts"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def get_a_list_of_all_liststags(self) -> list[Any]:
        """
        Retrieves a list of labels using the GET method, returning a successful response with a 200 status code, and handles unauthorized access with 401 and 403 status codes, along with rate limit errors indicated by a 429 status code.

        Returns:
            list[Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Labels    
        """
        url = f"{self.base_url}/labels"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def get_a_list_of_all_custom_fields(self) -> dict[str, Any]:
        """
        Retrieves a list of typed custom fields available in the system.

        Returns:
            dict[str, Any]: 200

        Raises:
            HTTPError: Raised when the API request fails (e.g., non-2XX status code).
            JSONDecodeError: Raised if the response body cannot be parsed as JSON.

        Tags:
            Typed Custom Fields    
        """
        url = f"{self.base_url}/typed_custom_fields"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        if response.status_code == 204 or not response.content or not response.text.strip():
            return None
        try:
            return response.json()
        except ValueError:
            return None

    def list_tools(self):
        return [
            self.people_enrichment,
            self.bulk_people_enrichment,
            self.organization_enrichment,
            self.bulk_organization_enrichment,
            self.people_search,
            self.organization_search,
            self.organization_jobs_postings,
            self.create_an_account,
            self.update_an_account,
            self.search_for_accounts,
            self.update_account_stage,
            self.update_account_ownership,
            self.list_account_stages,
            self.create_a_contact,
            self.update_a_contact,
            self.search_for_contacts,
            self.update_contact_stage,
            self.update_contact_ownership,
            self.list_contact_stages,
            self.create_deal,
            self.list_all_deals,
            self.update_deal,
            self.list_deal_stages,
            self.add_contacts_to_sequence,
            self.update_contact_status_sequence,
            self.create_task,
            self.search_tasks,
            self.get_a_list_of_users,
            self.get_a_list_of_email_accounts,
            self.get_a_list_of_all_liststags,
            self.get_a_list_of_all_custom_fields
        ]
