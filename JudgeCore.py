import pathlib
import difflib


def diff(ans_str: str, out_str: str, print_info=True, stop_at=5):
    ans_lines = [line for line in ans_str.splitlines() if line[0] == '@' or line[0] == '@']
    out_lines = [line for line in out_str.splitlines() if line[0] == '@' or line[0] == '@']
    if print_info:
        print(f"Answer: {len(ans_lines)} lines / Output: {len(out_lines)} lines")
    ans_line, out_line = 1, 1
    wrong_count = 0
    for line in difflib.ndiff(ans_lines, out_lines):
        if line[0] == '+':
            print(f"Answer: line{ans_line}: {line[2:]}")
            ans_line += 1
            wrong_count += 1
        elif line[0] == '-':
            print(f"Output: line{out_line}: {line[2:]}")
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
