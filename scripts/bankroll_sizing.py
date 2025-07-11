def bankroll_sizing(
    df_stats,
    bankroll,
    order_pct_min=0.03,
    order_pct_max=0.05,
    min_roi=0.10,
    max_days_to_fill=3,
    use_fee_adjusted_roi=True
):
    """
    Filter EVE Online market items for trading based on ROI, liquidity, order sizing, and speed.

    Parameters:
        df_stats: DataFrame with avg_lowest, avg_highest, avg_daily_volume, type_id, type_name, and 'roi' column
        bankroll: Your total ISK (int or float)
        order_pct_min: Minimum percent of bankroll to allocate per item (0.03 = 3%)
        order_pct_max: Maximum percent of bankroll to allocate per item (0.05 = 5%)
        min_roi: Minimum ROI required (0.10 = 10%)
        max_days_to_fill: Maximum days you want your order to fill in
        use_fee_adjusted_roi: Use the 'roi' column (if True) or recalculate gross ROI (if False)

    Returns:
        Filtered DataFrame with key columns
    """
    # ISK order sizes
    min_order_size = order_pct_min * bankroll
    max_order_size = order_pct_max * bankroll

    df = df_stats.copy()
    df['isk_volume_daily'] = df['avg_daily_volume'] * df['avg_lowest']
    df['days_to_fill_min'] = min_order_size / df['isk_volume_daily']
    df['days_to_fill_max'] = max_order_size / df['isk_volume_daily']

    # Choose ROI column
    roi_col = 'roi' if use_fee_adjusted_roi else 'roi_gross'
    if roi_col not in df.columns:
        df['roi_gross'] = (df['avg_highest'] - df['avg_lowest']) / df['avg_lowest']

    # Filtering
    filtered = df[
        (df[roi_col] >= min_roi) &
        (df['isk_volume_daily'] >= min_order_size) &
        (df['days_to_fill_min'] <= max_days_to_fill)
    ].sort_values('isk_volume_daily', ascending=False)

    # Columns to show
    cols_to_show = [
        'type_id', 'type_name', 'avg_lowest', 'avg_highest', roi_col,
        'avg_daily_volume', 'isk_volume_daily', 'days_to_fill_min', 'days_to_fill_max'
    ]
    return filtered[cols_to_show]
