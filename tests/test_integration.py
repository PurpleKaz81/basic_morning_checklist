def test_homepage_renders(client):
    resp = client.get('/')
    assert resp.status_code == 200
    text = resp.get_data(as_text=True)
    # looks for wake-time input and one of the checklist headings
    assert 'id="wake-time"' in text or 'name="wake-time"' in text
    assert 'Morning Checklist' in text or 'checklist' in text.lower()
