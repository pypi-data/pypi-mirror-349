import pytest


@pytest.mark.asyncio
async def test_acquisition_list(mock_client):
    mock_client.acquisition.list.return_value = [{"acquisition_id": "ACQ001"}]
    result = await mock_client.acquisition.list()
    assert result == [{"acquisition_id": "ACQ001"}]
    mock_client.acquisition.list.assert_called_once()


@pytest.mark.asyncio
async def test_acquisition_create(mock_client):
    acquisition_data = {"acquisition_id": "ACQ002", "roi_id": "ROI001"}
    mock_client.acquisition.create.return_value = acquisition_data
    result = await mock_client.acquisition.create(acquisition_data)
    assert result == acquisition_data
    mock_client.acquisition.create.assert_called_once_with(acquisition_data)


@pytest.mark.asyncio
async def test_acquisition_get(mock_client):
    acquisition_data = {"acquisition_id": "ACQ002", "roi_id": "ROI001"}

    mock_client.acquisition.get.return_value = acquisition_data
    result = await mock_client.acquisition.get("ACQ002")
    assert result == acquisition_data
    mock_client.acquisition.get.assert_called_once_with("ACQ002")


@pytest.mark.asyncio
async def test_acquisition_update(mock_client):
    acquisition_data = {"acquisition_id": "ACQ002", "roi_id": "ROI001"}

    update_data = {"status": "COMPLETED"}
    mock_client.acquisition.update.return_value = {**acquisition_data, **update_data}
    result = await mock_client.acquisition.update("ACQ002", update_data)
    assert result == {**acquisition_data, **update_data}
    mock_client.acquisition.update.assert_called_once_with("ACQ002", update_data)


@pytest.mark.asyncio
async def test_acquisition_delete(mock_client):
    await mock_client.acquisition.delete("ACQ002")
    mock_client.acquisition.delete.assert_called_once_with("ACQ002")
