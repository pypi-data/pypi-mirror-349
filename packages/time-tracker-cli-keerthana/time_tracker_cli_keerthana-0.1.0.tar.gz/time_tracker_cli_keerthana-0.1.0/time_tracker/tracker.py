import json
import os
from datetime import datetime, timedelta
import argparse
from rich.console import Console
from rich.table import Table
from rich import box
import csv
import matplotlib.pyplot as plt

console = Console()
DATA_FILE = "tracker_data.json"
TIME_FORMAT = "%d-%m-%Y %H:%M:%S"  # Custom date-time format


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"active_task": None, "task_log": []}
    
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"active_task": None, "task_log": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def start_task(task_name):
    data = load_data()
    if data["active_task"]:
        console.print("[yellow]A task is already running.[/]")
        return
    data["active_task"] = {
        "name": task_name,
        "start": datetime.now().strftime(TIME_FORMAT)
    }
    save_data(data)
    console.print(f"[green]Started task:[/] {task_name}")


def stop_task():
    data = load_data()
    if not data["active_task"]:
        console.print("[red]No active task to stop.[/]")
        return
    task = data["active_task"]
    start_time = datetime.strptime(task["start"], TIME_FORMAT)
    end_time = datetime.now()
    task["end"] = end_time.strftime(TIME_FORMAT)
    delta = end_time - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    task["duration"] = f"{hours:02}:{minutes:02}:{seconds:02}"
    data["task_log"].append(task)
    data["active_task"] = None
    save_data(data)
    console.print(f"[red]Stopped task:[/] {task['name']} | Duration: [bold]{task['duration']}[/]")


def show_status():
    data = load_data()
    task = data["active_task"]
    if task:
        console.print(f"[cyan]Active task:[/] {task['name']} (started at {task['start']})")
    else:
        console.print("[yellow]No active task.[/]")


def show_report():
    data = load_data()
    logs = data.get("task_log", [])

    if not logs:
        console.print("[yellow]No task history found.[/]")
        return

    table = Table(title="Task History", box=box.SIMPLE)
    table.add_column("Task", style="magenta")
    table.add_column("Start", style="dim")
    table.add_column("End", style="dim")
    table.add_column("Duration", style="green")

    for task in logs:
        table.add_row(task["name"], task["start"], task["end"], task["duration"])

    console.print(table)


def export_to_csv():
    data = load_data()
    logs = data.get("task_log", [])

    if not logs:
        console.print("[yellow]No data to export.[/]")
        return

    with open("task_report.csv", "w", newline="") as csvfile:
        fieldnames = ["Task", "Start", "End", "Duration"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for task in logs:
            writer.writerow({
                "Task": task["name"],
                "Start": task["start"],
                "End": task["end"],
                "Duration": task["duration"]
            })

    console.print("[green]Exported data to task_report.csv[/]")


def show_summary(summary_type="daily"):
    data = load_data()
    logs = data.get("task_log", [])

    if not logs:
        console.print("[yellow]No tasks logged yet.[/]")
        return

    now = datetime.now()
    summary = {}

    for task in logs:
        try:
            start_time = datetime.strptime(task["start"], TIME_FORMAT)
            if summary_type == "daily" and start_time.date() != now.date():
                continue
            if summary_type == "weekly" and (now - start_time).days > 7:
                continue

            task_name = task["name"]
            h, m, s = map(int, task["duration"].split(":"))
            seconds = h * 3600 + m * 60 + s
            summary[task_name] = summary.get(task_name, 0) + seconds
        except Exception as e:
            console.print(f"[red]Error processing task '{task['name']}':[/] {e}")

    if not summary:
        console.print(f"[yellow]No {summary_type} data available.[/]")
        return

    table = Table(title=f"{summary_type.capitalize()} Summary", box=box.SIMPLE)
    table.add_column("Task", style="magenta")
    table.add_column("Total Time", style="green")

    for task_name, total_seconds in summary.items():
        hours, remainder = divmod(int(total_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted = f"{hours:02}:{minutes:02}:{seconds:02}"
        table.add_row(task_name, formatted)

    console.print(table)
    plot_summary_graph(summary, summary_type)


def plot_summary_graph(summary, summary_type):
    task_names = list(summary.keys())
    durations = list(summary.values())
    durations_in_hours = [round(sec / 3600, 2) for sec in durations]  # Convert to hours

    plt.figure(figsize=(10, 6))
    bars = plt.bar(task_names, durations_in_hours, color="skyblue")
    plt.xlabel("Tasks")
    plt.ylabel("Total Time (hours)")
    plt.title(f"{summary_type.capitalize()} Task Summary")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    for bar, duration in zip(bars, durations_in_hours):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{duration}h',
                 ha='center', va='bottom', fontsize=8)

    
    plt.show()  # Pop-up graph
    plt.savefig("summary_chart.png")
    console.print("[green]Saved graph as summary_chart.png[/]")
