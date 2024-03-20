# Introduction
- This is my adaptation of [Aswath Damodaran's](https://pages.stern.nyu.edu/~adamodar/) [November 2023 Tesla valuation](https://aswathdamodaran.substack.com/p/tesla-in-november-2023-story-twists)
- He is a finance professor at New York University's [Stern School of Business](https://www.stern.nyu.edu)
- Here is the [Excel Spreadsheet](https://pages.stern.nyu.edu/~adamodar/pc/blog/Tesla2023OctDIY.xlsx) that the program is based on
- I added a feature to optimize the model given the master input constraints, using [Optuna](https://optuna.org)

# How to

## Install this Repository
- Install python
- `pip install -r requirements.txt`

## Run This Repository (notebooks folder)
- notebook_valuation: run manager with adjustable master inputs
- notebook_optimizer: get maximum and minimum valuations
    - max is 800+ billion, min is negative
- notebook_visualizer: see importance of master inputs
    - target margin and start growth are the most important

# Notes
- I skipped the option derivation (final._calculate_share_price), because I didn't understand it

## Simplified Logic
- Revenue follows growth
    - Ebit = revenue * margin
    - Reinvestment = revenue diff * (capital / sales)
    - FCFF = ebit - reinvestment
- Discount follows cost of capital
    - Annuity = terminal FCFF / (cost of capital - risk free)
    - Present value = annuity + discounted FCFF
    - Adjust present value for failure
- Equity = present value - debt + cash
## What is the Difference Between Max and Min Valuation?
- FCFF (Ebit - reinvestment) is lower
    - Ebit (revenue * margin) is lower
        - Target margin is lower
    - Reinvestment (revenue growth / (sales/capital)) is higher
        - Sales/capital is lower
    - Main determinant of valuation is FCFF
## Start and End Values
- Cost of capital: start* -> end
- Growth: start* -> risk free rate
- Margin: income/revenue -> target*
- Sales Capital Ratio: start* -> 2/3 of start 
- Tax: marginal -> effective
- \* means the value is a master input

# Trees

## Module Tree
- optimizer: finds max/min valuation (optional)
    - manager: runs everything
        - lease: to add to operating income (optional)
        - r_d: to add to operating income (optional)
        - df: some columns must be calculated by year
        - df_columns: other columns can be vectorised
        - final: df -> share price
## Function Tree (Excluding Optimizer)
- manager._run_lease()
    - lease._calculate_cost_of_debt(): risk free + credit spread
    - lease._read_table()
    - lease._discount_commitments(): Present value of future commitments
    - lease._calculate_end_commitment(): end spread out to same size as average
    - lease._calculate_end_present(): end -> discounted annuity
    - lease._calculate_adjustment(): first lease - annual depreciation
- manager._run_r_d()
    - r_d._read_table()
    - r_d._calculate_amortized(): expense / # years
    - r_d._calculate_adjustment(): first expense - annual amortization
- manager._run_df()
    - df._initialize_ebit(): add r_d and lease to ebit_net
    - df._initialize_variables(): revenue follows growth, discount follows cost of capital
    - df._initialize_convergers(): margin, growth, tax, cost of capital converge
    - df._append_variables(): 
    - for df.index in range(df.config.years_all):
        - df._update_variables()
        - df._append_variables()
    - df._make_df()
- manager._run_df_columns()
    - df_columns._calculate_ebit(): (after tax) income
    - df_columns._calculate_sales_capital(): start -> end
    - df_columns._calculate_reinvestment(): capital * revenue% change
    - df_columns._calculate_fcff(): ebit after tax - reinvestment
- manager._run_final()
    - final._calculate_value_end(): terminal cash flow -> annuity
    - final._calculate_present(): add discounted cash flows
    - final._calculate_fail(): adjust for chance of failure
    - final._calculate_equity(): adjust for debt, cash
    - final._calculate_share_price(): subtract options, divide by # shares

