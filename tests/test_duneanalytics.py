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
        dune.fetch_auth_token()
        assert dune.auth_refresh is not None
        assert dune.username is not None
        assert dune.password is not None
        assert dune.token is not None

    @pytest.mark.skip(reason='To be implemented')
    def test_query_result_id(self, dune):
        assert False

    @pytest.mark.skip(reason='To be implemented')
    def test_query_result(self, dune):
        assert False
