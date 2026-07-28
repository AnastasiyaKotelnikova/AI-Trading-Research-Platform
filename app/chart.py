"""
Stock Chart Module
Creates interactive trading charts.
"""

import plotly.graph_objects as go


def create_candlestick_chart(
    history,
    symbol,
    trade=None
):

    fig = go.Figure()


    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=history.index,
            open=history["Open"],
            high=history["High"],
            low=history["Low"],
            close=history["Close"],
            name=symbol
        )
    )


    # SMA 20
    if "SMA20" in history.columns:

        fig.add_trace(
            go.Scatter(
                x=history.index,
                y=history["SMA20"],
                name="SMA 20"
            )
        )


    # SMA 50
    if "SMA50" in history.columns:

        fig.add_trace(
            go.Scatter(
                x=history.index,
                y=history["SMA50"],
                name="SMA 50"
            )
        )


    # Trade levels
    if trade is not None:

        for level, name in [
            ("Entry", "Entry"),
            ("Stop_Loss", "Stop Loss"),
            ("Target_1", "Target 1"),
            ("Target_2", "Target 2")
        ]:

            if level in trade.index:

                fig.add_hline(
                    y=float(trade[level]),
                    annotation_text=name
                )


    fig.update_layout(
        title=f"{symbol} Technical Chart",
        xaxis_rangeslider_visible=False,
        height=600
    )


    return fig
