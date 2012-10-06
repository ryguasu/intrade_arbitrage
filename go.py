import Quotes
import UnityStrategy

# Actually evaluate some concrete markets, looking
# for arbitrage opportunities

def evalMarket(marketName, quotes):
	(bids, asks) = quotes
	print "EVALUATING MARKET: %s" % marketName
	us = UnityStrategy.UnityStrategy()
	print "DEBUG bids: ",
	print bids
	print "DEBUG sum(available bids): ",
	print "%.20f" % sum([val for val in bids.values() if val != None])
	print "DEBUG asks: ",
	print asks
	print "DEBUG sum(available asks): ",
	print "%.20f" % sum([val for val in asks.values() if val != None])

	(trades, profit, principal) = us.arbitrage(bids, asks)

	(buy, sell) = trades
	if not (len(buy) == len(sell) == 0):
		print "Trades:"
		for b in buy:
			print "\tBuy " + b
		for s in sell:
			print "\tSell " + s
		print "profit: %f" % profit
		print "principal: %f" % principal
		if principal != 0:
			print "ROI: %f" % (profit / principal)
	else:
		print "No profitable trades"
	print ""

iqf = Quotes.IntradeQuoteFetcher()

def evalMarketByEventId(marketName, eventId):
	return evalMarket(marketName, iqf.fetchByEventId(eventId))

def evalEventGroupId(eventGroupId):
	print "*** BEGIN EVALUATING EVENT GROUP %s ***" % str(eventGroupId)
	for (eventId, eventName) in iqf.fetchEventsByGroupId(eventGroupId):
		evalMarketByEventId(eventName, eventId)
	print "*** END EVALUATING EVENT GROUP %s ***" % str(eventGroupId)

presidentialIndividualQuotes = iqf.fetchBySymbols(["2012.PRES.OBAMA", "2012.PRES.ROMNEY", "2012.PRES.PAUL(RON)", "2012.PRES.CLINTON", "2012.PRES.HUCKABEE", "2012.PRES.JOHNSON", "2012.PRES.SANTORUM", "2012.PRES.BIDEN", "2012.PRES.GINGRICH", "2012.PRES.PALIN", "2012.PRES.CHRISTIE", "2012.PRES.DANIELS", "2012.PRES.BLOOMBERG", "2012.PRES.TRUMP", "2012.PRES.HUNTSMAN", "2012.PRES.THUNE", "2012.PRES.CAIN", "2012.PRES.PERRY", "2012.PRES.BACHMANN", "2012.PRES.BARBOUR", "2012.PRES.PAWLENTY", "2012.PRES.OTHER"]) 
evalMarket("Individual President", presidentialIndividualQuotes)

presidentialPartyQuotes = iqf.fetchBySymbols(["PRESIDENT.DEM.2012", "PRESIDENT.REP.2012", "PRESIDENT.OTHER.2012"])
evalMarket("President Party", presidentialPartyQuotes)

evalMarket("Republican Candidate", iqf.fetchByEventId(84328))

evalMarket("Republican VP", iqf.fetchByEventId(90482))

evalMarket("Democrat Candidate", iqf.fetchByEventId(84329))

evalMarket("Democrat VP", iqf.fetchByEventId(90015))

evalMarket("2012 Senate Control", iqf.fetchByEventId(84331))

evalMarket("2012 House Control", iqf.fetchByEventId(84330))

evalMarket("President-Congress Combination after 2012 Elections", iqf.fetchByEventId(91194))

evalMarketByEventId("Last named storm of 2012 Atlantic Hurricane Season (1 Jun - 30 Nov)", 91294)

evalMarketByEventId("Who will be the next US Supreme Court Justice to retire or resign from the Court?", 90289)


# event *groups*!

evalEventGroupId(9725) # US Primaries

evalEventGroupId(9704) # 2012 US States

evalEventGroupId(9705) # 2012 US Senate Races

evalEventGroupId(9705) # US Governors

evalEventGroupId(9731) # Endorcements

# NOTE: other groups one could add are "UK Politics" and "Mexican politics"

