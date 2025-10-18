import time

text = "ny"

# 10 - число пробелов, которые появятся по сторонам от переменной
print(f"|{text:<10}|")
# Можно заменить на любой символ
print(f"|{text:=^10}|")


print()
for i in range(11):
    print(f"\r[{'='*i:<10}]", end="", flush=True)
    time.sleep(0.05)

# \r - возвращает курсор в начало строки
# flush - не изучено

print('\n\n')


# пример, как делать загрузку, пока выполняется функция
import time
import threading

def loading(func):
    def wrapper(*args, **kwargs):
        def spinner():
            frames = ['-', '\\', '|', '/']
            i = 0
            while not done.is_set():
                print(f'\rЗагрузка... {frames[i % 4]}', end='', flush=True)
                i += 1
                time.sleep(0.1)

        done = threading.Event()  # Event to stop the spinner
        spinner_thread = threading.Thread(target=spinner)
        spinner_thread.start()

        # Execute the wrapped function
        result = func(*args, **kwargs)

        # Stop the spinner
        done.set()
        spinner_thread.join()

        return result

    return wrapper

# Long-running function
@loading
def long_process():
    time.sleep(1)  # Simulate a long task
    return "Task finished!"

print(long_process())
