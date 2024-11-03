from django.test import Client
from django.urls import reverse
import time

from moose_dj.news.views import NUM_FAKE_TASKS

def test_immediate_response():
    reverse("start_task")

    client = Client()
    response = client.post(reverse('start_task'), data={
        "data": "foo"
    })
    assert response.status_code == 200
    assert "task_id" in response.json()

    task_id = response.json()["task_id"]
    response2 = client.get(reverse("get_task_status", kwargs={ "task_id": task_id }))
    assert response2.status_code == 200
    assert response2.json()["status"] == "running"

    time.sleep(NUM_FAKE_TASKS + 1)

    response3 = client.get(reverse("get_task_status", kwargs={ "task_id": task_id }))
    assert response3.status_code == 200
    assert response3.json()["status"] == "completed"
