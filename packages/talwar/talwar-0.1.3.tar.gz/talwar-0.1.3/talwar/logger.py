import logging
from colorama import Fore, Style, init

# Initialize colorama
init()

class Logger:
    colors = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'blue': Fore.BLUE,
        'yellow': Fore.YELLOW,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'black': Fore.BLACK,
        'light_red': Fore.LIGHTRED_EX,
        'light_green': Fore.LIGHTGREEN_EX,
        'light_blue': Fore.LIGHTBLUE_EX,
        'light_yellow': Fore.LIGHTYELLOW_EX,
        'light_magenta': Fore.LIGHTMAGENTA_EX,
        'light_cyan': Fore.LIGHTCYAN_EX,
        'light_white': Fore.LIGHTWHITE_EX,
        'dim': Style.DIM,
        'normal': Style.NORMAL,
        'bright': Style.BRIGHT
    }

    def __init__(self, name='app'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        # Remove any existing handlers to prevent duplicates
        self.logger.handlers = []
        # Add a single handler
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        # Prevent propagation to root logger
        self.logger.propagate = False

    def info(self, message, color='white'):
        color_code = self.colors.get(color, Fore.WHITE)
        self.logger.info(f"{color_code}{message}{Style.RESET_ALL}")
        
    def warning(self, message):
        self.logger.warning(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
        
    def error(self, message, color='red'):
        color_code = self.colors.get(color, Fore.RED)
        self.logger.error(f"{color_code}{message}{Style.RESET_ALL}")
        
    def debug(self, message):
        self.logger.debug(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
