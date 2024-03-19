class Asserter:
    def __init__(self, config_):
        self.config = config_
    def _assert(self, variable_names, low, high):
        for self.variable_name in variable_names:
            self.variable = eval(f'self.config.{self.variable_name}')
            assert low <= self.variable <= high, f'{self.variable_name}: {low} <= {self.variable} <= {high}'
    def _all(self):
        self._assert(['years'], 0, 10)
    def _lease(self):
        self._assert(['lease_start', 'lease_end'], 0, 10000)
    def _r_d(self):
        self._assert(['r_d_start'], 0, 10000)
    def _df_master(self):
        # These reflect Aswath Damodaran's assumptions
        self._assert(['growth_start'], 0.0, 0.3)
        self._assert(['margin_target'], -0.2, 0.3)
        self._assert(['sales_capital_start'], 0.0, 5.0)
        self._assert(['cost_capital_start'], 0.05, 0.12)
    def _df_other(self):
        self._assert(['tax_marginal', 'tax_effective', 'risk_free', 'cost_capital_end'], 0, 0.3)
    def _final(self):
        self._assert(['book_equity', 'book_debt', 'cash', 'options', 'share_count'], 0, 100000)
        self._assert(['fail_percentage', 'fail_probability'], 0, 1)
    def main(self):
        self._all()
        self._lease()
        self._r_d()
        self._df_master()
        self._df_other()
        self._final()
