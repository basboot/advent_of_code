file1 = open('q2a.txt', 'r')
lines: [str] = file1.readlines()

part: int = 2

def is_safe(report: [int]) -> bool:
    inc_report: [int] = sorted(report)
    dec_recport: [int] = sorted(report, reverse=True)

    # sequence can only be safe when increasing or decreasing
    if report == inc_report or report == dec_recport:
        valid: bool = True
        for i in range(1, len(report)):
            # only valid if interval is 1-3
            if not (0 < abs(report[i] - report[i - 1]) < 4):
                valid = False
                break
        if valid:
            return True
    return False


total: int = 0

for line in lines:
    report: [int] = [int(x) for x in line.rstrip().split()]
    if is_safe(report):
        total += 1
        continue

    if part == 1:
        continue

    # if not safe, try to fix by removing one number
    for i in range(len(report)):
        smaller_report: [int] = report.copy()
        smaller_report.pop(i)

        if is_safe(smaller_report):
            total += 1
            break

print(f"Part {part}, {total}")

