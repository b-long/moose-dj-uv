import pytest 

from django.test import Client
from django.urls import reverse
import time

from moose_dj.news.views import NUM_FAKE_TASKS

@pytest.mark.django_db
@pytest.mark.skip(reason="Focused on Celery")
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
    r2_status = response2.json()["status"]
    assert r2_status == "running"

    time.sleep(NUM_FAKE_TASKS + 5)

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        try:
            response3 = client.get(reverse("get_task_status", kwargs={"task_id": task_id}))
            assert response3.status_code == 200

            r3_status = response3.json()["status"]
            r3_progress = response3.json()["progress"]

            assert r3_progress >= 1
            assert r3_status == "completed"
            break  # Exit the loop if successful
        except Exception:
            attempts += 1
            if attempts == max_attempts:
                raise  # Raise the last exception if all attempts failed



@pytest.mark.skip(reason="Focused on Celery")
@pytest.mark.django_db
def test_immediate_response_with_huey(huey_worker_fixture):
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
    r2_status = response2.json()["status"]
    assert r2_status == "running"

    time.sleep(NUM_FAKE_TASKS + 5)

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        try:
            response3 = client.get(reverse("get_task_status", kwargs={"task_id": task_id}))
            assert response3.status_code == 200

            r3_status = response3.json()["status"]
            r3_progress = response3.json()["progress"]

            assert r3_progress >= 1
            assert r3_status == "completed"
            break  # Exit the loop if successful
        except Exception:
            attempts += 1
            if attempts == max_attempts:
                raise  # Raise the last exception if all attempts failed




def test_immediate_response_with_celery(celery_worker_fixture):
    # from django.test import override_settings, modify_settings
    # with override_settings():
    # with modify_settings(
    # with override_settings(
    #     CELERY_TASK_ALWAYS_EAGER=True, 
    #     # CELERY_ALWAYS_EAGER = False
    # ): 

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
    r2_status = response2.json()["status"]
    assert r2_status == "running"

    time.sleep(NUM_FAKE_TASKS)

    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        time.sleep(2)
        try:
            response3 = client.get(reverse("get_task_status", kwargs={"task_id": task_id}))
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