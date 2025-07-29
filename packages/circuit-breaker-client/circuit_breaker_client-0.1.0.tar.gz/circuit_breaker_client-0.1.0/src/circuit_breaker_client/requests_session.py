import time

import requests


class CircuitBreakerSession(requests.Session):
    def __init__(self, failure_threshold=3, recovery_timeout=30):
        super().__init__()
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self._failure_count = 0
        self._circuit_open = False
        self._last_failure_time = None

    def request(self, method, url, **kwargs):
        # Check circuit breaker state
        if self._circuit_open:
            if time.time() - self._last_failure_time < self.recovery_timeout:
                raise RuntimeError("Circuit is open. Request blocked.")
            else:
                # Try again after cooldown
                self._circuit_open = False
                self._failure_count = 0

        try:
            response = super().request(method, url, **kwargs)
            response.raise_for_status()
            # Success → reset state
            self._failure_count = 0
            return response
        except Exception as e:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                self._circuit_open = True
                self._last_failure_time = time.time()
                print(f"[Circuit Breaker] Opened circuit after {self._failure_count} failures.")
            raise e
