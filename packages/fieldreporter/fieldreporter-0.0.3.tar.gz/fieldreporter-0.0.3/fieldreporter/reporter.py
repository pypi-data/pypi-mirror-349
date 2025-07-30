from apscheduler.schedulers.background import BackgroundScheduler
from .config import load_config
from .config import FieldReporterTelegramDestinationConfig
from .config import FieldReporterDiskSpaceMonitorConfig, FieldReporterPathsExistMonitorConfig, FieldReporterUptimeMonitorConfig
from .destinations import TelegramDestination
from .monitors import FieldReporterDiskSpaceMonitor, FieldReporterPathsExistMonitor, FieldReporterUptimeMonitor
from .exceptions import ConditionFailedException
import time

class FieldReporter:
    def __init__(self, config_path):
        self.destinations = []
        self.monitors = []
        self.schedule = []
        config = load_config(config_path)
        for destination_config in config.destinations:
            if isinstance(destination_config, FieldReporterTelegramDestinationConfig):
                self.destinations.append(TelegramDestination(destination_config.api_token,
                                                             destination_config.chat_id))
        for monitor_config in config.monitors:
            if isinstance(monitor_config, FieldReporterDiskSpaceMonitorConfig):
                self.monitors.append(FieldReporterDiskSpaceMonitor(threshold=monitor_config.threshold_gb,
                                                                   disks=monitor_config.disks))
            elif isinstance(monitor_config, FieldReporterPathsExistMonitorConfig):
                self.monitors.append(FieldReporterPathsExistMonitor(pattern=monitor_config.pattern,
                                                                    created_since=monitor_config.created_since,
                                                                    minimum_count=monitor_config.minimum_count))
            elif isinstance(monitor_config, FieldReporterUptimeMonitorConfig):
                self.monitors.append(FieldReporterUptimeMonitor(minimum_uptime=monitor_config.minimum_uptime,
                                                                maximum_uptime=monitor_config.maximum_uptime))
        self.schedule = config.schedule

    def run(self):
        scheduler = BackgroundScheduler()
        scheduler.start()
        
        for at_time in self.schedule.at_times:
            scheduler.add_job(self.check_all, 'cron', hour=at_time.hour, minute=at_time.minute)

        at_times_str = ", ".join([f"{at_time.hour:02}:{at_time.minute:02}" for at_time in self.schedule.at_times])
        print("FieldReporter: Scheduler started. Waiting for scheduled checks (at times: %s)..." % at_times_str)

        while True:
            time.sleep(1)
    
    def error(self, message):
        for destination in self.destinations:
            destination.send("ERROR: %s" % message)

    def warning(self, message):
        for destination in self.destinations:
            destination.send("WARNING: %s" % message)

    def check_all(self):
        print("FieldReporter: Checking all monitors...")
        for monitor in self.monitors:
            try:
                monitor.check()
            except ConditionFailedException as e:
                print(f" - Condition failed: {e}")
                self.error(str(e))
                