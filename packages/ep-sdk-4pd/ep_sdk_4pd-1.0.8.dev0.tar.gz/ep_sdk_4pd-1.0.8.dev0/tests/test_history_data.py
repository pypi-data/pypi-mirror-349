from ep_sdk_4pd.ep_data import EpData


def test_history_data():
    print('-------------test_history_data-------------')

    data = EpData.get_history_data(days=2)
    print(data)
    print('-------------------------------------')


if __name__ == '__main__':
    test_history_data()
