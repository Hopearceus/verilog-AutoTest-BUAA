import pathlib
import difflib


def diff(ans_str: str, out_str: str, print_info=True, stop_at=5):
    def line_filter(line: str):
        if len(line) == 0:
            return False
        if line.strip(" \t0123456789")[0] != '@':
            return False
        idx = line.find('$')
        if idx != -1 and line[idx: idx + 3] == "$ 0":
            return False
        return True

    def remove_time_stamp(line: str):
        idx = line.find('@')
        if idx != -1:
            return line[idx:]
        return ""

    def sort_key_time(line: str):
        idx1, idx2 = line.find('@'), line.find(':')
        pc = int(line[idx1 + 1:idx2], 16)
        if idx1 == 0:
            return pc
        else:
            return pc + int(line[:idx1]) * 0x00010000

    ans_lines = [line for line in ans_str.splitlines() if line_filter(line)]
    out_lines = [line for line in out_str.splitlines() if line_filter(line)]
    out_lines.sort(key=sort_key_time)
    out_lines = list(map(remove_time_stamp, out_lines))
    if print_info:
        print(f"Answer: {len(ans_lines)} lines / Output: {len(out_lines)} lines")
    ans_line, out_line = 1, 1
    wrong_count = 0
    for line in difflib.ndiff(ans_lines, out_lines):
        if line[0] == '+':
            print(f"Output: line{ans_line}: {line[2:]}")
            ans_line += 1
            wrong_count += 1
        elif line[0] == '-':
            print(f"Answer: line{out_line}: {line[2:]}")
            out_line += 1
            wrong_count += 1
        elif line[0] != '?':
            ans_line += 1
            out_line += 1
        if wrong_count >= stop_at:
            break
    return wrong_count == 0


if __name__ == "__main__":
    print(diff(pathlib.Path("temporary/mars.out").read_text(), pathlib.Path("temporary/mars_less.out").read_text()))
