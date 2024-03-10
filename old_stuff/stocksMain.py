#main script for stock trades and logging
import stockData

oldPositions = getOldPositions()

currentPositions = getCurrentPositions()

predictions = getPredictions()

actions = getActions(preditions, currentPositions)

newerPositions = executeActions(actions)

updateData(newerPosition)
