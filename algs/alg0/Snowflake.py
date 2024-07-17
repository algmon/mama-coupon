import time
import threading

class Snowflake:
    def __init__(self, datacenter_id=0, worker_id=0):

        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = 0
        self.lock = threading.Lock()

        # Twitter的Snowflake算法起始时间戳(2014-01-01)
        self.twepoch = 1388534400000
        self.worker_id_bits = 5
        self.datacenter_id_bits = 5
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        self.sequence_bits = 12

        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_left_shift = self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

        self.last_timestamp = -1

    def _til_next_millis(self, last_timestamp):
        timestamp = time.time_ns() // 1000000  # 转换为毫秒
        while timestamp <= last_timestamp:
            timestamp = time.time_ns() // 1000000
        return timestamp

    def _next_id(self):
        with self.lock:
            timestamp = time.time_ns() // 1000000
            if self.last_timestamp == timestamp:
                self.sequence = (self.sequence + 1) & self.sequence_mask
                if self.sequence == 0:
                    timestamp = self._til_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            if timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards. Refusing to generate id for %d milliseconds" % (self.last_timestamp - timestamp))

            self.last_timestamp = timestamp

            return ((timestamp - self.twepoch) << self.timestamp_left_shift) | \
                   (self.datacenter_id << self.datacenter_id_shift) | \
                   (self.worker_id << self.worker_id_shift) | \
                   self.sequence


    def generate(self):

        return self._next_id()

if __name__ == "__main__":
    snowflake = Snowflake(datacenter_id=1, worker_id=3)
    for i in range(10):
        print(snowflake.generate())

