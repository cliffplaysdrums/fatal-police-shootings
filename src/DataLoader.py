import pandas as pd
import numpy as np
from os import path
import os


class ShootingsDataLoader:

    ARMED = {
        'unarmed': 0,
        'unknown': 1,
        'undetermined': 2,
        'toy weapon': 3,
        'unknown weapon': 4,
        'claimed to be armed': 4,
        'stapler': 4,
        'nail gun': 4,
        'screwdriver': 4,
        'wrench': 4,
        'walking stick': 4,
        'cordless drill': 4,
        'metal hand tool': 4,
        'contractor\'s level': 4,
        'blunt object': 4,
        'air conditioner': 4,
        'rock': 4,
        'piece of wood': 4,
        'brick': 4,
        'motorcycle': 4,
        'vehicle': 4,
        'pellet gun': 4,
        'BB gun': 4,
        'BB gun and vehicle': 4,
        'pepper spray': 4,
        'wasp spray': 4,
        'fireworks': 4,
        'air pistol': 4,
        'Airsoft pistol': 4,
        'pen': 4,
        'barstool': 4,
        'chain': 4,
        'chair': 4,
        'garden tool': 4,
        'metal rake': 4,
        'oar': 4,
        'flashlight': 4,
        'shovel': 5,
        'pitchfork': 5,
        'baton': 5,
        'scissors': 5,
        'glass shard': 5,
        'beer bottle': 5,
        'bottle': 5,
        'metal pipe': 5,
        'pipe': 5,
        'metal stick': 5,
        'carjack': 5,
        'pole': 5,
        'crowbar': 5,
        'pick-axe': 5,
        'metal pole': 5,
        'flagpole': 5,
        'bean-bag gun': 5,
        'baseball bat': 5,
        'baseball bat and bottle': 5,
        'tire iron': 5,
        'baseball bat and fireplace poker': 5,
        'crossbow': 6,
        'hammer': 6,
        'spear': 6,
        'bayonet': 6,
        'metal object': 6,
        'box cutter': 6,
        'straight edge razor': 6,
        'sharp object': 6,
        'ice pick': 6,
        'hand torch': 6,
        'incendiary device': 6,
        'bow and arrow': 7,
        'hatchet': 7,
        'meat cleaver': 7,
        'knife': 7,
        'car, knife and mace': 7,
        'baseball bat and knife': 7,
        'pole and knife': 7,
        'sword': 7,
        'samurai sword': 7,
        'machete': 7,
        'vehicle and machete': 7,
        'ax': 7,
        'chain saw': 7,
        'chainsaw': 7,
        'lawn mower blade': 7,
        'Taser': 7,
        'gun': 8,
        'gun and knife': 8,
        'hatchet and gun': 8,
        'machete and gun': 8,
        'gun and machete': 8,
        'gun and sword': 8,
        'gun and car': 8,
        'gun and vehicle': 8,
        'vehicle and gun': 8,
        'guns and explosives': 8,
        'grenade': 8
    }

    @staticmethod
    def convert_armed(armed):
        if armed in ShootingsDataLoader.ARMED:
            return ShootingsDataLoader.ARMED[armed]
        elif armed is None:
            return 1  # same as 'unknown'
        elif len(armed) == 0:
            return 1
        else:
            raise ValueError('Got unexpected value for armed: {}'.format(armed))

    GENDER = {
        'None': 0,
        'M': 1,
        'F': 2
    }

    @staticmethod
    def convert_gender(gender):
        if gender in ShootingsDataLoader.GENDER:
            return ShootingsDataLoader.GENDER[gender]
        elif gender is None or gender == '':
            return 0
        else:
            raise ValueError(f'Unexpected value for gender: "{gender}" ({type(gender)})')

    RACE_FULL_NAMES = ['White', 'Black', 'Asian', 'Native American', 'Hispanic']

    RACE = {
        'W': 0,
        'B': 1,
        'A': 2,
        'N': 3,
        'H': 4,
        #'O': 5
    }

    @staticmethod
    def convert_race(race, as_str=False):
        if race in ShootingsDataLoader.RACE:
            if as_str:
                return race
            else:
                return ShootingsDataLoader.RACE[race]
        elif race == 'O':
            return None
        elif race is None or len(race) == 0:
            if as_str:
                return None
            else:
                # return ShootingsDataLoader.RACE['None']
                return None
        else:
            raise ValueError('Got unexpected value for race: {}'.format(race))

    @staticmethod
    def int_to_race(num):
        for k, v in ShootingsDataLoader.RACE.items():
            if v == num:
                return k
        raise Exception(f'Integer for race category should be between 0 & {len(ShootingsDataLoader.RACE.items())}')

    THREAT_LEVEL = {
        'undetermined': 0,
        'other': 1,
        'attack': 2
    }

    @staticmethod
    def convert_threat_level(level):
        if level in ShootingsDataLoader.THREAT_LEVEL:
            return ShootingsDataLoader.THREAT_LEVEL[level]
        else:
            raise ValueError(f'Unexpected value for threat level: {level}')

    FLEE = {
        'Not fleeing': 0,
        'Other': 1,
        'Foot': 2,
        'Car': 3
    }

    @staticmethod
    def convert_flee(flee):
        if flee in ShootingsDataLoader.FLEE:
            return ShootingsDataLoader.FLEE[flee]
        elif flee is None or len(flee) == 0:
            return ShootingsDataLoader.FLEE['Other']
        else:
            raise ValueError(f'Unexpected value for flee: {flee}')

    @staticmethod
    def convert_age(age):
        if age is None:
            return 0
        elif len(age) < 1:
            return 0
        else:
            return round(int(age) / 10)

    COLUMNS_USED = [4, 5, 6, 7, 10, 11, 12, 13]
    COLUMN_NAMES = ['id', 'name', 'date', 'manner_of_death', 'armed', 'age', 'gender', 'race', 'city', 'state',
                    'signs_of_mental_illness', 'threat_level', 'flee', 'body_camera']

    def __init__(self):
        self.__converters = {
            4: self.__class__.convert_armed,
            5: self.__class__.convert_age,
            6: self.__class__.convert_gender,
            7: self.__class__.convert_race,
            10: lambda tf: 1 if tf == 'True' else 0,
            11: self.__class__.convert_threat_level,
            12: self.__class__.convert_flee,
            13: lambda tf: 1 if tf == 'True' else 0
        }

    def get_data(self, train_frac=.75, as_df=False, shuffle=False, random_seed=1):
        """Gets the data!

        Args:
            train_frac (float): Fraction (0 to 1) to reserve for training (as opposed to testing).
            as_df (bool): Whether to return pandas DataFrames (True) or numpy arrays (False).
            shuffle (bool): Shuffle the data before returning.
            random_seed (int): Seed the shuffle function for reproducibility.

        Returns:
            Depends on ``as_df``. If True, returns a tuple of DataFrames (train set, test set). If False, returns a
            tuple of numpy arrays (training features, training labels, test features, test labels).
        """
        dirname = os.path.dirname(__file__)
        filepath = path.join(dirname, '..', 'data-police-shootings', 'fatal-police-shootings-data.csv')
        df = pd.read_csv(filepath, usecols=self.COLUMNS_USED, converters=self.__converters)
        df.dropna(inplace=True)
        if shuffle:
            df = df.sample(random_state=random_seed, frac=1)  # Shuffle data

        train_size = int(df.shape[0] * train_frac)
        if as_df:
            train_df = df.iloc[:train_size, :]
            test_df = df.iloc[train_size:, :]
            return train_df, test_df
        else:
            data = df.to_numpy()
            train_targets = data[:train_size, 3]  # 4th column is our target
            train_features = data[:train_size, [0, 1, 2, 4, 5, 6, 7]]  # everything else is a feature

            test_targets = data[train_size:, 3]  # 4th column is our target
            test_features = data[train_size:, [0, 1, 2, 4, 5, 6, 7]]  # everything else is a feature

            return train_features, train_targets, test_features, test_targets
