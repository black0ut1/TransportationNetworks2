import sys


def sanitize(string: str) -> str:
    """Removes comments and leading and trailing whitespaces"""
    return string.split('~')[0].strip()


def parse_header(file: list[str]) -> (dict[str, str], int):
    header = {}
    i = 0
    for i, line in enumerate(file):
        line = sanitize(line)
        if len(line) == 0:
            continue

        split = line.split('>')
        key = split[0][1:].strip()

        if key == "END OF METADATA":
            break

        value = split[1].strip()
        header[key] = value

    return header, i + 1


def convert_net(file: list[str]) -> list[str]:
    header, i = parse_header(file)
    nodes = header["NUMBER OF NODES"]
    zones = header["NUMBER OF ZONES"]
    edges = header["NUMBER OF LINKS"]

    new_lines = [
        f"NODES:{nodes}\n",
        f"ZONES:{zones}\n",
        f"EDGES:{edges}\n",
        "END\n"
    ]

    for line in file[i:]:
        line = sanitize(line)
        if len(line) == 0:
            continue

        split = line.split()
        init_node = int(split[0]) - 1
        term_node = int(split[1]) - 1
        capacity = split[2]
        length = split[3]
        free_flow_time = split[4]
        b = split[5]
        power = split[6]
        speed = split[7]
        toll = split[8]
        link_type = split[9]
        if link_type.endswith(';'):
            link_type = link_type[0: len(link_type) - 1]
        new_lines.append(f"{init_node} {term_node} {capacity} {free_flow_time} "
                         f"{length} {speed} {toll} {b} {power} {link_type}\n")

    return new_lines


def convert_trips(file: list[str]) -> list[str]:
    header, i = parse_header(file)
    zones = int(header["NUMBER OF ZONES"])
    total_flow = header["TOTAL OD FLOW"]

    new_lines = [
        f"ZONES:{zones}\n",
        f"FLOW:{total_flow}\n",
        "END\n"
    ]

    odm = [[0.0] * zones for _ in range(zones)]
    from_zone = None
    for line in file[i:]:
        line = sanitize(line)
        if len(line) == 0:
            continue

        if line.startswith("Origin"):
            from_zone = int(line.split()[1]) - 1
            continue

        split = line.split(';')
        for pair in split:
            if len(pair.strip()) == 0:
                continue

            split2 = pair.split(':')
            to_zone = int(split2[0].strip()) - 1
            flow = float(split2[1].strip())
            odm[from_zone][to_zone] = flow

    for from_zone in range(zones):
        line = f"{from_zone} "
        for to_zone in range(zones):
            flow = odm[from_zone][to_zone]
            if flow == 0:
                continue

            line += f"{to_zone}:{flow} "
        new_lines.append(line[0:len(line) - 1] + '\n')

    return new_lines


def convert_flow(file: list[str]) -> list[str]:
    new_lines = []

    for line in file[1:]:
        line = sanitize(line)
        if len(line) == 0:
            continue

        try:
            int(line[0])
        except ValueError:
            continue

        split = line.split()
        from_node = int(split[0]) - 1
        to_node = int(split[1]) - 1
        new_lines.append(f"{from_node} {to_node} {split[2]} {split[3]}\n")

    return new_lines


def convert_nodes(file: list[str]) -> list[str]:
    new_lines = []

    for line in file[1:]:
        line = sanitize(line)
        if len(line) == 0:
            continue

        split = line.split()
        new_lines.append(f"{int(split[0]) - 1} {split[1]} {split[2]}\n")

    return new_lines


def convert(path: str):
    with open(path) as file:
        lines = file.readlines()
    name = path.split('_')[0]

    if "net" in path.lower():
        new_lines = convert_net(lines)
        with open(f"{name}.net.tntp", 'w') as file:
            file.writelines(new_lines)

    elif "trips" in path.lower():
        new_lines = convert_trips(lines)
        with open(f"{name}.odm.tntp", 'w') as file:
            file.writelines(new_lines)

    elif "flow" in path.lower():
        new_lines = convert_flow(lines)
        with open(f"{name}.flow.tntp", 'w') as file:
            file.writelines(new_lines)

    elif "node" in path.lower():
        new_lines = convert_nodes(lines)
        with open(f"{name}.node.tntp", 'w') as file:
            file.writelines(new_lines)


if __name__ == '__main__':
    convert(sys.argv[1])
