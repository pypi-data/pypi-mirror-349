def file_size(size_in_bytes: float, precision: int = 2) -> str:
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    index = 0
    while (size_in_bytes / 1024) > 0.9 and (index < len(units) - 1):
        size_in_bytes /= 1024
        index += 1

    return f"{size_in_bytes:.{precision}f} {units[index]}"
