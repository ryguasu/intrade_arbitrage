import xml.etree.ElementTree
from xml.etree.ElementTree import ElementTree
import urllib2

# Fetch latest quotes from intrade, by market
# ID or other selectors.
#
# Note: For now we don't call
#  http://api.intrade.com/jsp/XML/MarketData/xml.jsp 
# but rather use a cached version from MarketData.xml.
# This is to avoid pissing off intrade when doing
# debug runs. But we still do call the live API
# to get the latest quotes for individual markets.
class IntradeQuoteFetcher(object):
	def __init__(self):
		self.symbol_id_map = {}

	def makeSymbolToIdMap(self):
		doc = ElementTree(file="MarketData.xml")
		for event in doc.findall(".//contract"):
			symbol = event.find("symbol").text
			id = event.get("id")
			self.symbol_id_map[symbol] = id

	def fetchByEventId(self, eventId):
		eventId = str(eventId)
		doc = ElementTree(file="MarketData.xml")
		symbols = []
		for event in doc.findall(".//Event"):
			if event.get("id") == eventId:
				for symbol in event.findall(".//contract/symbol"):
					symbols.append(symbol.text)

		return self.fetchBySymbols(symbols)

	# returns (id, name) pairs
	def fetchEventsByGroupId(self, eventGroupId):
		eventGroupId = str(eventGroupId)
		ids = []
		doc = ElementTree(file="MarketData.xml")
		for group in doc.findall(".//EventGroup"):
			if group.get("id") == eventGroupId:
				for event in group.findall(".//Event"):
					eventId = event.get("id")
					name = event.find(".//name").text
					ids.append( (eventId, name) )
		return ids

	def fetchBySymbols(self, symbols):
		self.makeSymbolToIdMap()

		bids = {}
		asks = {}

		url = "http://api.intrade.com/jsp/XML/MarketData/ContractBookXML.jsp?depth=1"
		for s in symbols:
			id = self.symbol_id_map[s]
			url += "&id=" + id

		openurl = urllib2.urlopen(url)
		data = openurl.read()
		
		mostRecentFile = open("most_recent.xml", "w+b")
		mostRecentFile.write(data)
		mostRecentFile.close()

		#doc = ElementTree()
		#doc.parse(openurl)
		doc = xml.etree.ElementTree.fromstring(data)
		# for now we're scaling all prices by 10, because
		# the API reports 0-100. I don't know what's up with
		# intrade's reporting prices in three different ways!
		for ci in doc.findall(".//contractInfo"):
			symbolNode = ci.find(".//symbol")
			if symbolNode == None:
				print "DEBUG: Contract id %s has no symbol. Ignoring it." % ci.get("conID")
				continue
			symbol = symbolNode.text
			bidNode = ci.find(".//bid")
			if bidNode != None:
				bidPrice = float(bidNode.get("price")) / 10.0
			else:
				bidPrice = None
			offerNode = ci.find(".//offer")
			if offerNode != None:
				offerPrice = float(offerNode.get("price")) / 10.0
			else:
				offerPrice = None

			bids[symbol] = bidPrice
			asks[symbol] = offerPrice

		return (bids, asks)

