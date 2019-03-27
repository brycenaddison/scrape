import time
import os


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


class ProgressBar:

    current_time = lambda: int(round(time.time() * 1000))

    def __init__(self, prefix="", suffix=""):
        self.total = 0
        self.iteration = 0
        self.prefix = prefix
        self.suffix = suffix
        self.is_running = False
        self.last_iteration = 0

    def update(self, stream, chunk, file_handle, bytes_remaining):
        self.is_running = True
        if bytes_remaining > self.total:
            self.total = bytes_remaining
        self.iteration = self.total - bytes_remaining

    def get_percent(self):
        return 100 * (self.iteration / float(self.total))

    @staticmethod
    def convert_ms(millis: int):
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24
        if minutes % 10 == minutes:
            minutes = "0" + str(minutes)
        if hours % 10 == hours:
            hours = "0" + str(int(hours))
        if seconds % 10 == seconds:
            seconds = "0" + str(seconds)
        return "%s:%s:%s" % (str(hours), str(minutes), str(seconds))

    def print_progress(self, start_time, decimals=1, length=100, fill='='):
        """
        Call in a loop to create terminal progress bar
        @params:
            start_time  - Required  : time started in ms (Int)
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        if not self.last_iteration == self.iteration:
            if self.iteration == 0:
                eta = 0
            else:
                eta = (self.total - self.iteration) * (__class__.current_time() - start_time) / self.iteration
            eta = __class__.convert_ms(eta)
            percent = ("{0:." + str(decimals) + "f}").format(100 * (self.iteration / float(self.total)))
            filled_length = int(length * self.iteration // self.total)
            bar = fill * filled_length + '-' * (length - filled_length)
            print('\r' + ' ' * 100, end='\r')
            print('\r%s |%s| %s%% %s %s %s/%s' % (
            self.prefix, bar, percent, self.suffix, eta, self.iteration, self.total), end='\r')
            if self.iteration == self.total:
                print()
                self.is_running = False
            self.last_iteration = self.iteration

    def in_progress(self):
        return self.is_running
