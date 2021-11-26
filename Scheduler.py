import sched
import time


class Scheduler:
    def __init__(self):
        self.s = sched.scheduler(time.time, time.sleep)
        self.active_tasks = {}

    def set_handler_for_n_second(self, handler, n_sec, priority):
        def run():
            handler()
            self.s.enter(n_sec, priority, run, )

        act = self.s.enter(n_sec, priority, run, )
        if n_sec not in self.active_tasks:
            self.active_tasks[n_sec] = []
        self.active_tasks[n_sec].append(act)

    def run(self):
        self.s.run()

    # def do_every_n_second(self):
    #     print("store and clean last minute tweets")
    #     imb.store_last_minute_tweets()
    #     imb.clear_last_minute_tweets()
    #     s.enter(60, 2, do_every_one_minute, )
    #
    # s.enter(request_rate_in_sec, 1, read_and_store_tweets, )
    # s.enter(60, 2, do_every_one_minute, )
