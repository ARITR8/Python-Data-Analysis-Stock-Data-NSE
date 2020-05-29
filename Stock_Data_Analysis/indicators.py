class indicators:

    def sma(self, data, window):
        """
        Calculates Simple Moving Average
        http://fxtrade.oanda.com/learn/forex-indicators/simple-moving-average
        """
        if len(data) < window:
            return None
        return sum(data[-window:]) / float(window)

    def ema(self, data, window, position=None, previous_ema=None):
        """
        Calculates Exponential Moving Average
        http://fxtrade.oanda.com/learn/forex-indicators/exponential-moving-average
        """
        if len(data) < window + 2:
            return None
        c = 2 / float(window + 1)
        if not previous_ema:
            return self.ema(data, window, window, self.sma(data[-window*2 + 1:-window + 1], window))
        else:
            current_ema = (c * data[-position]) + ((1 - c) * previous_ema)
            if position > 0:
                return self.ema(data, window, position - 1, current_ema)
            return previous_ema

p = indicators()
