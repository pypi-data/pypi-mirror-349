import numpy as np
import pandas as pd


def _rules_func(
    input_series: pd.Series,
    cl: pd.Series,
    lcl: pd.Series,
    ucl: pd.Series,
    rules_to_test_dict: dict[str, bool] = None,
) -> dict:
    """
    Set of five rules to test for process control.

    Inputs:
        - input_series (Pandas.Series): Target variable being tracked.
        - cl (Pandas.Series): Control line.
        - lcl (Pandas.Series): Lower control line.
        - ucl (Pandas.Series): Upper control line.
        - rules_to_test_dict (dict): Dictionary with rules being tested.

    Todo:
        - Optimsation around using pd.Series and taking subsets of the data to estimate sigma etc.

    """
    sigma = (
        ucl - cl
    ) / 3  # Calculate 1 sigma (Pandas.Series), based on upper control and center line
    violations = {}  # Store violations as dictionary (list of dates as values).

    # Rule 1: Point outside the +/- 3 sigma limits
    if rules_to_test_dict["Rule 1"]:
        rule1 = (input_series > ucl) | (input_series < lcl)
        violations["Rule 1 violation"] = input_series.index[rule1].tolist()

    # Rule 2: 8 successive consecutive points above (or below) the centre line
    if rules_to_test_dict["Rule 2"]:
        rule2 = []
        for i in range(7, len(input_series)):
            subset = input_series.iloc[i - 7 : i + 1]
            cl_subset = cl.iloc[i - 7 : i + 1]
            if (subset > cl_subset).all() or (subset < cl_subset).all():
                rule2.append(input_series.index[i])
        violations["Rule 2 violation"] = rule2

    # Rule 3: 6 or more consecutive points steadily increasing or decreasing
    if rules_to_test_dict["Rule 3"]:
        rule3 = []
        for i in range(5, len(input_series)):
            subset = input_series.iloc[i - 5 : i + 1]
            if np.all(np.diff(subset) > 0) or np.all(np.diff(subset) < 0):
                rule3.append(input_series.index[i])
        violations["Rule 3 violation"] = rule3

    # Rule 4: 2 out of 3 successive points beyond +/- 2 sigma limits
    if rules_to_test_dict["Rule 4"]:
        rule4 = []
        for i in range(2, len(input_series)):
            subset = input_series.iloc[i - 2 : i + 1]
            cl_subset = cl.iloc[i - 2 : i + 1]
            sigma_subset = sigma.iloc[i - 2 : i + 1]

            if ((subset > (cl_subset + 2 * sigma_subset)).sum() >= 2) or (
                (subset < (cl_subset - 2 * sigma_subset)).sum() >= 2
            ):
                rule4.append(input_series.index[i])
        violations["Rule 4 violation"] = rule4

    # Rule 5: 15 consecutive points within +/- 1 sigma on either side of the centre line
    if rules_to_test_dict["Rule 5"]:
        rule5 = []
        for i in range(14, len(input_series)):
            subset = input_series.iloc[i - 14 : i + 1]
            cl_subset = cl.iloc[i - 14 : i + 1]
            sigma_subset = sigma.iloc[i - 14 : i + 1]

            if np.all(
                np.abs(subset - cl_subset) <= (cl_subset + sigma_subset) - cl_subset
            ):
                rule5.append(input_series.index[i])
        violations["Rule 5 violation"] = rule5

    return violations
