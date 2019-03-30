from threading import Thread
from typing import List, Union
from sys import argv
from itermark import Itermark
import time


# Table writing object, designed to read a specific list and write them as new entries are added
#  by continuously checking target list
class AsidePrint:
    """
    Asynchronous Object Printer class. Feed items to async_print and it will print them out
    with/without numerical indicators. Best used to offload stdout functionality to a single
    thread/remove printing function from a highly repetitive loop
    """
    def __init__(self, queue: list=None, header: list=None, include_index=False,
                 target_list=None, tabler_is_writing=None, tabler_queue=None, running=None, ):

        if not queue:
            queue = ['']
        print(queue)
        self.queue = Itermark(queue)
        print(self.queue)

        self.header = header if header else []

        self.include_index = include_index

        self.table_is_running = False

        self.writing_to_queue = False

        self.behind = False

    def start(self):
        """Start AsidePrint"""
        self.queue.mark = 0
        self.table_is_running = True

    def pause(self):
        """Pause printing. Can resume where left off"""
        self.table_is_running = False

    def resume(self):
        self.table_is_running = True

    def stop(self):
        """Stops asoprint, clears queue, resets bookmark to 0, preserves header"""
        self.table_is_running = False
        self.queue.mark.clear()

    def restart(self):
        """Stops and starts asoprint function (resets bookmark, clears queue, preserves header)"""
        self.start()
        self.start()

    def append(self, item: any):
        """
        Add an item to queue, akin to a list.append() This should be the primary way to add new
        items to print
        """
        # queue[-1] is None to match buffer (last item will not print due to [-1] index never == len

        self.writing_to_queue = True

        old = True

        if old:
            self.queue.append(item)

        if not old:
            if self.queue.__len__() == 1:
                self.queue.append(item)
            else:
                self.queue[-1] = item
            self.queue.append(None)

        self.writing_to_queue = False

    @property
    def _caughtup(self):
        """"""
        try:
            return self.queue.mark + 1 == len(self.queue)
        except TypeError:
            return True

    def run(self):
        """Start asoprint"""
        try:
            self.table_is_running = True
            t_inst = Thread(target=self._run)  # , args=(self.target_list,))
            t_inst.start()
        except Exception as err:
            print('Unable to start!')
            print(err)

    @staticmethod
    def _stdout(out):
        """
        Funnel fun for displaying items

        Args:
            out: item/s to print
        """
        print(out)

    def _run(self):
        # print(('#', 'IP', 'Server Name'))
        print('_running')

        if self.header is not None:
            self._stdout(self.header)

        try:
            # write initial
            self._stdout(self.queue.active)
            while self.table_is_running:

                # Make sure table is not being written to...
                if not self.writing_to_queue:
                    self.queue.mark += 1
                    self._stdout(self.queue.active)

                    while self._caughtup:
                        # x = self._caughtup
                        time.sleep(.5)

                    time.sleep(.25)

        except KeyboardInterrupt:
            self.stop()
        except Exception as err:
            print("*" * 20)
            print("Error: ", err)


if __name__ == '__main__':
    aside = AsidePrint()
    aside.start()
