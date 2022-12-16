import pytest


@pytest.mark.usefixtures('dune')
class TestDuneAnalytics:
    """
    Class to test DuneAnalytics
    """
    def test_login(self, dune):
        # try to login
        dune.login()
        assert dune.auth_refresh is not None
        assert dune.username is not None
        assert dune.password is not None
        assert dune.token is None

    def test_fetch_auth_token(self, dune):
        # fetch authentication token
        # dune.login()
        dune.fetch_auth_token()
        assert dune.auth_refresh is not None
        assert dune.username is not None
        assert dune.password is not None
        assert dune.token is not None

    # @pytest.mark.skip(reason='To be implemented')
    def test_query_result_id(self, dune):
        result_id = dune.query_result_id(query_id=3751)
        assert result_id is not None

    # @pytest.mark.skip(reason='To be implemented')
    def test_query_result(self, dune):
        result_id = dune.query_result_id(query_id=3705)
        assert result_id is not None
        data = dune.query_result(result_id)
        assert data is not None

    def test_get_execution_result(self, dune):
        result_id = dune.query_result_id_v3(query_id=1105079)
        assert result_id is not None
        data = dune.get_execution_result(result_id)
        assert data is not None
        assert data.get('get_execution') is not None
        assert data.get('get_execution', {}).get('execution_succeeded') is not None
