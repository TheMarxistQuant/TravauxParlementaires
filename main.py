from src import DataLoading

if __name__ == "__main__":
    leg = DataLoading.LegislatureEnum.XVI
    legislature_data = DataLoading.get_all_legislature_data(leg, force_download=False)