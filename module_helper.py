import argparse
from signal import SIGINT, signal


def args_parser():
    signal(SIGINT, sigint_handler)
    arg_parser = argparse.ArgumentParser(description="Argos Stock Checker")
    arg_parser.add_argument("product_id", help="Argos product ID")
    arg_parser.add_argument("postcode", help="Postcode")
    arg_parser.add_argument("retry_count", help="Amount of runs for search")
    args = arg_parser.parse_args()
    return args


def sigint_handler(sig, frame):
    """
    ISR to handle the Ctrl-C combination and stop the program in a clean way
    """
    exit(2)
