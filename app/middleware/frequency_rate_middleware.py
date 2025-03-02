from fastapi import HTTPException
import logging
import datetime
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FrequencyRateMiddleware:
    def __init__(self, redis, queue_key: str):
        self.redis = redis  
        self.queue_key = queue_key
        self.frequency = 0
        self.last_request_time = "last_request_time"

    
    async def check_frequency(self):
        current_time = datetime.now()

        last_request_time_str = await self.redis.get(self.last_request_time_key)
        if last_request_time_str:
            last_request_time = datetime.datetime.fromisoformat(last_request_time_str.decode("utf-8"))

        time_diff = (current_time - last_request_time).total_seconds()

        if time_diff < 1:
            self.frequency += 1
            if self.frequency > 1:
                raise HTTPException(
                    status_code=429, detail='Request frequency too high (max 1 Hz)'
                )

        else:
            self.frequency = 1

        self.last_request_time = current_time

        await self.start_reset_timer()

        queue_size = await self.redis.llen(self.queue_key)

        if queue_size > 10:
            raise HTTPException(
                    status_code=429, detail="Request frequency too high (max 10 Hz)"
                )


    async def reset_frequency_after_delay(self):
        await asyncio.sleep(1)  
        self.frequency = 0  
