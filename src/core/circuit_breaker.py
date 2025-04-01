import logging
import time
from typing import Any, Callable

import pybreaker

logger = logging.getLogger('uvicorn')


class AsyncCircuitBreaker:
    def __init__(self, fail_max: int = 3, reset_timeout: int = 10):
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = 'closed'  # closed, open

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == 'open':
            current_time = time.time()
            if current_time - self.last_failure_time >= self.reset_timeout:
                logger.info('Circuit breaker: tempo de reset atingido, tentando fechar')
                self.state = 'closed'
                self.failure_count = 0
            else:
                logger.info(f'Circuit breaker aberto! Aguardando {self.reset_timeout}s para reset')
                raise pybreaker.CircuitBreakerError('Circuit breaker está aberto')

        try:
            result = await func(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.fail_max:
                self.state = 'open'
                logger.warning(f'Circuit breaker aberto após {self.failure_count} falhas')

            raise e
