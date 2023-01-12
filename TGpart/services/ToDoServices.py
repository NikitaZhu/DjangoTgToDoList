import requests


class ToDoService:
    limit = 5
    base_url = "http://localhost:8000/"

    def get_events(self, page):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f"{self.base_url}events/", params=query_params)
        response.raise_for_status()
        return response.json()

    def get_event(self, event_id: int) -> None:
        response = requests.get(f"{self.base_url}events/{event_id}/")
        response.raise_for_status()
        return response.json()


todo_service = ToDoService()