import pandas as pd

class Lease:
    def __init__(self, config_):
        self.config = config_
    def _calculate_cost_of_debt(self):
        self.credit_ratings = pd.read_csv('resource_files/credit_rating.csv')
        self.spread = self.credit_ratings.query('Rating == @self.config.credit_rating').Spread.values[0]
        self.cost_of_debt = self.config.risk_free + self.spread
    def _read_table(self):
        self.lease = pd.read_csv('resource_files/lease.csv')
    def _discount_commitments(self):
        self.lease.index += 1
        self.lease['discount'] = (1 + self.cost_of_debt) ** self.lease.index
        self.lease['present_value'] = self.lease.commitment / self.lease.discount
    def _calculate_end_commitment(self):
        self.years_extra = self.config.lease_end / self.lease.commitment.mean()
        self.years_extra = round(self.years_extra)
        self.end_commitment = self.config.lease_end / self.years_extra
    def _calculate_end_present(self):
        self.end_annuity = self.end_commitment * (1 - (1 + self.cost_of_debt) ** (-self.years_extra)) / self.cost_of_debt
        self.end_present = self.end_annuity / self.lease.discount.values[-1]
    def _calculate_adjustment(self):
        self.config.lease_sum = self.lease.present_value.sum() + self.end_present
        self.years_total = len(self.lease) + self.years_extra
        self.depreciation = self.config.lease_sum / self.years_total
        self.config.lease_adjustment = self.config.lease_start - self.depreciation
    def main(self):
        self._calculate_cost_of_debt()
        self._read_table()
        self._discount_commitments()
        self._calculate_end_commitment()
        self._calculate_end_present()
        self._calculate_adjustment()
