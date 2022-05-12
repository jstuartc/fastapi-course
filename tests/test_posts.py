import pytest
from app import schemas
from tests.conftest import authorised_client

def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, res.json())
    posts_list = list(post_map)

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

def test_unauthorised_user_get_all(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorised_user_get_one(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorised_client, test_posts):
    res = authorised_client.get("/posts/10099342")
    assert res.status_code == 404

def test_get_one_post(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content  # Can do more if I really want to 


@pytest.mark.parametrize("title, content, published",[
    ("awesome new title","rubbish content",True), ("Pizza","I like margarita", False)
])
def test_create_post(authorised_client,test_user, test_posts, title, content, published):
    res = authorised_client.post("/posts/", json= {"title":title,"content":content,"published": published})

    created = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created.title == title
    assert created.content == content
    assert created.published == published
    assert created.owner_id == test_user['id']

def test_create_post_default_published(authorised_client,test_user):
    res = authorised_client.post("/posts/", json= {"title":"Hello","content":"No published section"})
    created = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created.title == "Hello"
    assert created.published == True
    assert created.owner_id == test_user['id']

def test_unauthorised_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json= {"title":"Hello","content":"No published section"})
    assert res.status_code == 401

def test_unauthorised_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204  # Could also count posts

def test_delete_post_non_exist(authorised_client, test_user, test_posts):
    res = authorised_client.delete("/posts/2323523532")
    assert res.status_code == 404

def test_delete_other_user_post(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorised_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    
    res = authorised_client.put(f"/posts/{test_posts[0].id}", json = data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_update_other_user_post(authorised_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    res = authorised_client.put(f"/posts/{test_posts[3].id}", json = data)
    assert res.status_code == 403

def test_unauthorised_user_update_post(client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    res = client.put(f"/posts/{test_posts[0].id}", json = data)
    assert res.status_code == 401

def test_update_post_non_exist(authorised_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    res = authorised_client.put("/posts/2323523532", json  = data)
    assert res.status_code == 404