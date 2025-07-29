
import argparse
from time_tracker.tracker import (
    start_task,
    stop_task,
    show_status,
    show_report,
    export_to_csv,
    show_summary,
)
def main():
    parser = argparse.ArgumentParser(description="CLI Time Tracker")
    parser.add_argument("command", choices=["start", "stop", "status", "report", "export", "summary"])
    parser.add_argument("--task", help="Task name (required for start)")
    parser.add_argument("--type", choices=["daily", "weekly"], help="Summary type for summary command")
    args = parser.parse_args()

    if args.command == "start":
        if not args.task:
            console.print("[red]Please provide a task name with --task[/]")
            return
        start_task(args.task)
    elif args.command == "stop":
        stop_task()
    elif args.command == "status":
        show_status()
    elif args.command == "report":
        show_report()
    elif args.command == "export":
        export_to_csv()
    elif args.command == "summary":
        show_summary(args.type or "daily")

if __name__ == "__main__":
    main()
