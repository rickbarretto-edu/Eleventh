

def metadata(lines: list[str]) -> dict[str, str]:
    separator = ":"

    def pair(line: str) -> tuple[str, str]:
        key, val = line.strip().split(separator, 1)
        return key.strip(), val.strip()

    def key(line: str) -> str:
        key, _ = pair(line)
        return key.lower()
    
    def value(line: str) -> str:
        _, val = pair(line)
        return val

    return {
        key(line): value(line)
        for line in lines
        if ":" in line
    }