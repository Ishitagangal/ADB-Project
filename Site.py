import os
import sys
import time
import Variable
import constants
from DataManager import DataManager
from Transaction import Transaction


class Site:
	"""
	Site instance.
	status: If the site is up, down or is in recovery state
	id: Index of the site
	variables: list of variables it stores
	SiteDataManager: data managaer instance for site
	foundVariables : list of variables this site has written/can access after failure

	Authors: Ishita Gangal and Divya Juneja
	Date: 18th November, 2019
	"""
	def __init__(self, id):
		self.site_id = id
		self.variables = []
		self.site_status = constants.SiteStatus.UP
		self.SiteDataManager = self.getDataManager(self.site_id)
		self.foundVariables = set()

	def getSiteID(self):
		"""
		Returns site id
		:return: site id
		"""
		return self.site_id

	def getStatus(self):
		"""
		Returns site status
		:return: site status
		"""
		return self.site_status

	def setStatus(self, status):
		"""
		Set site status
		:param status: status to be set to
		"""
		if status in constants.SiteStatus:
			self.site_status = status
		else:
			print("Invalid site status")
		return

	def setFail(self):
		"""
		Set site status to fail
		"""
		self.site_status = constants.SiteStatus.DOWN

	def setRecover(self):
		"""
		Set site status to recover
		"""
		self.site_status = constants.SiteStatus.RECOVERING

	def getDataManager(self, id):
		"""
		Getter for data manager instance
		:param id: id of site
		:return: data manager of this site id
		"""
		return DataManager(id)

	def acquireLockOnSite(self, transaction, type, variable):
		"""
		Tried to acquire a lock on the site
		:param transaction: transaction requesting lock
		:param type: type of lock being requested read or write
		:param variable: variable on which lock is requested
		:return: True if acquired else False
		"""
		if self.SiteDataManager.acquireLock(transaction, type, variable):
			self.foundVariables.add(variable)
			if len(self.foundVariables) == len(self.SiteDataManager.variables):
				self.setStatus(constants.SiteStatus.UP)
			return True
		return False

	def releaseLockOnSite(self, lock, variable):
		"""
		Releases lock for variable
		:param lock: lock object to be released
		:param variable: variable on which this lock is present
		"""
		self.SiteDataManager.releaseLock(lock, variable)

	def writeVariable(self, transaction, variable, value):
		"""
		Writes variable onto site
		:param transaction: transaction doing the writing
		:param variable: variable to be written
		:param value: new value of variable
		"""
		if self.site_status != constants.SiteStatus.DOWN and variable in self.foundVariables:
			self.SiteDataManager.writeVariableForTransaction(transaction, variable, value)

	def fail(self):
		"""
		Called when site fails
		Set transaction state to aborted if it used this site
		"""
		self.setFail()
		self.foundVariables = set()
		lockTable = self.SiteDataManager.getLockTable()
		lockDict = lockTable.get_lockDict()

		for variable, locks in lockDict.items():
			for l in locks:
				print("Transaction "+l.transaction.name+ " has been aborted due to site "+str(self.site_id)+" failure")
				l.transaction.setTransactionState(constants.TransactionState.aborted)

	def recover(self):
		"""
		Called when site recovers
		Sets status to recovering
		"""
		for variable in self.SiteDataManager.variables.keys():
			if int(variable[1:]) % 2 !=0:
				self.foundVariables.add(variable)
		self.setStatus(constants.SiteStatus.RECOVERING)

	def dump(self):
		"""
		Called when dump() is called in site manager.
		Prints all values of all variables on this site
		"""
		if self.site_status == constants.SiteStatus.DOWN:
			print("Site " + str(self.site_id) + " is down")
			return
		print("Variables on site "+str(self.site_id)+" are :", end = " ")
		variablesToPrint = self.getVariablesOnThisSite()
		for var in variablesToPrint:
			print(var.name+" :"+ str(var.value)+",", end = " ")
		# print("\n")
		# for i in list(self.SiteDataManager.variables):
		# 	variable = self.SiteDataManager.variables[i]

	def getVariablesOnThisSite(self):
		"""
		Returns list of variables present on this site
		:return: list of variables
		"""
		variables = list()
		for index in list(self.SiteDataManager.variables):
			variable = self.SiteDataManager.variables[index]
			variables.append(variable)
		return variables





