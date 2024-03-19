import pandas as pd

class RD:
    def __init__(self, config_):
        self.config = config_
    def _read_table(self):
        self.df = pd.read_csv('resource_files/r_d.csv')
    def _calculate_amortized(self):
        self.df['amortized_this_year'] = self.df.expense / self.config.years
        self.df.loc[0, 'amortized_this_year'] = 0
    def _calculate_adjustment(self):
        self.config.r_d_adjustment = self.df.loc[0, 'expense'] - self.df.amortized_this_year.sum()
        self.adjustment_tax = self.config.r_d_adjustment * self.config.tax_marginal
    def main(self):
        self._read_table()
        self._calculate_amortized()
        self._calculate_adjustment()