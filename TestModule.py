import math
import random
import logging
import sys
from VEBTree import VEBTree
logging.basicConfig(stream = sys.stderr, level = logging.DEBUG)
MAXINT = 2**15
class VEBError(Exception):
	"""Base class for exceptions in this module.
	Attributes:
		message - explanation of the error
	"""
	def __init__(self, message: str = None):
		self.message = None
	pass
class VEBIncorrectValueError(VEBError):
	"""Exception raised for errors if vEB tree accepted incorrect value.
	
	Attributes:
        value 	- value which raised exception
	"""
	def __init__(self, value: int = None):
		self.value = value
		self.message = "VEBTree accepted incorrect value: {}".format(self.value)
class VEBUniversumError(VEBError):
	"""Exception raised for wrong initializing of universums.
	
	Attributes:
        rootUniversum 	- value which raised exception
		subTreeUniversum - 
	"""
	def __init__(self, rootUniversum: int = None, subTreeUniversum: int = None, rightUniversum: int = None):
		self.subTreeUniversum = subTreeUniversum
		self.rootUniversum = rootUniversum
		self.message = "VEBTree with {} universum has subtree with wrong {} universum. Subtree universum should be {}".format(self.rootUniversum, self.subTreeUniversum, rightUniversum)
class VEBClustersNumberError(VEBError):
	"""Exception raised for wrong quantity of clusters in the root vEB tree.
	
	Attributes:
        rootUniversum 	- value which raised exception
		subTreeUniversum - 
	"""
	def __init__(self, rootUniversum: int = None, clustersNumber: int = None, rightNumber: int = None):
		self.subTreeUniversum = subTreeUniversum
		self.rootUniversum = rootUniversum
		self.message = "VEBTree with {} universum has {} clusters. Quantity of clusters should be equal to {}".format(rootUniversum, clustersNumber, rightNumber)
class VEBInsertionError(VEBError):
	"""Exception raised for wrong insertion of the value.
	
	Attributes:
        value 	- value which raised exception
	"""
	def __init__(self, value: int = None):
		self.value = value
		self.message = "VEBTree could not insert value {}".format(self.value)
	"""Exception raised for wrong quantity of clusters in the root vEB tree.
	
	Attributes:
        rootUniversum 	- value which raised exception
		subTreeUniversum - 
	"""
	def __init__(self, rootUniversum: int = None, clustersNumber: int = None, rightNumber: int = None):
		self.subTreeUniversum = subTreeUniversum
		self.rootUniversum = rootUniversum
		self.message = "VEBTree with {} universum has {} clusters. Quantity of clusters should be equal to {}".format(rootUniversum, clustersNumber, rightNumber)
class VEBRemovingError(VEBError):
	"""Exception raised for wrong removing of the value.
	
	Attributes:
        value 	- value which raised exception
	"""
	def __init__(self, value: int = None):
		self.value = value
		self.message = "VEBTree could not remove value {}".format(self.value)
	
class TestModule(object):
	"""Module to test VEBTree
	Attributes:
		tree - VEBTree object which describes vEB tree
	"""
	def __init__(self, testObject = None):
		self.tree = testObject
	def testIncorrectValues(self, universum: int = None, totalTries: int = None) -> bool:
		"""Checks behaviour of the vEB on incorrect values (bigger than univesum or less than zero)
		Arguments:
					universum  - the size of the universum of the vEB tree
					totalTries - quantity of tries to insert incorrect values
		Return:
					True  - incorrect values were not inserted into the vEB tree
					False - incorrect value was inserted into the vEB tree
		"""
		self.tree.resetTree(universum)
		negTest = self._insertNegativeValues(totalTries)
		bigTest = self._insertTooBigValues(totalTries)
		return negTest and bigTest
	def _insertNegativeValues(self, totalTries: int = None) -> bool:
		"""Checks insertion of negative values into the vEB tree
		Arguments:
					totalTries - quantity of tries to insert incorrect values
		Return:
					True  - incorrect values were not inserted into the vEB tree
					False - incorrect value was inserted into the vEB tree
		"""
		if totalTries == None or totalTries == 0:
			totalTries = random.randint(2, self.tree.universum/2)
		for tryNumber in range(totalTries):
			randomValue = random.randint(-1*self.tree.universum, -1)
			try:
				if self.tree.insertValue(randomValue) == True:
					raise VEBIncorrectValueError(randomValue)
			except VEBIncorrectValueError as error:
				print(error.message)
				return False
		return True
	def _insertTooBigValues(self, totalTries: int = None) -> bool:
		"""Checks insertion of values greater than universum of the vEB tree
		Arguments:
					totalTries - quantity of tries to insert incorrect values
		Return:
					True  - incorrect values were not inserted into the vEB tree
					False - incorrect value was inserted into the vEB tree
		"""
		if totalTries == None or totalTries == 0:
			totalTries = random.randint(2, self.tree.universum/2)
		maxValue = MAXINT
		if MAXINT < self.tree.universum:
			maxValue = self.tree.universum + random.randint(self.tree.universum/4, self.tree.universum/2)
		for tryNumber in range(totalTries):
		
				
			randomValue = random.randint(self.tree.universum, maxValue)
			try:
				if self.tree.insertValue(randomValue) == True:
					raise VEBIncorrectValueError(randomValue)
			except VEBIncorrectValueError as error:
				print(error.message)
				return False
		return True
	def checkSubtree(self, tree: VEBTree) -> bool:
		"""Checks subtrees of the current tree
		Arguments:
					tree - vEB tree which should be checked
		Return:
					True  - if universum of some subtree matches universum of the parent tree
					False - if universum of some subtree does not match universum of the parent tree
		"""
		for subTree in tree.infoCluster:
			try:
				if subTree.universum != tree.sqrtUniversum():
					raise VEBUniversumError(tree.universum, subTree.universum, tree.sqrtUniversum())
			except VEBUniversumError as error:
				print (error.message)
				return False
			if subTree.universum > 2:
				self.checkSubtree(subTree)
		return True
	def testInitFunction(self, universum: int = None) -> bool:
		"""Checks correctness of the init functions
		Arguments:
					universum - the size of the universum of the vEB tree
		Return:
					True  - if initializing functions has successfully run
					False - if initializing functions has not successfully run
		"""
		if universum == None:
			universum = random.randint(2, MAXINT)
		self.tree = VEBTree(universum)
		if self.tree.universum % 2 != 0:
			return False
		try:
			if len(self.tree.infoCluster) != self.tree.sqrtUniversum(True):
				raise VEBClustersNumberError(self.tree.universum, len(self.tree.infoCluster), self.tree.sqrtUniversum(True))
		except VEBClustersNumberError as error:
			print (error.message)
			return False
		self.checkSubtree(self.tree)
		try:
			if self.tree.resume.universum != self.tree.sqrtUniversum(True):
				raise VEBUniversumError(self.tree.universum, self.tree.resume.universum, self.tree.sqrtUniversum(True))
		except VEBClustersNumberError as error:
			print ("Error during initializing summary cluster." + error.message)
			return False
		self.checkSubtree(self.tree.resume)
		return True
	def _testInsertValue(self, value: int) -> bool:
		"""Inserts 'value' into the vEB tree and checks whether it is placed correctly
		Arguments:
					value - number which should be inserted into the vEB tree
		Return:
					True  - if value was successfully inserted
					False - if value was not inserted
		"""
		self.tree.insertValue(value)	
		try:
			if self.tree.containsValue(value) == False:
				raise VEBInsertionError(value)
		except VEBInsertionError as error:
			print(error.message)
			return False
		clusterIndex = self.tree._high(value)
		try:
			if self.tree.getMin() != value and not self.tree.resume.containsValue(clusterIndex):
				raise VEBInsertionError(value)
		except VEBInsertionError as error:
			print("VEBTree could not update summary cluster after insertion value {}".format(error.value))
			return False
		return True
	def testInsertion(self, universum: int = None, randomInsert: bool = False, values: list = None) -> list:
		"""Inserts 'values' into the vEB tree with 'universum' size of the universum  
		Arguments:
					universum    - the size of the universum of the vEB tree
					randomInsert - flag which indicates how to insert values into the tree: with random order or not
					values       - values which should be inserted in the vEB tree
		Return:
					list of inserted values - if all values were successfully inserted
					empty list 				- if even one value was not inserted into the vEB tree
		"""
		self.tree.resetTree(universum)
		# insert whatever value to check whether it will be placed in min element of root VEBTree object
		if values == None:
			values = self._generateValues()
		if randomInsert == True:
			random.shuffle(values)
		for value in values:
			# Generated values can definitely be inserted into the tree
			if self._testInsertValue(value) == False:
				return list()
		return values
	def _generateValues(self, values: list = None) -> list:
		"""Generates list with random length in range[2, tree.universum) with random values [0,self.treeUniversum)
		Arguments:
					values - list with int values or None
		Return:
					list of random values in range [0, self.tree.universum				   - if 'values' was None
					list of all values which are not included in the values from universum - if 'values' was not None
		"""
		length = random.randint(2, self.tree.universum - 1)
		if values == None:
			values = []
			randomValue = 0
			for index in range(length):
				randomValue = random.randint(0, self.tree.universum - 1)
				if not (randomValue in values):
					values.append(randomValue)
		else:
			rightValues = values
			values = []
			allValues = list(range(0, self.tree.universum - 1))
			values = list(set(allValues) - set(rightValues))
		return values
	def testRemoving(self, universum: int = None, deleteValues: list = None) -> bool:
		"""Checks correctness of removing values from tree
		Arguments:
					universum - size of the universum of the vEB tree
					deleteValues - values which should be removed from the tree
		Return:
					True - if all values were successfully removed from the tree
					False - if even one value (which garanteed is in the tree) was not removed
		"""
		if deleteValues == None:
			self.tree.resetTree(universum)
			if deleteValues == None:
				deleteValues = self._generateValues()
			self.testInsertion(deleteValues)
		# Test removing values which are not in the tree
		testValues = self._generateValues(deleteValues)
		
		for value in testValues:
			try:
				#pdb.set_trace()
				if self.tree.removeValue(value) == True:
					raise VEBRemovingError(value)
			except VEBRemovingError as error:
				print("VEBTree somehow removed nonexisted {} value".format(error.value))
				#pdb.set_trace()
				return False
		for value in deleteValues:
			try:
				if self.tree.removeValue(value) == False:
					raise VEBRemovingError(value)
			except VEBRemovingError as error:
				print(error.message)
				return False
		return True

def test():
	testObj = TestModule()
	logging.debug("'Initializing' test has passed {}".format(testObj.testInitFunction()))
	logging.debug("'Incorrect Values Insertion' test has been passed successfully: {}".format(testObj.testIncorrectValues()))
	values = testObj.testInsertion(randomInsert = True)
	logging.debug("'Insertion' test has been passed successfully: {}".format(len(values) > 0))
	logging.debug("'Removing' test has been passed successfully: {}".format(testObj.testRemoving(deleteValues = values)))
test()