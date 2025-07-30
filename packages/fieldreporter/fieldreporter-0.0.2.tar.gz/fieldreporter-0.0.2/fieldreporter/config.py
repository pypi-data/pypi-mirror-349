from dataclasses import dataclass, field
import datetime
import yaml
import re


@dataclass
class FieldReporterTelegramDestinationConfig:
    api_token: str
    chat_id: str


@dataclass
class FieldReporterScheduleConfig:
    at_times: list = field(default_factory=list)
    at_interval: float = None


@dataclass
class FieldReporterConfig:
    destinations: list
    monitors: list
    schedule: FieldReporterScheduleConfig


@dataclass
class FieldReporterDiskSpaceMonitorConfig:
    disks: list = field(default_factory=list)
    threshold_gb: float = 10


@dataclass
class FieldReporterPathsExistMonitorConfig:
    pattern: str
    created_since: int = None
    minimum_count: int = 1


def load_config(file_path: str):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    destinations = []
    for destination in config.get('destinations', []):
        if destination["type"] == "telegram":
            destination = FieldReporterTelegramDestinationConfig(api_token=destination["api_token"],
                                                                 chat_id=destination["chat_id"])
        destinations.append(destination)

    schedule = FieldReporterScheduleConfig()
    schedule_config = config.get('schedule', {})
    at_times = schedule_config.get('at_times', [])
    for at_time in at_times:
        pattern = r'^(\d{2}):(\d{2})$'
        match = re.match(pattern, at_time)
        if not match:
            raise ValueError(f"Invalid time format: {at_time}. Expected HH:MM.")
        hour = int(match.group(1))
        minute = int(match.group(2))

        schedule.at_times.append(datetime.time(hour=hour, minute=minute))

    monitors = []
    for monitor_type, monitor_config in config["monitors"].items():
        if monitor_type == "paths_exist":
            monitor = FieldReporterPathsExistMonitorConfig(pattern=monitor_config.get("pattern"),
                                                           created_since=monitor_config.get("created_since", None),
                                                           minimum_count=monitor_config.get("minimum_count", 1))
            monitors.append(monitor)
        elif monitor_type == "disk_space":
            threshold = monitor_config.get("threshold", 10)
            if threshold.endswith("G"):
                threshold = float(threshold[:-1])
            monitor = FieldReporterDiskSpaceMonitorConfig(disks=monitor_config.get("disks", None),
                                                          threshold_gb=threshold)
            monitors.append(monitor)
    config = FieldReporterConfig(destinations=destinations,
                                 monitors=monitors,
                                 schedule=schedule)

    return config
