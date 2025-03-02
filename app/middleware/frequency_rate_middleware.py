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
        self.last_request_time = None
   
    async def check_frequency(self):
        current_time = datetime.datetime.now().isoformat()

        if self.last_request_time:
            time_diff = (current_time - self.last_request_time).total_seconds()
            if time_diff < 1:
                self.frequency += 1
            if self.frequency > 1:
                raise HTTPException(
                    status_code=429, detail='Request frequency too low (min 1 Hz)'
                )

        else:
            self.frequency = 1
        

        self.last_request_time = current_time

        queue_size = await self.redis.llen(self.queue_key)
        print(f"Queue key: {self.queue_key}, Current queue size: {queue_size}")

        if queue_size > 10:
            raise HTTPException(
                    status_code=429, detail=f"Request frequency too high (max 10 Hz) {queue_size}"
                )
        
        await self.redis.delete(self.queue_key)