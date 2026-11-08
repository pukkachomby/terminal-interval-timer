#!/usr/bin/env python3
import time
import sys
import select
import shutil
import subprocess

def clear_screen():
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def beep():
    sys.stdout.write("\a")
    sys.stdout.flush()

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def print_banner(text):
    # Try figlet or toilet using the 'big' font which is ideal for large numbers
    for cmd in ['figlet', 'toilet']:
        if shutil.which(cmd):
            try:
                result = subprocess.run([cmd, '-f', 'big', text], stdout=subprocess.PIPE, text=True, check=True)
                print(result.stdout)
                return
            except Exception:
                pass

    # Absolute fallback if neither figlet nor toilet is installed on the system
    print(f"\n   [ TIME: {text} ]\n")

def run_timer(duration_seconds, label="Interval"):
    if duration_seconds <= 0:
        return

    total = duration_seconds
    remaining = total
    paused = False

    while remaining > 0:
        clear_screen()
        print("=== TERMINAL INTERVAL TIMER ===")
        print(f"Current Phase: {label}\n")

        print_banner(format_time(remaining))

        print("\nControls: [p] Pause/Resume | [q] Quit")

        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            char = sys.stdin.read(1)
            if char.lower() == 'q':
                print("\nTimer stopped.")
                sys.exit(0)
            elif char.lower() == 'p':
                paused = not paused
                if paused:
                    print("\n[PAUSED] Press 'p' to resume...")
                    while paused:
                        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                        if rlist:
                            c = sys.stdin.read(1)
                            if c.lower() == 'q':
                                sys.exit(0)
                            elif c.lower() == 'p':
                                paused = False
                        time.sleep(0.1)

        if not paused:
            time.sleep(1)
            remaining -= 1

    beep()

def main():
    work_seconds = 150
    if len(sys.argv) > 1:
        try:
            minutes = float(sys.argv[1])
            work_seconds = int(minutes * 60)
        except ValueError:
            print(f"Invalid duration argument: {sys.argv[1]}. Using default 150 seconds.")
            time.sleep(1)

    import termios
    import tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)

        print("Starting timer sequence...")
        time.sleep(1)

        run_timer(5, label="Preparation")

        rounds = 10
        for r in range(1, rounds + 1):
            run_timer(work_seconds, label=f"Work Round {r}/{rounds}")
            if r < rounds:
                run_timer(0, label=f"Rest Round {r}")

        clear_screen()
        print_banner("DONE")
        beep()
        time.sleep(2)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()
