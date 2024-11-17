from django.test import Client
from django.urls import reverse
import time


def test_immediate_response_with_dask():
    client = Client()
    response = client.post(reverse("start_task_dask"), data={"data": "foo"})
    assert response.status_code == 200
    assert "task_id" in response.json()

    task_id = response.json()["task_id"]
    response2 = client.get(reverse("get_task_status_dask", kwargs={"task_id": task_id}))
    assert response2.status_code == 200
    r2_status = response2.json()["status"]
    assert r2_status == "running"

    attempts = 0
    max_attempts = 8

    while attempts < max_attempts:
        time.sleep(1)
        try:
            response3 = client.get(
                reverse("get_task_status_dask", kwargs={"task_id": task_id})
            )
            assert response3.status_code == 200

            r3_status = response3.json()["status"]
            r3_progress = response3.json()["progress"]

            assert r3_progress >= 99
            assert r3_status == "completed"
            break  # Exit the loop if successful
        except Exception:
            attempts += 1
            if attempts == max_attempts:
                raise  # Raise the last exception if all attempts failed
