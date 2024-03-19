import optuna
from classes import manager

class Optimizer:
    def _objective(self, trial):
        self.model = manager.Manager()
        self.model.config.growth_start = trial.suggest_float('growth_start', 0.02, 0.28)
        self.model.config.margin_target = trial.suggest_float('margin_target', 0.03, 0.21)
        self.model.config.sales_capital_start = trial.suggest_float('sales_capital_start', 0.75, 4.0)
        self.model.config.cost_capital_start = trial.suggest_float('cost_capital_start', 0.06, 0.11)
        self.model.main()
        return self.model.final.equity
    def main(self, direction):
        self.direction = direction
        self.study = optuna.create_study(direction = self.direction)
        self.study.optimize(self._objective, n_trials=200)
