from src.DataLoader import ShootingsDataLoader
from src.Cenus2019 import Census2019


def print_race_counts(df):
    """

    Args:
        df (pandas.DataFrame):

    Returns:

    """
    print('Fatal shootings by race:')
    counts = dict()
    total = 0
    for k, v in ShootingsDataLoader.RACE.items():
        counts[k] = len(df[df['race'] == v])
        total += counts[k]

    for k, v in ShootingsDataLoader.RACE.items():
        fraction = counts[k] / total
        print(f'\t{k}: {counts[k]} ({100 * fraction:.2f}%)')

    print('Population by race (2019):')
    for k, v in Census2019.RACE.items():
        fraction = v / Census2019.TotalPopulation
        print(f'\t{k}: {100 * fraction:.2f}% of US population')

    print('Fatal shootings per million by race:')
    for k, v in Census2019.RACE.items():
        per_million = counts[k] / (v / (1000 * 1000))
        print(f'\t{k}: {round(per_million)} per million killed')