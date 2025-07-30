import argparse

import sys


def main():
    try:
        parser = argparse.ArgumentParser(
            description="aircheckdata - A utility for loading AIRCHECK data from python environment and interacting with them."
        )
        parser.add_argument(
            "--list", action="store_true", help="List all available datasets."
        )
        parser.add_argument(
            "--load", nargs="?", const="WDR91",  help="Load a specific dataset by name."
        )
        parser.add_argument(
            "--columns", nargs="?", const="WDR91",  help="Specify Dataset name to view the available columns."
        )

        args = parser.parse_args()

        from aircheckdata import list_datasets, load_dataset, get_columns

        if args.list:
            print("Available datasets:")
            for d in list_datasets():
                print(f" - {d}")

        elif args.columns and not args.load:
            dataset = args.columns or "WDR91"
            print(f"Listing columns for dataset: {dataset}")
            print(f"Listing columns for dataset: {dataset}")
            columns = get_columns(dataset_name=dataset)
            for column in columns:
                print(f" - {column}")
            # print(f"Available columns for dataset {args.load} is {columns}:")
        elif args.load:
            dataset_name = args.load or "WDR91"
            columns = None
            if args.columns and ',' in args.columns:
                columns = [col.strip() for col in args.columns.split(',')]
            elif args.columns and args.columns != "WDR91":
                # If user passed a single column
                columns = [args.columns.strip()]
            print(f"Loading dataset: {dataset_name}")
            if columns:
                print(f"With columns: {columns}")
            df = load_dataset(dataset_name=dataset_name, columns=columns)
            print(
                f"Loaded dataset {dataset_name} with {len(df)} rows and {len(df.columns)} columns.")
        else:
            parser.print_help()
    except Exception as e:
        print(f"\n❌ An error occurred: {e}", file=sys.stderr)
        exit(1)
