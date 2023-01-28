import sys
from counter.counter import Counter
from file.file import DataError


def _main(path: str) -> int:
    counter = Counter(path)
    print(counter.get_islands_count())
    return 0


def _path_provided(argv):
    return len(argv) > 1


def main(argv: list) -> int:
    if _path_provided(argv):
        try:
            return _main(sys.argv[1])
        except KeyboardInterrupt:
            print("\nProgram stopped")
            return 1
        except DataError:
            print("Something is wrong with your data. Please check it")
            return 1
        except IsADirectoryError:
            print("Please provide path to the file, not directory")
            return 1
    print("No path provided. Please run script with path param")
    return 1


if __name__ == '__main__':
    main(sys.argv)
