from telegram.error import TimedOut

from feedback_bot.retry import TelegramTimedOutRetry


class RaiseTimeout:
    def __init__(self, n_times_timeout=1):
        self.n_times_timeout = n_times_timeout

    def __call__(self, **kwargs):
        if self.n_times_timeout > 0:
            self.n_times_timeout -= 1
            raise TimedOut()
        else:
            return 1


def test_timeout():
    f = RaiseTimeout()
    retry = TelegramTimedOutRetry(1, f, {})
    assert retry.retry() == 1
