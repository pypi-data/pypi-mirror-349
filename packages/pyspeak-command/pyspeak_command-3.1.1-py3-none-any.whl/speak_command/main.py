import sys, io
# import controller as control
# import utils as util
# from speak_command import utils as util
from speak_command import controller as control

args = sys.argv

def main():
    
    if len(args) < 2:
        control.run_help(1, args)
        sys.exit()

    cmd = args[1:]
    
    match cmd[0]:
        case '--pyFile':
            control.run_scripts(len(cmd), cmd)
        case '--help' | '--h':
            control.run_help(len(cmd), cmd)
        case '--file':
            control.run_file(len(cmd), cmd)
        case _:
            control.run_normal_command(len(cmd), cmd)


if __name__ == "__main__":
    main()