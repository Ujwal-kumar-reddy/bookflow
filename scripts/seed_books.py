import urllib.request
import json

def post(url, data):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

b1 = post('http://localhost:8000/api/books', {
    'title': 'Designing Data-Intensive Applications',
    'author': 'Martin Kleppmann',
    'category': 'Software Architecture'
})
print(f"Added book: {b1['id']} - {b1['title']}")

b2 = post('http://localhost:8000/api/books', {
    'title': 'The DevOps Handbook',
    'author': 'Gene Kim, Jez Humble, Patrick Debois',
    'category': 'DevOps & Cloud'
})
print(f"Added book: {b2['id']} - {b2['title']}")

b3 = post('http://localhost:8000/api/books', {
    'title': 'Introduction to Algorithms (CLRS)',
    'author': 'Thomas H. Cormen et al.',
    'category': 'Algorithms & Data Structures'
})
print(f"Added book: {b3['id']} - {b3['title']}")

# Checkout b2
post(f"http://localhost:8000/api/books/{b2['id']}/checkout", {
    'borrower_name': 'Aarav Sharma (STU-2026-042)',
    'loan_days': 14
})
print(f"Loaned '{b2['title']}' to Aarav Sharma.")
