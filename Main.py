import sys

from Run import run

if __name__ == "__main__":
    template_list, count = None, 10
    if len(sys.argv) > 1:
        template_list = []
        for arg in sys.argv[1:]:
            if arg.startswith("count="):
                count = int(arg.removeprefix("count="))
            else:
                template_list.append(arg)
    if not template_list:
        template_list = None

    run(count=count, template_used=template_list)
