from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep
from random import randint


class Lightswitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


def init():
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    valid_data = Event()

    for monitor_id in range(2):
        Thread(monitor, monitor_id, valid_data, turnstile, ls_monitor, access_data)
    for sensor_id in range(11):
        Thread(sensor, sensor_id, turnstile, ls_sensor, valid_data, access_data)


def monitor(monitor_id, valid_data, turnstile, ls_monitor, access_data):
    valid_data.wait()

    while True:
        sleep(.5)
        turnstile.wait()
        reading_monitors = ls_monitor.lock(access_data)
        turnstile.signal()
        print(f'monit "{monitor_id}": pocet_citajucich_monitorov={reading_monitors}\n')
        ls_monitor.unlock(access_data)


def sensor(sensor_id, turnstile, ls_sensor, valid_data, access_data):
    while True:
        turnstile.wait()
        turnstile.signal()
        writing_sensors = ls_sensor.lock(access_data)
        write_time = randint(10, 15)/1000
        print(f'cidlo "{sensor_id}": pocet_zapisujucich_cidiel={writing_sensors}, trvanie_zapisu={write_time}\n')
        sleep(write_time)
        valid_data.signal()
        ls_sensor.unlock(access_data)


if __name__ == "__main__":
    init()
