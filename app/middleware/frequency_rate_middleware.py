from fastapi import HTTPException
import time


class FrequencyRateMiddleware:
    def __init__(self, min_interval: float = 0.1, max_interval: float = 1.0):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.last_request_time = {}

    def check_rate(self, server_ulid: str):        
        current_time = time.time()

        if server_ulid in self.last_request_time:
            last_time = self.last_request_time[server_ulid]
            interval = current_time - last_time

            if interval < self.min_interval:
                raise HTTPException(
                    status_code=429, detail="Request frequency too low (min 1 Hz)"
                )

            if interval > self.max_interval:
                raise HTTPException(
                    status_code=429, detail="Request frequency too high (max 10 Hz)"
                )

        self.last_request_time[server_ulid] = current_time
