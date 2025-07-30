# ApolloApp MCP Server

An MCP Server for the ApolloApp API.

## 🛠️ Tool List

This is automatically generated from OpenAPI schema for the ApolloApp API.


| Tool | Description |
|------|-------------|
| `people_enrichment` | Matches a person’s profile based on provided identifiers such as name, email, organization, or LinkedIn URL, with options to reveal personal emails and phone numbers. |
| `bulk_people_enrichment` | Performs a bulk matching operation for people records using posted data, with options to reveal personal emails or phone numbers and specify a webhook URL for result delivery. |
| `organization_enrichment` | Retrieves enriched organizational data such as industry, revenue, employee count, funding details, and contact information based on a provided domain. |
| `bulk_organization_enrichment` | Enriches multiple organization profiles by accepting a list of domains and returns detailed data for each, allowing for efficient bulk processing. |
| `people_search` | Searches for people by specified criteria such as titles, locations, seniorities, organization details, and additional filters, returning paginated results via a POST request. |
| `organization_search` | Searches for mixed companies based on various filters such as employee ranges, locations, revenue, technologies used, keywords, and pagination parameters. |
| `organization_jobs_postings` | Retrieves a paginated list of job postings for the specified organization by organization_id. |
| `create_an_account` | Creates a new account resource using provided query parameters such as name, domain, owner ID, account stage ID, phone, and raw address. |
| `update_an_account` | Updates the account identified by {account_id} with new provided values or replaces its details if required, supporting various account attributes as query parameters[1][2][5]. |
| `search_for_accounts` | Searches for accounts using the specified organization name, account stages, and sorting preferences, returning a paginated list of results. |
| `update_account_stage` | Updates multiple accounts in bulk using the provided account IDs and stage ID. |
| `update_account_ownership` | Updates the owners of multiple accounts by specifying the account IDs and the new owner ID via a POST request. |
| `list_account_stages` | Retrieves a list of account stages available in the system. |
| `create_a_contact` | Creates a new contact record with provided details such as name, organization, title, email, account ID, phone numbers, address, and labels, returning a success or error response. |
| `update_a_contact` | Updates an existing contact identified by contact_id with provided details such as name, organization, email, phone numbers, and labels. |
| `search_for_contacts` | Searches contacts based on keywords, contact stage IDs, and other query parameters, returning a paginated and sortable list of matching contacts. |
| `update_contact_stage` | Updates the stages of specified contacts using their IDs and a target stage ID. |
| `update_contact_ownership` | Updates the owners of multiple contacts by assigning a specified owner ID to the given list of contact IDs. |
| `list_contact_stages` | Retrieves a list of available contact stages from the system. |
| `create_deal` | Creates a new opportunity with the specified parameters such as name, owner ID, account ID, amount, opportunity stage ID, and closed date. |
| `list_all_deals` | Searches for opportunities with optional sorting and pagination parameters and returns the matching results. |
| `update_deal` | Updates an opportunity with the specified `opportunity_id` by applying partial modifications using query parameters to change attributes such as owner, name, amount, stage, and status. |
| `list_deal_stages` | Retrieves a list of opportunity stages representing different phases in the sales pipeline, such as New Lead, Negotiating, and Closed. |
| `add_contacts_to_sequence` | Adds specified contact IDs to an emailer campaign sequence with options to control email sending behavior and filtering criteria. |
| `update_contact_status_sequence` | Removes or stops specified contacts from one or more emailer campaigns based on the provided mode. |
| `create_task` | Creates multiple tasks in bulk by specifying user ID, contact IDs, priority, due date, type, status, and an optional note in a single POST request. |
| `search_tasks` | Searches for tasks based on specified criteria including sorting, filtering by open factor names, and supports pagination through page and per_page parameters. |
| `get_a_list_of_users` | Searches for users using query parameters for pagination and returns matching results if successful. |
| `get_a_list_of_email_accounts` | Retrieves a list of email accounts accessible to the user. |
| `get_a_list_of_all_liststags` | Retrieves a list of labels using the GET method, returning a successful response with a 200 status code, and handles unauthorized access with 401 and 403 status codes, along with rate limit errors indicated by a 429 status code. |
| `get_a_list_of_all_custom_fields` | Retrieves a list of typed custom fields available in the system. |
