class Config:
    def __init__(self):
        self._all()
        self._lease()
        self._r_d()
        self._df_master()
        self._df_other()
        self._final()
    def _all(self):
        self.years = 5
        self.years_all = self.years * 2 + 1
    def _lease(self):
        self.credit_rating = 'Ba2/BB'
        self.lease_start = 275.65
        self.lease_end = 477.9
        self.lease_tf = False
        # lease_adjustment, lease_sum added by lease
    def _r_d(self):
        self.r_d_start = 3005
        self.r_d_tf = True
        # r_d_adjustment added by r_d
    def _df_master(self):
        # Start
        self.growth_start = 0.24
        self.cost_capital_start = 0.0965 * 2/3 + 0.1116 * 1/3
        self.sales_capital_start = 4
        # End (margin start is derived)
        self.margin_target = 0.16
    def _df_other(self):
        # Start
        self.ebit_net = 13656
        self.revenue_start = 81462
        self.tax_marginal = 0.25
        # End
        self.tax_effective = 0.1
        # Masters' End
        self.risk_free = 0.0347
        self.cost_capital_end = 0.09
        self.sales_capital_end = self.sales_capital_start * 2/3
    def _final(self):
        # Fail
        self.book_equity = 41124
        self.book_debt = 5874
        self.fail_percentage = 0.5
        self.fail_probability = 0
        self.fail_type = 'present'
        # Equity
        self.debt_lease_tf = False
        self.cash = 21107
        # Share price
        self.options = 36769.41
        self.share_count = 3146