from classes import config, asserter, lease, r_d, df, df_columns, final

class Manager:
    def __init__(self):
        self.config = config.Config()
    def _run_asserter(self):
        self.asserter = asserter.Asserter(config_ = self.config)
        self.asserter.main()
    def _run_lease(self):
        self.lease = lease.Lease(config_ = self.config)
        self.lease.main()
    def _run_r_d(self):
        self.r_d = r_d.RD(config_ = self.config)
        self.r_d.main()
    def _run_df(self):
        self.df = df.DF(config_ = self.config)
        self.df.main()
    def _run_df_columns(self):
        self.df_columns = df_columns.DFColumns(df = self.df.df, config_ = self.config)
        self.df_columns.main()
    def _run_final(self):
        self.final = final.Final(df = self.df_columns.df, config_ = self.config)
        self.final.main()
    def main(self):
        self._run_asserter()
        self._run_lease()
        self._run_r_d()
        self._run_df()
        self._run_df_columns()
        self._run_final()