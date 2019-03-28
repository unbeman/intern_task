async def test_get_company(tables_and_data, api):
    expected_data = {"title": "Plushki", "description": "Bread and cakes", "id": 1}
    response = await api.get('/company/1')
    assert response.status == 200
    data = await response.json()
    assert data == expected_data


async def test_get_nonexistent_company(tables_and_data, api):
    response = await api.get('/company/2')
    assert response.status == 404


async def test_get_worker(tables_and_data, api):
    expected_data = {"full_name": "Vasya Pupkin", "position": "seller",
                     "phone_number": "89998765432",
                     "company_id": 1, "id": 1}
    response = await api.get('/worker/1')
    assert response.status == 200
    data = await response.json()
    assert data == expected_data
