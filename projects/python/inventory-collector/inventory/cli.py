import argparse

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Inventory Collector")
    parser.add_argument(
        "--output",
        type=str,
<<<<<<< HEAD
        default= None,
=======
        default=None,
>>>>>>> 7544b3ff25569fa0649e0e7d7d353c63847014b9
        help="Output JSON filename (default: inventory.json)",
    )

    parser.add_argument(
        "--pretty",
        # type=str,
        action="store_true",
        default=None,
        help="Pretty-print the output JSON (default: False)",
    )

    parser.add_argument(
        "--no-network",
        action="store_true",
        default=None,
        help="Disable network information collection",
    )

    # parser.add_argument(
    #     "--collect-os",
    #     action="store_true",
    #     help="Collect OS information",
    # )
    # parser.add_argument(
    #     "--collect-cpu",
    #     action="store_true",
    #     help="Collect CPU information",
    # )
    # parser.add_argument(
    #     "--collect-memory",
    #     action="store_true",
    #     help="Collect memory information",
    # )
    # parser.add_argument(
    #     "--collect-disk",
    #     action="store_true",
    #     help="Collect disk information",
    # )
    # parser.add_argument(
    #     "--collect-network",
    #     action="store_true",
    #     help="Collect network information",
    # )
    return parser.parse_args()