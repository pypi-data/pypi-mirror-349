import pytest
from unittest.mock import patch, MagicMock, mock_open
from aircheckdata import DataLoader


def test_get_dataset_columns():
    loader = DataLoader(dataset_name="WDR91")
    columns = loader.get_dataset_columns("WDR91")
    assert isinstance(columns, dict)
    assert "ECFP4" in columns
    assert "LABEL" in columns


def test_get_dataset_columns_invalid():
    loader = DataLoader(dataset_name="WDR91")
    with pytest.raises(ValueError):
        loader.get_dataset_columns("nonexistent_dataset")


@patch("aircheckdata.main.pq.read_table")
@patch("aircheckdata.main.gcsfs.GCSFileSystem")
def test_load_dataset_with_mocked_gcs(mock_gcsfs, mock_read_table):
    # Mock GCS file system and parquet loading
    mock_fs = MagicMock()
    mock_gcsfs.return_value = mock_fs
    mock_fs.info.return_value = {'size': 1024}
    mock_file = MagicMock()
    mock_file.read.side_effect = [b'data', b'']
    mock_fs.open.return_value.__enter__.return_value = mock_file

    mock_table = MagicMock()
    mock_df = MagicMock()
    mock_table.to_pandas.return_value = mock_df
    mock_read_table.return_value = mock_table

    loader = DataLoader(dataset_name="WDR91", columns=["ECFP4"])
    df = loader.load_dataset(dataset_name="WDR91", columns=["ECFP4"])
    assert df is not None
    mock_read_table.assert_called_once()
