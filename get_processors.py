
def get_number_of_processors_running(processors: list) -> int:
    running_processes = 0
    for processor in processors:
        if processor.is_alive():
            running_processes += 1
    return running_processes


if __name__ == '__main__':
    pass
