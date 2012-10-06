from unittest import *
import itertools

# UnityStrategy looks for profit opportunities based on
# the rule that the probabilities of independent, exhaustive
# events must sum to 1.
class UnityStrategy:
	TOL = 0.01

	# identifies the best tradeset currently available
	# in the market given by bids and asks.
	#
	# bids and asks should be the bid/ask prices
	# for a set of independent, exhaustive events
	# (whose probabilities ought to sum to 1.)
	#
	# returns (trades, profit, principal)
	# trades is a (buy, sell), which are each lists.
	def arbitrage(self, bids, asks):
		bestBuyTrade = self.arbitrageBuy(asks)
		bestSellTrade = self.arbitrageSell(bids)

		buyProfit = bestBuyTrade[1]
		if buyProfit < UnityStrategy.TOL:
			buyProfit = 0

		sellProfit = bestSellTrade[1]
		if sellProfit < UnityStrategy.TOL:
			sellProfit = 0

		if buyProfit == sellProfit == 0:
			return (([], []), 0, 0)
		elif buyProfit > sellProfit:
			return bestBuyTrade
		else:
			return bestSellTrade

	def arbitrageBuy(self, asks):
		if None in asks.values():
			# If not all contracts have an ask price,
			# we can't guarantee a successful
			# arbitrage
			buy = []
			buyProfit = 0
			buyPrincipal = 0
		else:
			buy = asks.keys()
			buyProfit = 10 - sum(asks.values())
			buyPrincipal = self.principal(asks)
		sell = []
		return ((buy, sell), buyProfit, buyPrincipal)

	def arbitrageSell(self, bids):
		if None in bids.values():
			# For at least one contract, no one wants to take the other side.
			# But we can still short the remaining contracts if they sum to > 1.

			# Throw out the non-shortable contracts
			bids = dict(item for item in bids.iteritems() if item[1] != None)

		# Note: This is actually a profit floor. Potentially we've thrown out
		# the winning contract, in which case we won't have to buy it back.
		sellProfit = sum(bids.values()) - 10

		sellPrincipal = self.principal(bids)

		sell = bids.keys()
		buy = []

		return ((buy, sell), sellProfit, sellPrincipal)
			

	# contracts can be bids or asks.
	def principal(self, contracts):
		return 10 * len(contracts)

class TestArbitrageLow(TestCase):
	def runTest(self):
		bids = { "Obama" : 5, "Romney" : 4 }
		asks = { "Obama" : 5, "Romney" : 4.5 }
		u = UnityStrategy()
		(trades, profit, principal) = u.arbitrage(bids, asks)
		(buy, sell) = trades
		self.assertEqual(2, len(buy))
		self.assertTrue("Obama" in buy)
		self.assertTrue("Romney" in buy)
		self.assertEqual(0, len(sell))
		self.assertEqual(0.5, profit)
		self.assertEqual(20, principal)

class TestArbitrageHigh(TestCase):
	def runTest(self):
		bids = { "Obama" : 10, "Romney" : 10 }
		asks = { "Obama" : 11, "Romney" : 11 }
		u = UnityStrategy()
		(trades, profit, principal) = u.arbitrage(bids, asks)
		(buy, sell) = trades
		self.assertEqual(0, len(buy))
		self.assertTrue("Obama" in sell)
		self.assertTrue("Romney" in sell)
		self.assertEqual(2, len(sell))
		self.assertEqual(10, profit)
		self.assertEqual(20, principal)

class TestNoArbitrage(TestCase):
	def runTest(self):
		bids = { "Obama" : 5, "Romney" : 5 }
		asks = { "Obama" : 5, "Romney" : 5 }
		u = UnityStrategy()
		(trades, profit, principal) = u.arbitrage(bids, asks)
		(buy, sell) = trades
		self.assertEqual(0, len(buy))
		self.assertEqual(0, len(sell))
		self.assertEqual(0, profit)
		self.assertEqual(0, principal)

class TestArbitrageLowWithNone(TestCase):
	def runTest(self):
		bids = { "Obama" : 5, "Romney" : 5 }
		asks = { "Obama" : 5, "Romney" : None }
		u = UnityStrategy()
		(trades, profit, principal) = u.arbitrage(bids, asks)
		(buy, sell) = trades
		self.assertEqual(0, len(buy))
		self.assertEqual(0, len(sell))
		self.assertEqual(0, profit)
		self.assertEqual(0, principal)

class TestArbitrageHighWithNone1(TestCase):
	def runTest(self):
		bids = { "Obama" : 5, "Romney" : None}
		asks = { "Obama" : 5, "Romney" : 5}
		u = UnityStrategy()
		(trades, profit, principal) = u.arbitrage(bids, asks)
		(buy, sell) = trades
		self.assertEqual(0, len(buy))
		self.assertEqual(0, len(sell))
		self.assertEqual(0, profit)
		self.assertEqual(0, principal)

class TestArbitrageHighWithNone2(TestCase):
	def runTest(self):
		bids = { "Obama" : 11, "Romney" : None}
		asks = { "Obama" : 5, "Romney" : 5}
		u = UnityStrategy()
		(trades, profit, principal) = u.arbitrage(bids, asks)
		(buy, sell) = trades
		self.assertTrue("Obama" in sell)
		self.assertEqual(1, len(sell))
		self.assertEqual(0, len(buy))
		self.assertEqual(1, profit)
		self.assertEqual(10, principal)

class TestArbitrageHighWithNone3(TestCase):
	def runTest(self):
		bids = { "A" : None, "B" : 6, "C" : 5 }
		asks = { "A" : 4, "B" : 5, "C" : 1 }
		u = UnityStrategy()
		(trades, profit, principal) = u.arbitrage(bids, asks)
		(buy, sell) = trades
		self.assertTrue("B" in sell)
		self.assertTrue("C" in sell)
		self.assertEqual(2, len(sell))
		self.assertEqual(0, len(buy))
		self.assertEqual(1, profit)
		self.assertEqual(20, principal)

if __name__ == '__main__':
	ts = TestSuite()
	ts.addTest(TestArbitrageLow())
	ts.addTest(TestArbitrageHigh())
	ts.addTest(TestNoArbitrage())
	ts.addTest(TestArbitrageLowWithNone())
	ts.addTest(TestArbitrageHighWithNone1())
	ts.addTest(TestArbitrageHighWithNone2())
	ts.addTest(TestArbitrageHighWithNone3())
	TextTestRunner().run(ts)

