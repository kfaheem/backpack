from cProfile import Profile
import pstats


def some_func(foo, bar):
    """

    :param foo:
    :param bar:
    :return:
    """
    try:
        profile1 = Profile()
        profile1.enable()  # to measure only a part of a function
        result = foo + bar
        profile1.disable()
        stats1 = pstats.Stats(profile)
        stats.print_stats()
        return result

    except Exception as exception:
        raise exception


def main():
    """

    :return:
    """
    try:
        some_func(10, 20)

    except Exception as exception:
        raise exception

# measure performance of a full function


profile = Profile()
profile.runcall(main)
stats = pstats.Stats(profile)
stats.print_stats()
stats.sort_stats()

