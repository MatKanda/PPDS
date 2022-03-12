"""
Nuclear power #2.

This is an example task from previous years tests. It's using
some sync techniques like lightswitch or barrier.

It requires "fei.ppds", "time" and "random" imports.
"""
from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep
from random import randint


class Lightswitch:
    """
    LightSwitch class shared between threads.
    Attributes
    ----------
    mutex: Mutex class used to lock/unlock
    counter: counter for number of threads that reached certain point of execution
    """
    def __init__(self):
        """
        Initialisation of LightSwitch class.
        """
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        """
        Lock method used to increment counter variable and return current
        count at the same time.

        Parameters:
        ----------
        semaphore: sync object Semaphore

        :param semaphore: sync object Semaphore

        Return value
        ------------
        counter: current counter value before incrementation

        :return counter: current counter value before incrementation
        """
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, semaphore):
        """
         Unlock method used to decrement counter variable and return current
         count at the same time.

         Parameters:
         ----------
         semaphore: sync object Semaphore

         :param semaphore: sync object Semaphore

         Return value
         ------------
         None
         """
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


def init():
    """
    Initialization function for testing purposes. Called by main() function.

    Return value
    ------------
    None
    """
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    valid_data = Event()

    for monitor_id in range(8):
        Thread(monitor, monitor_id, valid_data, turnstile, ls_monitor, access_data)

    Thread(sensor_p_t, 1, turnstile, ls_sensor, valid_data, access_data)
    Thread(sensor_p_t, 2, turnstile, ls_sensor, valid_data, access_data)
    Thread(sensor_h, 3, turnstile, ls_sensor, valid_data, access_data)


def monitor(monitor_id, valid_data, turnstile, ls_monitor, access_data):
    """
    Function simulating a monitoring some data that are being changed by other functions.

    Parameters
    ----------
    monitor_id: id of the current monitor
    valid_data: Event sync object
    turnstile: Semaphore sync object
    ls_monitor: LightSwitch class defined above
    access_data:Semaphore sync object

    :param monitor_id: id of the current monitor
    :param valid_data: Event sync object
    :param turnstile: Semaphore sync object
    :param ls_monitor: LightSwitch class defined above
    :param access_data:Semaphore sync object

    Return value
    ------------
    None
    """
    valid_data.wait()

    while True:
        turnstile.wait()
        reading_monitors = ls_monitor.lock(access_data)
        turnstile.signal()
        read_time = randint(40, 50) / 1000
        print(f'monit "{monitor_id}": pocet_citajucich_monitorov={reading_monitors}, trvanie_citana: {read_time}\n')
        sleep(read_time)
        ls_monitor.unlock(access_data)


def sensor_p_t(sensor_id, turnstile, ls_sensor, valid_data, access_data):
    """
    Function simulating the sensors updating/rewriting some data

    Parameters
    ----------
    sensor_id: id of the current sensor
    valid_data: Event sync object
    turnstile: Semaphore sync object
    ls_sensor: LightSwitch class defined above
    access_data:Semaphore sync object

    :param sensor_id: id of the current sensor
    :param valid_data: Event sync object
    :param turnstile: Semaphore sync object
    :param ls_sensor: LightSwitch class defined above
    :param access_data:Semaphore sync object

    Return value
    ------------
    None
    """
    while True:
        turnstile.wait()
        turnstile.signal()
        writing_sensors = ls_sensor.lock(access_data)
        write_time = randint(10, 20)/1000
        print(f'cidlo "{sensor_id}": pocet_zapisujucich_cidiel={writing_sensors}, trvanie_zapisu={write_time}\n')
        sleep(write_time)
        valid_data.signal()
        ls_sensor.unlock(access_data)


def sensor_h(sensor_id, turnstile, ls_sensor, valid_data, access_data):
    """
    Function simulating the sensors updating/rewriting some data

    Parameters
    ----------
    sensor_id: id of the current sensor
    valid_data: Event sync object
    turnstile: Semaphore sync object
    ls_sensor: LightSwitch class defined above
    access_data:Semaphore sync object

    :param sensor_id: id of the current sensor
    :param valid_data: Event sync object
    :param turnstile: Semaphore sync object
    :param ls_sensor: LightSwitch class defined above
    :param access_data:Semaphore sync object

    Return value
    ------------
    None
    """
    while True:
        turnstile.wait()
        turnstile.signal()
        writing_sensors = ls_sensor.lock(access_data)
        write_time = randint(20, 25) / 1000
        print(f'cidlo "{sensor_id}": pocet_zapisujucich_cidiel={writing_sensors}, trvanie_zapisu={write_time}\n')
        sleep(write_time)
        valid_data.signal()
        ls_sensor.unlock(access_data)