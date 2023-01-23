import requests


class ToDoService:
    limit = 5
    base_url = "http://localhost:8000/"

    def get_events(self, page):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f"{self.base_url}events/", params=query_params)
        response.raise_for_status()
        return response.json()

    def get_my_events(self, events_data):
        query_params = dict(limit=self.limit, offset=(events_data['page'] - 1) * self.limit, user=events_data['user'])
        response = requests.get(f"{self.base_url}events/", params=query_params)
        response.raise_for_status()
        return response.json()

    def get_event(self, event_id: int) -> None:
        response = requests.get(f"{self.base_url}events/{event_id}/")
        response.raise_for_status()
        return response.json()

    def del_event(self, event_id):
        response = requests.delete(f'{self.base_url}events/{event_id}/')
        response.raise_for_status()
        return response.raise_for_status()

    def patch_event(self, event_data):
        response = requests.patch(f'{self.base_url}events/{event_data["id"]}/', json=event_data)
        response.raise_for_status()
        return response.json()

    def get_users(self, page):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f'{self.base_url}users/', params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user(self, users_id: int) -> None:
        response = requests.get(f"{self.base_url}users/{users_id}/")
        response.raise_for_status()
        return response.json()

    def get_wish(self, wish_id: int) -> None:
        response = requests.get(f'{self.base_url}questions/{wish_id}/')
        response.raise_for_status()
        return response.json()

    def get_questions(self, page):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f'{self.base_url}questions/', params=query_params)
        response.raise_for_status()
        return response.json()

    def get_groups(self, page):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f'{self.base_url}groups/', params=query_params)
        response.raise_for_status()
        return response.json()

    def get_group(self, group_id: int):
        response = requests.get(f'{self.base_url}groups/{group_id}/')
        response.raise_for_status()
        return response.json()


todo_service = ToDoService()
