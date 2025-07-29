### README.md

# Time Tracker CLI

A simple command-line tool to help you track tasks, time spent, and generate reports or summaries.

## Features

- Start and stop tasks
- View status of ongoing task
- Generate daily or weekly summaries
- Export logs to CSV
- View Graphical reports
- Persistent Local storage
- Easy-to-use CLI Interface

## Requirements

- Python 3.7+
- [matplotlib](https://matplotlib.org/)

## Installation

```bash
pip install time-tracker-cli-keerthana
```
## Commands

- `start` – Start a task (use `--task "Task Name"`)
- `stop` – Stop the currently running task
- `status` – Show current active task
- `summary` – Show summary of tasks (daily/weekly)
- `export` – Export logs as CSV
- `report` – Show a bar graph of time spent on tasks

## Usage

```bash
time-tracker start --task "Writing"
time-tracker status
time-tracker stop
time-tracker summary --type daily
time-tracker summary --type weekly
time-tracker export
time-tracker report
```
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.