from src.DataLoader import ShootingsDataLoader
from src.Cenus2019 import Census2019


def total_shootings(df):
    """

    Args:
        df (pandas.DataFrame):

    Returns:
        (tuple): counts, fraction, pop_fraction, per_million
            counts: Total shootings of each race.
            fraction: Each race's shootings as a fraction of the sum of counts.
            pop_fraction: Each race's population as a fraction of the total US population.
            per_million: Each race's shootings per million people of that race.
    """

    # Get counts for each race & total (sum) since we might be missing races not in RACE.items() (e.g. 'other')
    counts = dict()
    total = 0
    for k, v in ShootingsDataLoader.RACE.items():
        counts[k] = len(df[df['race'] == v])
        total += counts[k]

    # Get each race's contribution to the above total
    fraction = dict()
    for k, v in ShootingsDataLoader.RACE.items():
        fraction[k] = counts[k] / total

    # Get each race's portion of total population from Census data
    pop_fraction = dict()
    for k, v in Census2019.RACE.items():
        pop_fraction[k] = v / Census2019.TotalPopulation

    # Calculate each race's total shootings per million people using Census data
    per_million = dict()
    for k, v in Census2019.RACE.items():
        per_million[k] = counts[k] / (v / (1000 * 1000))

    return counts, fraction, pop_fraction, per_million
