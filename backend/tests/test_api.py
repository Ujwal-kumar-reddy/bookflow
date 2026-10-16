from datetime import date, timedelta
from fastapi.testclient import TestClient

def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}

def test_ready(client: TestClient):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "READY"}

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "BookFlow API"
    assert "version" in payload
    assert payload["docs"] == "/docs"

def test_metrics(client: TestClient):
    # Trigger a request so instrumentator records an entry
    client.get("/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text or "http_request_duration_seconds" in response.text

def test_metrics_contains_http_requests_total(client: TestClient):
    client.get("/")
    client.get("/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text

def test_create_book_success(client: TestClient):
    book_data = {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "category": "Computer Science",
    }
    response = client.post("/api/books", json=book_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["title"] == "Designing Data-Intensive Applications"
    assert data["author"] == "Martin Kleppmann"
    assert data["category"] == "Computer Science"
    assert data["status"] == "AVAILABLE"
    assert data["borrower_name"] is None
    assert data["due_date"] is None

def test_create_book_validation_error(client: TestClient):
    # Missing required 'author' and empty title
    response = client.post("/api/books", json={"title": "", "category": "Fiction"})
    assert response.status_code == 422

def test_list_books_and_filters(client: TestClient):
    # Create two books
    client.post(
        "/api/books",
        json={"title": "Clean Architecture", "author": "Robert C. Martin", "category": "Software"},
    )
    client.post(
        "/api/books",
        json={"title": "Introduction to Algorithms", "author": "CLRS", "category": "Algorithms"},
    )

    # List all
    all_books = client.get("/api/books").json()
    assert len(all_books) >= 2

    # Filter by category
    filtered = client.get("/api/books?category=Algorithms").json()
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Introduction to Algorithms"

    # Search by title
    search_res = client.get("/api/books?search=Clean").json()
    assert len(search_res) == 1
    assert search_res[0]["author"] == "Robert C. Martin"

def test_get_book_and_not_found(client: TestClient):
    create_res = client.post(
        "/api/books",
        json={"title": "Kubernetes in Action", "author": "Marko Luksa", "category": "DevOps"},
    )
    book_id = create_res.json()["id"]

    # Found
    get_res = client.get(f"/api/books/{book_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Kubernetes in Action"

    # Not found
    not_found = client.get("/api/books/99999")
    assert not_found.status_code == 404

def test_update_book(client: TestClient):
    create_res = client.post(
        "/api/books",
        json={"title": "The Phoenix Project", "author": "Gene Kim", "category": "DevOps"},
    )
    book_id = create_res.json()["id"]

    update_res = client.put(
        f"/api/books/{book_id}",
        json={"title": "The Phoenix Project: 10th Anniversary", "category": "Management"},
    )
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["title"] == "The Phoenix Project: 10th Anniversary"
    assert updated["author"] == "Gene Kim"
    assert updated["category"] == "Management"

def test_checkout_book_success(client: TestClient):
    create_res = client.post(
        "/api/books",
        json={"title": "Site Reliability Engineering", "author": "Betsy Beyer", "category": "DevOps"},
    )
    book_id = create_res.json()["id"]

    checkout_res = client.post(
        f"/api/books/{book_id}/checkout",
        json={"borrower_name": "Aarav Sharma", "loan_days": 14},
    )
    assert checkout_res.status_code == 200
    data = checkout_res.json()
    assert data["status"] == "BORROWED"
    assert data["borrower_name"] == "Aarav Sharma"
    assert data["due_date"] == str(date.today() + timedelta(days=14))

def test_checkout_already_borrowed_fails(client: TestClient):
    create_res = client.post(
        "/api/books",
        json={"title": "The DevOps Handbook", "author": "Gene Kim", "category": "DevOps"},
    )
    book_id = create_res.json()["id"]

    # First checkout succeeds
    client.post(
        f"/api/books/{book_id}/checkout",
        json={"borrower_name": "Student A", "loan_days": 7},
    )

    # Second checkout fails with 400 Bad Request
    second_res = client.post(
        f"/api/books/{book_id}/checkout",
        json={"borrower_name": "Student B", "loan_days": 7},
    )
    assert second_res.status_code == 400
    assert "already checked out" in second_res.json()["detail"]

def test_return_book_success(client: TestClient):
    create_res = client.post(
        "/api/books",
        json={"title": "Terraform: Up & Running", "author": "Yevgeniy Brikman", "category": "Cloud"},
    )
    book_id = create_res.json()["id"]

    client.post(
        f"/api/books/{book_id}/checkout",
        json={"borrower_name": "Priya Patel", "loan_days": 10},
    )

    # Return book
    return_res = client.post(f"/api/books/{book_id}/return")
    assert return_res.status_code == 200
    data = return_res.json()
    assert data["status"] == "AVAILABLE"
    assert data["borrower_name"] is None
    assert data["due_date"] is None

def test_return_available_book_fails(client: TestClient):
    create_res = client.post(
        "/api/books",
        json={"title": "Clean Code", "author": "Robert C. Martin", "category": "Software"},
    )
    book_id = create_res.json()["id"]

    # Attempting to return an already available book
    return_res = client.post(f"/api/books/{book_id}/return")
    assert return_res.status_code == 400
    assert "already available" in return_res.json()["detail"]

def test_delete_book(client: TestClient):
    create_res = client.post(
        "/api/books",
        json={"title": "Legacy Systems", "author": "Old Author", "category": "Archive"},
    )
    book_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/books/{book_id}")
    assert delete_res.status_code == 200

    # Verify book is gone
    get_res = client.get(f"/api/books/{book_id}")
    assert get_res.status_code == 404

def test_book_stats(client: TestClient):
    # Clean state
    stats_empty = client.get("/api/books/stats").json()
    assert stats_empty["total"] == 0
    assert stats_empty["available"] == 0
    assert stats_empty["borrowed"] == 0
    assert stats_empty["overdue"] == 0

    # Add available book
    client.post(
        "/api/books",
        json={"title": "Book 1", "author": "Author 1", "category": "Cat A"},
    )
    # Add book and check it out
    res2 = client.post(
        "/api/books",
        json={"title": "Book 2", "author": "Author 2", "category": "Cat B"},
    )
    client.post(
        f"/api/books/{res2.json()['id']}/checkout",
        json={"borrower_name": "Student", "loan_days": 14},
    )

    stats = client.get("/api/books/stats").json()
    assert stats["total"] == 2
    assert stats["available"] == 1
    assert stats["borrowed"] == 1
    assert stats["overdue"] == 0
