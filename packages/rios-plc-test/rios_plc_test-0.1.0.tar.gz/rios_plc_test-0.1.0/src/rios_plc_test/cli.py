import time
import logging
import argparse

from pycomm3 import LogixDriver
from pycomm3.exceptions import CommError

logger = logging.getLogger("rios-plc-test")

def run_loop(host, tag):
    with LogixDriver(host, init_tags=True, init_program_tags=False) as plc:
        while True:
            try:
                result = plc.read(tag)
                logger.info(result)
                time.sleep(1)
            except CommError as e:
                logger.exception(e)
                return e
            except Exception as e:
                logger.exception(e)
                return e

def main():
    parser = argparse.ArgumentParser(description="A simple PLC tool.")
    parser.add_argument("host", help="PLC host")
    parser.add_argument("tag", help="PLC tag")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s]: %(message)s"
    )

    iteration = 1
    while True:
        error = run_loop(args.host, args.tag)
        iteration += 1
        logging.error(f"Lost connection to PLC ({error}). Reconnecting in 5 seconds.")
        time.sleep(5)

