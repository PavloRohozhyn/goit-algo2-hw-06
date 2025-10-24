import json
import time
from hyperloglog import HyperLogLog

"""
Extract IP addr from log file
"""
def extract_ips(path_to_logfile: str):
    with open(path_to_logfile, 'r', encoding='utf-8') as file:
        for row in file:
            try:
                data = json.loads(row)
                ip = data.get("remote_addr")
                if ip:
                    yield ip
            except json.JSONDecodeError:
                continue

"""
Exact. counting
"""
def exact_counting(ip_iterable):
    ip_set = set(ip_iterable)
    return len(ip_set)


"""
Approx. counting (HyperLogLog - 0.01 - its like 1%)
"""
def approx_counting(ip_iterable):
    res = HyperLogLog(0.01)
    for ip in ip_iterable:
        res.add(ip)
    return len(res)

if __name__ == "__main__":
    ips = list(extract_ips("./lms-stage-access.log")) # get ip(s)
    start = time.time() # profiling start
    exact_result = exact_counting(ips) # exact
    exact_time = time.time() - start # profiling end
    start = time.time() # profiling start
    hll_result = approx_counting(ips) # approx.
    hll_time = time.time() - start # profiling end
    print("Результати порівняння:")
    print(f"{'':<30}{'Точний підрахунок':<20}{'HyperLogLog'}")
    print(f"{'Унікальні елементи':<30}{exact_result:<20}{hll_result}")
    print(f"{'Час виконання (сек.)':<30}{exact_time:<20.5f}{hll_time:.5f}")