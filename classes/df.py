import pandas as pd

class DF:
    def __init__(self, config_):
        self.config = config_
    def _calculate_ebit_start(self):
        self.ebit_start = self.config.ebit_net
        if self.config.r_d_tf:
            self.ebit_start += self.config.r_d_adjustment
        if self.config.lease_tf:
            self.ebit_start += self.config.lease_adjustment
    def _calculate_variables(self):
        # Others
        self.revenue = self.config.revenue_start
        self.discount = 1
        self.df = []
        # First Half
        self.margin = self.ebit_start / self.revenue
        self.margin_change = (self.margin - self.config.margin_target) / self.config.years
        # Second Half
        self.growth = self.config.growth_start
        self.growth_change = (self.growth - self.config.risk_free) / self.config.years
        self.tax = self.config.tax_effective
        self.tax_change = (self.config.tax_marginal - self.config.tax_effective) / self.config.years
        self.cost_capital = self.config.cost_capital_start
        self.cost_capital_change = (self.cost_capital - self.config.cost_capital_end) / self.config.years
    def _append_variables(self):
        self.df.append({
            'growth': self.growth, 
            'revenue': self.revenue, 
            'margin': self.margin, 
            'tax': self.tax, 
            'cost_of_capital': self.cost_capital, 
            'discount': self.discount
        })
    def _update_variables(self):
        # First half: margin converges
        if self.index < self.config.years:
            self.margin -= self.margin_change
        # Second half: tax, growth, cost of capital converge
        if self.config.years <= self.index < self.config.years * 2:
            self.growth -= self.growth_change
            self.tax += self.tax_change
            self.cost_capital -= self.cost_capital_change
        self.revenue *= (1 + self.growth)
        self.discount /= (1 + self.cost_capital)
    def _make_df(self):
        self.df = pd.DataFrame(self.df)
        self.df.loc[self.config.years_all, 'discount'] = float('nan')
    def main(self):
        self._calculate_ebit_start()
        self._calculate_variables()
        self._append_variables()
        for self.index in range(self.config.years_all):
            self._update_variables()
            self._append_variables()
        self._make_df()
