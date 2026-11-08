#!/usr/bin/env python3
import time
import sys
import select
import os

def clear_screen():
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def beep():
    # Triggers the terminal bell
    sys.stdout.write("\a")
    sys.stdout.flush()

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def draw_progress_bar(current, total, width=30):
    if total <= 0:
        filled = width
    else:
        filled = int(width * (current / total))
    bar = "=" * filled + "-" * (width - filled)
    return f"[{bar}]"

def run_timer(duration_seconds, label="Interval"):
    total = duration_seconds
    remaining = total
    paused = False

    while remaining > 0:
        clear_screen()
        print("=== TERMINAL INTERVAL TIMER ===")
        print(f"Current Phase: {label}")
        print(f"Time Remaining: {format_time(remaining)}")
        print(draw_progress_bar(total - remaining, total))
        print("\nControls: [p] Pause/Resume | [q] Quit")

        # Check for user input without blocking for long
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
    # Make terminal read input instantly without requiring Enter key
    import termios
    import tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)

        # Example workout structure: Prep, Work, Rest
        print("Starting timer sequence...")
        time.sleep(1)

        run_timer(5, label="Preparation")

        # Run a sample 3-round interval session (e.g., 45s work, 15s rest)
        rounds = 10
        for r in range(1, rounds + 1):
            run_timer(150, label=f"Work Round {r}/{rounds}")
            if r < rounds:
                run_timer(0, label=f"Rest Round {r}")

        clear_screen()
        print("=== WORKOUT COMPLETE! ===")
        beep()
        time.sleep(2)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()
