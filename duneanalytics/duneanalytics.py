# -*- coding: utf-8 -*- #
"""This provides the DuneAnalytics class implementation"""

from requests import Session

# --------- Constants --------- #

BASE_URL = "https://dune.xyz"
GRAPH_URL = 'https://core-hsr.duneanalytics.com/v1/graphql'

# --------- Constants --------- #

class DuneAnalyticsException(Exception):
    """Exception raised for errors during communication with Dune Analytics.

    Attributes:
        response -- response object received the last time before exception occurs
        message -- explanation of the error
    """
    def __init__(self, message="", response=None):
        self.response = response
        self.message = message
        super().__init__(self.message)


class DuneAnalytics:
    """
    DuneAnalytics class to act as python client for duneanalytics.com.
    All requests to be made through this class.
    """

    def __init__(self, username, password, raise_exception=False):
        """
        Initialize the object
        :param username: username for duneanalytics.com
        :param password: password for duneanalytics.com
        """
        self.csrf = None
        self.auth_refresh = None
        self.token = None
        self.username = username
        self.password = password
        self.raise_exception = raise_exception
        self.session = Session()
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,'
                      'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'dnt': '1',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'origin': BASE_URL,
            'upgrade-insecure-requests': '1'
        }
        self.session.headers.update(headers)

    def _should_raise_exception(self, override_raise_exception):
        return (override_raise_exception is True or (override_raise_exception is None and self.raise_exception))

    def _try_raise_exception(raise_exception, description):
        if (raise_exception is True or (raise_exception is None and self.raise_exception)):
            raise Exception(description)

    def login(self, raise_exception=None):
        """
        Try to login to duneanalytics.com & get the token
        :return:
        """
        login_url = BASE_URL + '/auth/login'
        csrf_url = BASE_URL + '/api/auth/csrf'
        auth_url = BASE_URL + '/api/auth'

        # fetch login page
        self.session.get(login_url)

        # get csrf token
        self.session.post(csrf_url)
        self.csrf = self.session.cookies.get('csrf')

        if (not self.csrf and self._should_raise_exception(raise_exception)):
            raise DuneAnalyticsException("Could not fetch CSRF token!", None)

        # try to login
        form_data = {
            'action': 'login',
            'username': self.username,
            'password': self.password,
            'csrf': self.csrf,
            'next': BASE_URL
        }

        self.session.post(auth_url, data=form_data)
        self.auth_refresh = self.session.cookies.get('auth-refresh')

    def fetch_auth_token(self, raise_exception=None):
        """
        Fetch authorization token for the user
        :return:
        """
        session_url = BASE_URL + '/api/auth/session'

        response = self.session.post(session_url)
        if response.status_code == 200:
            self.token = response.json().get('token')
        else:
            if (self._should_raise_exception(raise_exception)):
                raise DuneAnalyticsException("Could not get auth token!", response=response)
            print(response.text)

    def query_result_id(self, query_id, raise_exception=None):
        """
        Fetch the query result id for a query

        :param query_id: provide the query_id
        :return:
        """
        query_data = {"operationName": "GetResult", "variables": {"query_id": query_id},
                      "query": "query GetResult($query_id: Int!, $parameters: [Parameter!]) "
                               "{\n  get_result(query_id: $query_id, parameters: $parameters) "
                               "{\n    job_id\n    result_id\n    __typename\n  }\n}\n"
                      }

        self.session.headers.update({'authorization': f'Bearer {self.token}'})

        response = self.session.post(GRAPH_URL, json=query_data)
        if response.status_code == 200:
            data = response.json()
            # print(data)
            if 'errors' in data:
                if(self._should_raise_exception(raise_exception)):
                    raise DuneAnalyticsException("Could not get query result id!", response=response)
                return None
            result_id = data.get('data').get('get_result').get('result_id')
            return result_id
        else:
            if (self._should_raise_exception(raise_exception)):
                raise DuneAnalyticsException("Could not get query result id!", response=response)
            print(response.text)
            return None

    def query_result(self, result_id, raise_exception=None):
        """
        Fetch the result for a query
        :param result_id: result id of the query
        :return:
        """
        query_data = {"operationName": "FindResultDataByResult",
                      "variables": {"result_id": result_id},
                      "query": "query FindResultDataByResult($result_id: uuid!) "
                               "{\n  query_results(where: {id: {_eq: $result_id}}) "
                               "{\n    id\n    job_id\n    error\n    runtime\n    generated_at\n    columns\n    __typename\n  }"
                               "\n  get_result_by_result_id(args: {want_result_id: $result_id}) {\n    data\n    __typename\n  }\n}\n"
                      }

        self.session.headers.update({'authorization': f'Bearer {self.token}'})

        response = self.session.post(GRAPH_URL, json=query_data)
        if response.status_code == 200:
            data = response.json()
            # print(data)
            return data
        else:
            if (self._should_raise_exception(raise_exception)):
                raise DuneAnalyticsException("Could not get query result data!", response=response)
            print(response.text)
            return {}
