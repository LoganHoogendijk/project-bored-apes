import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Logan Hoogendijk's Portfolio</title>" in html
        assert '<p class="title is-4"> Logan Hoogendijk </p>' in html
        assert '<h1 class="title is-1 is-uppercase has-text-white ">Experience</h1>' in html
        assert '<h1 class="title is-1 is-uppercase has-text-white">Education</h1>' in html
        assert '<h1 class="title is-1 is-uppercase has-text-white">Projects</h1>' in html
        assert '<h1 class="title is-1 has-text-white is-uppercase">Trivia Board</h1>' in html
        assert '<h1 class="title is-1 is-uppercase has-text-white">Hobbies</h1>' in html

    def test_timeline_api(self):
        # empty get
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # post
        response = self.client.post("/api/timeline_post", data={
            "name": "test",
            "email": "test@test.com",
            "content": "this is a test"
        })
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "test" in json['content']
        
        # get with one item in db
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1
        
        # delete
        delete_id = json['timeline_posts'][0]['id']
        response = self.client.delete(f"/api/timeline_post/{delete_id}")
        assert response.status_code == 200
        response_text = response.get_data(as_text=True)
        assert "Deleted" in response_text and str(delete_id) in response_text
        # check that post was actually deleted
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        
    def test_bad_timeline_post(self):
        # POST request missing name
        response = self.client.post("api/timeline_post", data={
            "email": "john@example.com",
            "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": ""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with bad email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "not-an-email",
            "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html