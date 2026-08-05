def bytes_to_gb(value: int) -> float:
    """Convert bytes to gigabytes."""
    return round(value / (1024 ** 3), 2)