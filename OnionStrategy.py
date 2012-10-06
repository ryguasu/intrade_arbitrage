from unittest import * 

# Looks for arbitrage opportunities for events with "nested
# probabilities". That is, finds trades where A entails B
# (ie B is at least as likely as A), but where B is priced less
# than A.
#
# Note: This hasn't been integrated into go.py yet.
class OnionStrategy:
	# dentifies the best tradeset currently available
	#
	# bidsList and asksList represent the bid/ask prices
	# for a set of contracts whose probabilities should
	# be in increasing order, logically speaking
	# Unlike some of the other strategies, bids/asks must be
	# sorted into logically increasing probability
	#
	# returns (trades, profit, principal)
	# trades is a (buy, sell), which are each lists.
	def arbitrage(self, bidsList, asksList):
		buy = sell = []
		profit = principal = 0

		for i in range(0, len(bidsList)):
			for j in range(i+1, len(bidsList)):
				# looking for cases where i's probability is higher than j's,
				# ie where i is overvalued and/or j is undervalued.
				# if it is, we want to consider selling i and buying j
				i_price = bidsList[i][1]
				j_price = asksList[j][1]

				#DEBUG helper:
				#print "i=%d (%f), j=%d (%f): i>j:%d" %(i, i_price, j, j_price, i_price > j_price)
				if i_price > j_price:
					# This is actually a profit floor.
					# We can potentially make this plus 10.
					testProfit = i_price - j_price
					if testProfit > profit:
						profit = testProfit
						sell = [ bidsList[i][0] ]
						buy = [ asksList[j][0] ]
						principal = 20

		return ( (buy,sell), profit, principal)

class TestProbsInOrder(TestCase):
	def runTest(self):
		bidsList = [ ("A",1), ("B",2), ("C",5) ]
		asksList = [ ("A",2), ("B",3), ("C",6) ]
		u = OnionStrategy()
		(trades, profit, principal) = u.arbitrage(bidsList, asksList)
		(buy, sell) = trades
		self.assertEqual(0, len(sell))
		self.assertEqual(0, len(buy))
		self.assertEqual(0, profit)
		self.assertEqual(0, principal)

# B is too high, so short it. (B is C2)
# C is too low, so go long (C is C1)
class TestProbsOnePairOutOfOrder(TestCase):
	def runTest(self):
		bidsList = [ ("A",1), ("B",5), ("C",2) ]
		asksList = [ ("A",2), ("B",6), ("C",3) ]
		u = OnionStrategy()
		(trades, profit, principal) = u.arbitrage(bidsList, asksList)
		(buy, sell) = trades
		self.assertTrue("B" in sell)
		self.assertEqual(1, len(sell))
		self.assertTrue("C" in buy)
		self.assertEqual(1, len(buy))
		self.assertEqual(5 - 3, profit)
		self.assertEqual(20, principal)

class TestProbsAllPairsOutOfOrder(TestCase):
	def runTest(self):
		bidsList = [ ("A",5), ("B",2), ("C",1) ]
		asksList = [ ("A",6), ("B",3), ("C",1.5) ]
		u = OnionStrategy()
		(trades, profit, principal) = u.arbitrage(bidsList, asksList)
		(buy, sell) = trades
		self.assertTrue("A" in sell)
		self.assertEqual(1, len(sell))
		self.assertTrue("C" in buy)
		self.assertEqual(1, len(buy))
		self.assertEqual(5 - 1.5, profit)
		self.assertEqual(20, principal)

if __name__ == "__main__":
	ts = TestSuite()
	ts.addTest(TestProbsInOrder())
	ts.addTest(TestProbsOnePairOutOfOrder())
	ts.addTest(TestProbsAllPairsOutOfOrder())
	TextTestRunner().run(ts)

