import sys


def BPRprimitive(capacity: float, freeFlow: float, b: float, power: float, flow: float) -> float:
    """
    Primitive function of the BPR function with respect to flow
    BPR: c(x) = f * ( 1 + 0.15 * (x/K)^4 ), f...free flow, K...capacity, x...current flow
    """
    a = b / (power + 1)
    c = (flow / capacity) ** power
    return freeFlow * flow * (1 + a * c)


def objective_function(net_file: str, flow_file: str):
    """Calculates the objective function from net file and assigned flows (flow file)"""
    dic = {}

    with open(net_file, 'r') as net:
        lines = net.readlines()

        # skip header
        i = 0
        for line in lines:
            i += 1
            if line.startswith("END"):
                break

        for line in lines[i:]:
            split = line.split()

            start = int(split[0])
            end = int(split[1])

            capacity = float(split[2])
            freeflow = float(split[3])
            b = float(split[7])
            power = float(split[8])

            dic[(start, end)] = [capacity, freeflow, b, power]

    with open(flow_file, 'r') as f:
        for line in f.readlines():
            split = line.split()
            start = int(split[0])
            end = int(split[1])
            flow = float(split[2])
            dic[(start, end)].append(flow)

    value = 0
    for key in dic:
        val = dic[key]
        value += BPRprimitive(*val)

    print(f"Value of objective function: {value}")


if __name__ == '__main__':
    objective_function(sys.argv[1], sys.argv[2])
