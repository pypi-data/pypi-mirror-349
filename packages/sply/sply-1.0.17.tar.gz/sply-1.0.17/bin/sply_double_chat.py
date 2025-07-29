#!/usr/bin/env python3

import sys
import random
import sply
import time


def main ():
    # TODO: load these dicts from config
    names = {
        "ai_1": "Amy",
        "ai_2": "Amber",
        "log_path": "sply_double_chat.log",
    }


    c1_args = sply.chat.get_default_args()
    c1_args |= {
        "backend": "llama-server",
        "port": 8080,
        "user_name": names["ai_2"],
        "user_desc": "is a girl",
        "ai_name": names["ai_1"],
        "ai_desc": "is another girl",
        "in_suffix": "",
        "in_suffix_enabled": False,
        "rev_prompt": f"{names["ai_2"]}:",
        "seed": -1,
        "temp": 0.6,
        "num_ctx": 16384,
        }

    c2_args = sply.chat.get_default_args()
    c2_args |= {
        "backend": "llama-server",
        "port": 8081,
        "user_name": names["ai_1"],
        "user_desc": c1_args["ai_desc"],
        "ai_name": names["ai_2"],
        "ai_desc": c1_args["user_desc"],
        "in_suffix": "",
        "in_suffix_enabled": False,
        "rev_prompt": f"{names["ai_1"]}:",
        "seed": -1,
        "temp": 0.9,
        "num_ctx": 16384,
        }

    for sys_arg in sys.argv[1:]:
        if sys_arg.find("--help") == 0:
            print(f"Usage: {sys.argv[0]} [options]\n"
                  f"  where [options] are zero or more of:")
            sply.chat.print_default_args("    c1_", c1_args)
            sply.chat.print_default_args("    c2_", c2_args)
            exit(-1)

        for param_d in sply.chat.param_desc:
            if sys_arg.find("c1_" + param_d["name"] + "=") == 0:
                sys_arg_param, sys_arg_value = sys_arg.split("=")
                sys_arg_param = sys_arg_param[3:]
                param_type = param_d["type"]
                if param_type == str:
                    c1_args[sys_arg_param] = sys_arg_value
                elif param_type == bool:
                    c1_args[sys_arg_param] = True if sys_arg_value == "True" else False
                elif param_type == int:
                    c1_args[sys_arg_param] = int(sys_arg_value)
                elif param_type == float:
                    c1_args[sys_arg_param] = float(sys_arg_value)

            if sys_arg.find("c2_" + param_d["name"] + "=") == 0:
                sys_arg_param, sys_arg_value = sys_arg.split("=")
                sys_arg_param = sys_arg_param[3:]
                param_type = param_d["type"]
                if param_type == str:
                    c2_args[sys_arg_param] = sys_arg_value
                elif param_type == bool:
                    c2_args[sys_arg_param] = True if sys_arg_value == "True" else False
                elif param_type == int:
                    c2_args[sys_arg_param] = int(sys_arg_value)
                elif param_type == float:
                    c2_args[sys_arg_param] = float(sys_arg_value)

    if c1_args["seed"] == -1:
        c1_args["seed"] = random.randrange(2**32)

    if c2_args["seed"] == -1:
        c2_args["seed"] = random.randrange(2**32)

    print(f"c1_args={c1_args}")
    print(f"c2_args={c2_args}")

    c1 = sply.chat(**c1_args)
    c2 = sply.chat(**c2_args)

    # modify the default prompt's greeting, which is prefaced with '\n'
    c2.prompt = c2.prompt[: c2.prompt.find("\n")] +\
          c2.make_prompt_greet(c2_args["ai_name"], c2_args["user_name"])
    c2.updated_prompt()

    interactive = False
    interrupted = False
    turn = 1

    running = True
    while running:
        while interactive:
            cmd = input("🔢")
            if not cmd:
                break
            elif cmd == "h":
                # TODO print("a1: list c1 adjustable params and current values\n"
                # TODO print("a1 [param]: display c1 param's value\n"
                # TODO print("a1 [param]=[value]: adjust c1 param to value\n"
                print("enter: next iteration")
                print("h: this help")
                print("e1: edit c1 prompt")
                print("e2: edit c2 prompt")
                print("p1: display c1 [[prompt]]")
                print("p2: display c2 [[prompt]]")
                print("i: disable interactive")
                print("q: quit running")
            #TODO elif cmd == "a1":
            elif cmd == "e1":
                c1.edit_prompt()
            elif cmd == "e2":
                c2.edit_prompt()
            elif cmd == "p1":
                print(f"[[{c1.prompt}]]")
            elif cmd == "p2":
                print(f"[[{c2.prompt}]]")
            elif cmd == "i":
                interactive = False
                break
            elif cmd == "q":
                running = False
                break

        if not running:
            break

        if turn == 1:
            while True:
                in1, interrupted = c1.read(show=True)
                if in1:
                    break
                else:
                    print("", end="", flush=True)
                    time.sleep(1)

            with open(names["log_path"], "a") as f:
                f.write(in1)

            c2.write(in1, show=False)

            if interrupted:
                interrupted = False
                interactive = True
                continue

            turn = 2

        if turn == 2:
            while True:
                in2, interrupted = c2.read(show=True)
                if in2:
                    break
                else:
                    print("", end="", flush=True)
                    time.sleep(1)

            with open(names["log_path"], "a") as f:
                f.write(in2)

            c1.write(in2, show=False)

            if interrupted:
                interrupted = False
                interactive = True
                continue

            turn = 1


    return 0


if __name__ == "__main__":
    exit(main())

