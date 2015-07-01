import pytest

@pytest.mark.django_db

class TestPrograms:

    def test_list_view(self, client):
        response = client.get('timesheet', follow=True)
        print response.content
        assert response.status_code == 200
