import pyarrow.parquet as pq
import io
import gcsfs
from tqdm import tqdm
import pandas as pd
import logging
from typing import Optional, List, Dict
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DATASETS = {
#     "default": "gs://aircheck-workshop-readonly/TrainDataset_Aircheck.parquet",
#     "wdr12": "gs://bucket/wdr12.parquet",
# }

DATASETS = {
    "default": {
        "bucket": "aircheck-workshop-readonly",
        "path": "gs://aircheck-workshop-readonly/TrainDataset_Aircheck.parquet",
        "description": "WRD91 datasets",
        "columns": {
            "ECFP6": "Unique transaction identifier",
            "ECFP4": "Customer identifier",
            "FCFP6": "Product identifier",
            "FCFP4": "Store identifier",
            "DELLabel": "Transaction date",
            "DEL_ID": "Number of units sold",
        }
    },
    "wdr12": {
        "bucket": "aircheck-workshop-readonly",
        "path": "TrainDataset_Aircheck.parquet",
        "description": "WDR12 datasets",
        "columns": {
            "ECFP6": "Unique transaction identifier",
            "ECFP4": "Customer identifier",
            "FCFP6": "Product identifier",
            "FCFP4": "Store identifier",
            "DELLabel": "Transaction date",
            "DEL_ID": "Number of units sold",
        }
    }
}


class DataLoader:
    def __init__(self, dataset_name: str, columns: Optional[List[str]] = None,
                 show_progress: bool = False):
        """
        Initializes the DataLoader with GCS URL and optional parameters.

        Parameters:
            gcs_url (str): GCS path to the Parquet file (e.g., 'gs://bucket/file.parquet').
            columns (Optional[List[str]]): List of columns to load from the Parquet file.
            show_progress (bool): Whether to show a progress bar during loading.
        """
        self.dataset_name = dataset_name
        self.columns = columns
        self.show_progress = show_progress
        self.datasets = DATASETS

    def get_dataset_columns(self, dataset_name: str) -> Dict[str, str]:
        """
        Get information about available columns in a dataset.

        Args:
            dataset_name: Name of the pre-configured dataset

        Returns:
            Dictionary mapping column names to their descriptions
        """
        if dataset_name not in self.datasets:
            available = ", ".join(self.datasets.keys())
            raise ValueError(
                f"Dataset '{dataset_name}' not found. Available datasets: {available}")

        return self.datasets[dataset_name]["columns"]

    def list_available_datasets(self) -> Dict[str, str]:
        """
        List all available pre-configured datasets.

        Returns:
            Dictionary mapping dataset names to their descriptions
        """
        return {name: config["description"] for name, config in self.datasets.items()}

    def load_dataset(self,
                     dataset_name: str,
                     columns: Optional[List[str]] = None,
                     show_progress: bool = True,
                     ) -> Optional[pd.DataFrame]:
        """
        Reads a Parquet file from a public GCS bucket with a progress bar.

        Parameters:
            gcs_url (str): GCS path to the Parquet file (e.g., 'gs://bucket/file.parquet').

        Returns:
            Optional[pd.DataFrame]: Loaded DataFrame or None on failure.
        """
        try:
            logger.info("Connecting to GCS and reading file metadata...")
            if dataset_name not in self.datasets:
                available = ", ".join(self.datasets.keys())
                raise ValueError(
                    f"Dataset '{dataset_name}' not found. Available datasets: {available}")

            dataset_config = self.datasets[dataset_name]
            if columns:
                available_columns = set(dataset_config["columns"].keys())
                requested_columns = set(columns)
                invalid_columns = requested_columns - available_columns
                if invalid_columns:
                    raise ValueError(
                        f"Invalid columns: {', '.join(invalid_columns)}. "
                        f"Available columns: {', '.join(available_columns)}"
                    )

            fs = gcsfs.GCSFileSystem(token='anon')
            file_info = fs.info(dataset_config["path"])
            gcs_url = dataset_config["path"]
            file_size = file_info['size']

            logger.info("File size: %.2f MB", file_size / (1024 * 1024))
            if show_progress:
                with fs.open(gcs_url, 'rb') as remote_file:
                    buffer = io.BytesIO()
                    chunk_size = 1024 * 1024  # 1 MB

                    with tqdm(total=file_size, unit='B', unit_scale=True, desc="Downloading") as pbar:
                        while True:
                            chunk = remote_file.read(chunk_size)
                            if not chunk:
                                break
                            buffer.write(chunk)
                            pbar.update(len(chunk))

                    buffer.seek(0)  # Reset to beginning
                    logger.info("Loading selected columns from Parquet: %s",
                                columns if columns else "All Columns")

                    logger.info("Loading Parquet data into DataFrame...")
                    table = pq.read_table(buffer, columns=columns)
                    df = table.to_pandas()
            else:
                logger.info(
                    "Loading Parquet data into DataFrame without progress...")
                df = pd.read_parquet(gcs_url, engine="pyarrow",
                                     storage_options={"token": "anon"}, columns=columns)
            logger.info("DataFrame loaded successfully.")

            logger.info(
                "Successfully loaded Parquet file with shape: %s", df.shape)
            return df

        except Exception as e:
            logger.error(
                "Failed to load Parquet with progress. Error: %s", str(e))
            return None


def load_dataset(
    dataset_name: str = "default",
    show_progress: bool = True,
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Convenience function to load a pre-configured dataset.

    Args:
        dataset_name: Name of the pre-configured dataset
        columns: Specific columns to load (optional)
        show_progress: Whether to display a progress bar (default: True)

    Returns:
        pandas DataFrame containing the dataset
    """

    loader = DataLoader(
        dataset_name=dataset_name, columns=columns, show_progress=show_progress
    )
    return loader.load_dataset(
        dataset_name=dataset_name, columns=columns, show_progress=show_progress
    )


def list_datasets(dataset_name: str = "default") -> Dict[str, str]:
    """
    List all available pre-configured datasets.

    Returns:
        Dictionary mapping dataset names to their descriptions
    """
    loader = DataLoader(dataset_name=dataset_name)
    return loader.list_available_datasets()


def get_columns(dataset_name: str = "dafault") -> Dict[str, str]:
    """
    Get information about available columns in a dataset.

    Args:
        dataset_name: Name of the pre-configured dataset

    Returns:
        Dictionary mapping column names to their descriptions
    """
    print("dataset_name", dataset_name)
    loader = DataLoader(dataset_name=dataset_name)
    return loader.get_dataset_columns(dataset_name)


def read_yaml_file(
    self,
    yaml_file_path: str
) -> Optional[dict]:
    """
    Reads a YAML file from a public Google Cloud Storage bucket.

    Parameters:
        gcs_url (str): The full GCS path to the YAML file (e.g., 'gs://my-public-bucket/data/file.yaml').

    Returns:
        Optional[dict]: A dictionary containing the YAML data if the file is read successfully, otherwise None.
    """
    try:
        with open(yaml_file_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
        logger.info("Successfully read YAML file.")
        return yaml_data
    except Exception as e:
        logger.error(
            "Failed to read YAML file from %s. Error: %s", yaml_file_path, str(e))
        return None


def read_yaml_file(
    yaml_file_path: str
) -> Optional[dict]:
    """
    Reads a YAML file from a public Google Cloud Storage bucket.

    Parameters:
        gcs_url (str): The full GCS path to the YAML file (e.g., 'gs://my-public-bucket/data/file.yaml').

    Returns:
        Optional[dict]: A dictionary containing the YAML data if the file is read successfully, otherwise None.
    """
    try:
        with open(yaml_file_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
        logger.info("Successfully read YAML file.")
        return yaml_data
    except Exception as e:
        logger.error(
            "Failed to read YAML file from %s. Error: %s", yaml_file_path, str(e))
        return None


# if __name__ == "__main__":
#     load_dataset(columns=["ECFP4", "DELLabel"])
#     # col = get_columns("default")
#     col = list_datasets("default")
#     print("Columns in the dataset:", col)
#     exit()
#     # Example usage
#     dict = read_yaml_file("config.yaml")
#     if dict is not None:
#         print("YAML data:\n", dict)
#     else:
#         print("Failed to read the YAML file.")
#     exit()
#     gcs_url = "gs://aircheck-workshop-readonly/TrainDataset_Aircheck.parquet"
#     # df = read_parquet_from_gcs(gcs_url)
#     df = read_parquet_with_progress(
#         gcs_url, columns=["ECFP4", "DELLabel"], show_progress=False)
#     if df is not None:
#         print("DataFrame head:\n", df.head())
#         print("DataFrame length:", len(df))
#     else:
#         print("Failed to read the Parquet file.")


# python3 -m build
