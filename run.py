from analysis.points_analysis import process_data, analyse_data, load_qualifying_data


if __name__ == '__main__':
    data = process_data()
    analyse_data(data, load_qualifying_data())