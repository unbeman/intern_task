async def test_get_company(api):
    resp = await api.get('/company/1')
    assert resp.status == 200
    text = await resp.text()


async def test_get_worker(api):
    resp = await api.get('/worker/1')
    assert resp.status == 200
    text = await resp.text()
