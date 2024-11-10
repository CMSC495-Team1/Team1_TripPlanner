from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):
    @task
    def load_locations(self):
        self.client.get("/locations")

    @task
    def load_hotels(self):
        self.client.get("/hotels")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    host = "http://localhost:5000"  # Adjust this to your API host
    min_wait = 5000
    max_wait = 9000