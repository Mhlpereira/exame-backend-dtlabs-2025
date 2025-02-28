from fastapi import Request, HTTPException
from timescape import Timeline
import time


class FrequencyRateMiddleware:
    def __init__(self, min_interval: float = 1.0, max_interval: float = 0.1):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.timeline = Timeline()
        self.last_request_time = {}

    async def __call__(self, request: Request, call_next):
        server_ulid = request.headers.get("Server-ULID")
        if not server_ulid:
            raise HTTPException(status_code=400, detail="Server Ulid is required")

        current_time = time.time()

        if server_ulid in self.last_request_time:
            last_time = self.last_request_time[server_ulid]
            interval = current_time - last_time

            if interval < self.min_interval:
                raise HTTPException(
                    status_code=429, detail="Request frequency too high (max 10 Hz)"
                )

            if interval > self.max_interval:
                raise HTTPException(
                    status_code=429, detail="Request frequency too low (min 1 Hz)"
                )

        self.last_request_time[server_ulid] = current_time

        self.timeline.add_event(server_ulid, current_time)

        response = await call_next(request)

        return response
