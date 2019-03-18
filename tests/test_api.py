from aiohttp import FormData


async def test_index(api):
    resp = await api.get('/')

    assert resp.status == 200
    assert 'Imagetagger' in await resp.text()


async def test_predict(api):
    with open('tests/data/hotdog.jpg', 'rb') as f:
        img = f.read()
    data = FormData()
    data.add_field(
        'file', img, filename='aircraft.jpg', content_type='image/img')

    resp = await api.post('/predict', data=data)
    assert resp.status == 200, resp
    data = await resp.json()
    assert data['success']
    assert data['predictions'][0]['label']


async def test_get_company(api):
    resp = await api.get('/company/1')
    assert resp.status == 200
    text = await resp.text()


async def test_get_worker(api):
    resp = await api.get('/worker/1')
    assert resp.status == 200
    text = await resp.text()
