def metadata(lines: list[str]) -> dict[str, str]:
    """Parse HTTP headers into a lowercase dictionary."""
    separator = ":"

    def pair(line: str) -> tuple[str, str]:
        key, val = line.strip().split(separator, 1)
        return key.strip().lower(), val.strip()

    return {
        key: val
        for line in lines
        if separator in line
        for key, val in [pair(line)]
    }
