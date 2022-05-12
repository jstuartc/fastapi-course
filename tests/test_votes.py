import pytest
from app import models

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Votes(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorised_client, test_posts):
    res = authorised_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": True})
    assert res.status_code == 201

def test_vote_twice_post(authorised_client, test_posts, test_vote):
    res = authorised_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": True})
    assert res.status_code == 409

def test_delete_vote(authorised_client, test_posts, test_vote):
    res = authorised_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": False})
    assert res.status_code == 201

def test_delete_non_existant_vote(authorised_client, test_posts):
    res = authorised_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": False})
    assert res.status_code == 404

def test_vote_post_non_exist(authorised_client, test_posts):
    res = authorised_client.post("/vote/", json={"post_id": 100000, "dir": True})
    assert res.status_code == 404

def test_vote_unauthorised(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": True})
    assert res.status_code == 401