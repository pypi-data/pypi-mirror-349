from aircheckdata import DataLoader


def test_load_dataset():
    """
    Test the load_dataset function with a sample dataset.
    """
    loader = DataLoader()
    print("loader", loader)
    exit()
    df = loader.load_dataset(
        dataset_name="sample_dataset",
        columns=["column1", "column2"],
        show_progress=True
    )
    assert df is not None, "Failed to load dataset"
    assert "column1" in df.columns, "Column 'column1' not found in dataset"
    assert "column2" in df.columns, "Column 'column2' not found in dataset"


if __name__ == "__main__":
    test_load_dataset()
