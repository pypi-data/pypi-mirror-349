volatility_filter =f"""
%s
r_vol = rank(ts_std_dev(returns, 10));
enter_cond = if_else(r_vol > 0.5, 1, -1);
trade_when(enter_cond, %s, -1)
"""

def reduce_turnover(expr: str, final_factor: str):
    """
    Reduce turnover by adding volatility filter
    Effective for price-volume based factors
    :param expr: origin factor expression
    :param final_factor: name of the final factor
    :return:
    """
    return volatility_filter % (expr, final_factor)


if __name__ == "__main__":
    expr0 = "a = rank(((-1 * returns) * ts_mean(volume, 20) * (high - low)));"
    print(reduce_turnover(expr0, "a"))