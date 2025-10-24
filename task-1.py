import hashlib
import bitarray


class BloomFilter:
    def __init__(self, size=1000, hash_count=3):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray.bitarray(size)
        self.bit_array.setall(0)

    def _hashes(self, item):
        """Повертає список хешів для переданого елемента"""
        item = item.encode('utf-8')
        return [
            int(hashlib.md5(item + bytes([i])).hexdigest(), 16) % self.size
            for i in range(self.hash_count)
        ]

    def add(self, item):
        """Додає елемент до фільтра"""
        for idx in self._hashes(item):
            self.bit_array[idx] = 1

    def contains(self, item):
        """Перевіряє, чи є елемент у фільтрі"""
        return all(self.bit_array[idx] for idx in self._hashes(item))


def check_password_uniqueness(passwords, bloom_filter):
    """
    Приймає список паролів і повертає список результатів перевірки:
    True – якщо пароль унікальний (не використовувався раніше),
    False – якщо ймовірно вже використовувався.
    Некоректні значення вважаються неунікальними (False).
    """
    results = []
    for pwd in passwords:
        if not isinstance(pwd, str) or not pwd.strip():
            results.append(False)
            continue
        if bloom_filter.contains(pwd):
            results.append(False)
        else:
            bloom_filter.add(pwd)
            results.append(True)
    return results


# tests:
if __name__ == "__main__":
    bloom = BloomFilter(size=5000, hash_count=5)
    passwords = [
        "password123", 
        "123456", 
        "helloWorld", 
        "", 
        None, 
        "password123", 
        "HELLOworld"
    ]
    results = check_password_uniqueness(passwords, bloom)
    for pwd, res in zip(passwords, results):
        print("{:<20} {:<50}".format(f"'{pwd}'", "-> Унікальний" if res else "-> Вже використовувався або некоректний"))
