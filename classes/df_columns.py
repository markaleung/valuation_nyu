import pandas as pd

class DFColumns:
    def __init__(self, df: pd.DataFrame, config_):
        self.df_input = df
        self.df = df.copy()
        self.config = config_
    def _calculate_ebit(self):
        self.df['ebit'] = self.df_input.revenue * self.df_input.margin
        self.after_tax = (1 - self.df_input.tax)
        self.df['ebit_after_tax'] = self.df.ebit * self.after_tax
    def _calculate_sales_capital(self):
        self.nan = [float('nan')]
        self.first = [self.config.sales_capital_start] * self.config.years
        self.second = [self.config.sales_capital_end] * self.config.years
        self.df['sales_to_capital_ratio'] = self.nan + self.first + self.second + self.nan
    def _calculate_reinvestment(self):
        '''
        reinvestment
        = capital * revenue % change
        = capital * revenue diff / total revenue
        = revenue diff * (capital / sales)
        = revenue diff / (sales / capital)
        '''
        self.df['reinvestment'] = self.df_input.revenue.diff() / self.df.sales_to_capital_ratio
        years = self.config.years_all
        self.df.loc[years, 'reinvestment'] = self.df_input.loc[years, 'growth'] * self.df.loc[years, 'ebit_after_tax'] / 0.18
    def _calculate_fcff(self):
        self.df['fcff'] = self.df.ebit_after_tax - self.df.reinvestment
        self.df['fcff_present'] = self.df.fcff * self.df_input.discount
    def main(self):
        self._calculate_ebit()
        self._calculate_sales_capital()
        self._calculate_reinvestment()
        self._calculate_fcff()