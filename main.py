import importlib
import os

from utils.log_utils import LoggingSystemDB
from utils.ranking import RankingSystemDB
from utils.testcase import TestCase

testcase = TestCase()
logging = LoggingSystemDB()
ranking = RankingSystemDB()


def run_algorithm_by_name(algorithm_name, testcase_file_name):
    try:
        module = importlib.import_module(f"algorithms.{algorithm_name}")
        func = getattr(module, "run_algorithm", None)

        if callable(func):
            print(f"Running {algorithm_name}...")
            testcase.run_testcase(
                algorithm_name=algorithm_name,
                func=func,
                testcase_file_name=testcase_file_name,
            )
        else:
            print(
                f"No valid 'run_algorithm' function found in {algorithm_name}.")
    except ModuleNotFoundError:
        print(f"Algorithm file '{algorithm_name}.py' not found.")


def run_all_algorithms(testcase_file_name):
    algorithm_folder = "./algorithms"
    for filename in os.listdir(algorithm_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            algorithm_name = filename[:-3]
            run_algorithm_by_name(
                algorithm_name=algorithm_name, testcase_file_name=testcase_file_name
            )


if __name__ == "__main__":
    # testcase_file_name = testcase.generate_testcase(
    #     testcase_num=10000, error_percent=10
    # )
    # testcase.display_testcase(testcase_file_name=testcase_file_name)
    # run_algorithm_by_name(
    #     algorithm_name="NLTT_1", testcase_file_name=testcase_file_name
    # )
    run_algorithm_by_name(algorithm_name='NLTT_1',
                          testcase_file_name='testcase_20241002_013436.json')
    # run_all_algorithms(testcase_file_name=testcase_file_name)
    ranking.display_ranks()
    logging.display_logs(answer_status='correct')
    pass
