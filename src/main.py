import terminal

def entry_standalone():
    terminal.clear_screen()
    running = True
    print("Press 'q' to quit. Click or press keys...\n")
    
    while running:
        while event := terminal.read_input():
            print(event)
            if event['type'] == 'key' and event['key'] == 'q':
                running = False
                break

    
def entry_args(args: list[str]):
    ...

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        entry_standalone()
    else:
        entry_args(sys.argv[1:])