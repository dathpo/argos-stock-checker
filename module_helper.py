import argparse
from signal import SIGINT, signal
from argos_scraper import ArgosScraper
from argos_stock_checker import ArgosStockChecker
from typing import NamedTuple


class ArgParserMock(NamedTuple):
    product_id: int
    postcode: str
    retry_count: int


def main(args):
    scraper = ArgosScraper(args.product_id)
    stock_checker = ArgosStockChecker(scraper, args.product_id, args.postcode)
    for i in range(int(args.retry_count)):
        print("\nNew search, product ID: {}, postcode: {}, retry count: {}".format(args.product_id, args.postcode,
                                                                                   args.retry_count))
        scraper.setup()
        if stock_checker.check_stock():
            break


def args_parser():
    signal(SIGINT, sigint_handler)
    arg_parser = argparse.ArgumentParser(description="Argos Stock Checker")
    arg_parser.add_argument("product_id", help="Argos product ID")
    arg_parser.add_argument("postcode", help="Postcode")
    arg_parser.add_argument("retry_count", help="Amount of runs for search")
    args = arg_parser.parse_args()
    return args


def sigint_handler(sig, frame):
    exit(2)


def lambda_handler(event, context):
    arg_parser_mock = ArgParserMock(1000000, "BN2 3PZ", 10)
    main(arg_parser_mock)
