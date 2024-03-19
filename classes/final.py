import pandas as pd

class Final:
    def __init__(self, df: pd.DataFrame, config_):
        self.df_input = df
        self.config = config_
    def _calculate_value_end(self):
        self.end = self.df_input.loc[self.config.years_all]
        self.value_end = self.end.fcff / (self.end.cost_of_capital - self.end.growth)
    def _calculate_present(self):
        # Min = 2nd last value
        self.value_present = self.value_end * self.df_input.discount.min()
        self.fcff_present = self.df_input.fcff_present.sum()
        self.present = self.value_present + self.fcff_present
    def _calculate_fail(self):
        if self.config.fail_type == 'book':
            self.fail_value = self.config.book_equity + self.config.book_debt
        elif self.config.fail_type == 'present':
            self.fail_value = self.present
        else:
            raise ValueError(f'{self.config.fail_type} is an invalid fail type')
        self.fail_value *= self.config.fail_percentage
        self.present_fail = (
            self.present * (1 - self.config.fail_probability) + 
            self.fail_value * self.config.fail_probability
        )
    def _calculate_equity(self):
        self.debt = self.config.book_debt
        if self.config.debt_lease_tf:
            self.debt += self.config.lease_sum
        self.equity = self.present_fail - self.debt + self.config.cash
    def _calculate_share_price(self):
        self.equity_options = self.equity - self.config.options
        self.share_price = self.equity_options / self.config.share_count
    def main(self):
        self._calculate_value_end()
        self._calculate_present()
        self._calculate_fail()
        self._calculate_equity()
        self._calculate_share_price()