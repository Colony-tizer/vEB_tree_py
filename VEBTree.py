import math
class VEBTree(object):
	"""Class describes vEB tree
	Attributes:
		universum	- maximum value which can be stored in the vEB tree; universum should be the result of raising 2 to a power
		_minElement	- stores the least element in the tree; minElement does not appear in any cluster
		_maxElement	- stores the biggest element in the tree; maxElement is placed in its cluster
		resume 		- vEB tree which contains information about status of the clusters (whether they are empty or not)
		infoCluster - vEB tree which contains information about presence of the values in the vEB tree
	"""
	def displayContent(self, clusterNum: int = -1) -> None:
		"""Prints information about VEBTree object 
		Prints max and min elements, the size of the universum and same information about daughter trees
		Arguments:
					clusterNum - index of the cluster of the root tree
		"""
		if clusterNum == -1:
			print("u: {}".format(self.universum))
			print("min: {}\tmax: {}".format(self.getMin(), self.getMax()))
			if self.infoCluster != None:
				line = ""
				for index, cluster in enumerate(self.infoCluster):
					if cluster != None:
						line += "Cluster no.{}| u = {}| min: {}\tmax: {}\n".format(index, cluster.universum, cluster.getMin(), cluster.getMax())
				print(line)
		else:
			self.infoCluster[clusterNum].displayContent()
	def _isValueValid(self, value: int) -> bool:
		"""Checks whether value is valid or not (greater or equals zero and less than universum)
		Arguments:
					value - int value
		Return: 
					True	- if value is valid
					False 	- if value is not valid
		"""
		if value == None or type(value) != int or value >= self.universum or value < 0 :
			return False
		return True
	def _fixUniversum(self) -> None:
		"""Fixes the universum value if it was not the result of raising 2 to a power
		"""
		if self.universum < 2:
			self.universum = 2
		module = self._log2(self.universum) % 2
		power = 0
		if module != 0:
			power = math.ceil(self._log2(self.universum))
			self.universum = 2**power
	def _log2(cls, value: int) -> float:
		"""Calculates log with base of 2
		"""
		return math.log(value, 2)
	def sqrtUniversum(self, roundingUp: bool = False) -> int:
		"""Calculates so-called "square of the universum"
		"square of the universum" is a codename for the formula 2^(lg2(u)/2)
		Arguments:
					roundingUp - flag indicates whether rounding should be up or down
		Return: 
					int - square of the universum
		This if help(?) function
		"""
		roundedValue = self._log2(self.universum)/2
		if roundingUp == True:
			roundedValue = int(math.ceil(roundedValue))
		else:
			roundedValue = int(math.floor(roundedValue))
		return 2**roundedValue
	def _high(self, value: int ) -> int:
		"""Calculates index of cluster, which contains asked value
		Arguments:
					value - int value
		Return: 
					int - index of the cluster
		"""
		return int(math.floor(value/self.sqrtUni)) 
	def _low(self, value: int) -> int:
		"""Calculates index of requested value in the cluster
		Arguments:
					value - int value
		Return: 
					int - index of the value in the cluster
		"""
		return value % self.sqrtUni
	def _index(self, clusterNumber: int, valueNumber: int) -> int:
		"""Calculates number which contains in the index [valueNumber] in the [clusterNumber]th cluster
		Arguments:
					clusterNumber - index of the cluster
					valueNumber   - index of the number in the cluster
		Return: 
					int - value which contains in the given index in the cluster with given index
		"""
		return clusterNumber * self.sqrtUni + valueNumber
	def _initResumes(self, fill:bool = False) -> None:
		""" Initializes summary cluster of VEBTree object"""
		# If universum equals 2 than VEBTree object does not require summary cluster
		if self.universum == 2:
			self.resume = None
		elif fill == True:
			# In other case VEBTree object needs summary cluster
			self.resume = VEBTree(self.sqrtUniversum(True), fill)
	def _initCluster(self, fill:bool = False) -> None:
		"""Initializes cluster section of VEBTree object"""
		# If universum equals 2 than given VEBTree object is the base vEB tree
		# Which contains only two members (both are numbers) and are stored in the min and max elements
		if self.universum == 2:
			self.infoCluster = None
		else:
			# If universum is greater than 2
			# Then VEBTree object is required to create the list of clusters 
			# The length of the list calculates with help of sqrtUniversum(bool) function
			if fill == False:
				self.infoCluster = [None for count in range(self.sqrtUniversum(True))]
			else:
				self.infoCluster = [VEBTree(self.sqrtUni, fill) for count in range(self.sqrtUniversum(True))]
	def __init__(self, universum: int = 2, fill: bool = False) -> None:
		"""Initializing function of the VEBTree class
		Arguments:
					universum - the size of the universum for vEB tree
		"""
		self.universum = universum
		self.sqrtUni = self.sqrtUniversum()
		self._fixUniversum()
		self._minElement = None
		self._maxElement = None
		self.resume = None
		self._initResumes(fill)
		self.infoCluster = None
		self._initCluster(fill)
	def resetTree(self, universum: int = None, fill: bool = False):
		"""Function resets existing tree with size of the universum from 'universum'
		   If universum is None - function just resets vEB tree with same value of the universum
		   Otherwise new vEB tree is created with the size of the universum from 'universum'
		Arguments:
					universum - the size of the universum of the vEB tree
		"""
		if universum == None:
			universum = self.universum
		self.__init__(universum, fill)
	def getMin(self):
		return self._minElement
	def getMax(self):
		return self._maxElement
	def containsValue(self, value: int) -> bool:
		"""Checks whether value is in the VEBTree object
		Arguments:
					value - int value
		Return: 
					True	- if value is in the VEBTree object
					False 	- if value is not in the VEBTree object
		"""
		if self._isValueValid(value) == False:
			return False
		elif value == self.getMin() or value == self.getMax():
			return True
		elif self.universum == 2:
			return False
		else:
			clustIndex = self._high(value)
			if self.infoCluster[clustIndex] != None:
				return self.infoCluster[clustIndex].containsValue(self._low(value))
		return False
	def _insertValueEmpty(self, value: int) -> None:
		"""Inserts number into the empty base VEBTree object
		Arguments:
					value - int value
		"""
		if value != None:
			self._minElement = value
			self._maxElement = value
	def insertValue(self, value: int) -> bool:
		"""Inserts number into the VEBTree object
		Arguments:
					value - int value
		Return: 
					True	- if number has been inserted successfully
					False	- if number has not been inserted successfully
		"""
		if self._isValueValid(value) == False:
			return False
		# If minElement of the VEBTree object is empty
		# Then VEBTree object is empty too
		if self.getMin() == None:
			self._insertValueEmpty(value)
		else:
			# In this line program knows that VEBTree is not empty
			# Function checks whether new number is less than current minElement
			if value < self.getMin():
				# Function swaps values of variable 'value' and 'minElement'
				# This happens because new number is less than minElement and it becomes new minimum element
				# Also works with base VEBTree object (when it stores only one element)
				tmp = self.getMin()
				self._minElement = value
				value = tmp
			if self.universum > 2:
				clustIndex = self._high(value)
				valueIndex = self._low(value)
				if self.infoCluster[clustIndex] == None:
					self.infoCluster[self._high(value)] = VEBTree(self.sqrtUniversum(self.universum))
					# In this line program knows that it deals with non base VEBTree object
					# So it awares that it should also update the summary clusters
				if self.infoCluster[clustIndex].getMin() == None:
					if self.resume == None:
						self.resume = VEBTree(self.sqrtUniversum(True))
					# The cluster is empty
					# Function updates summary cluster according to the index of the updated cluster
					self.resume.insertValue(clustIndex)
					self.infoCluster[clustIndex]._insertValueEmpty(valueIndex)
				else:
					# The cluster is not empty
					# Dives into the recursion
					self.infoCluster[clustIndex].insertValue(valueIndex)
			# checks whether inserted value is the maximum value and updates in cluster which contains this value
			if value  > self.getMax():
				# Also can be the case where VEBTree object with universum = 2 (object stores only one element)
				self._maxElement = value
		return True
	def getSuccessor(self, value: int) -> int:
		"""Returns the successor of the given number in 'value'
		Arguments:
					value - int value
		Return:
					Int		- if the VEBTree object contains number greater than given number
					None	- if the VEBTree object does not contain greater value that given number
		"""
		if self._isValueValid(value) == False:
			return None
		if self.universum == 2:
			# If the given value is the least element in the base vEB tree
			# and next value is in the tree
			if value == 0 and self.getMax() == 1:
				# Then next value is the successor
				return 1
			else:
				return None
		# Checks whether value is less than minElement of current vEB object
		elif self.getMin() != None and value < self.getMin():
			return self.getMin()
		else:
			clustIndex = self._high(value)
			valueIndex = self._low(value)
			# Gets index of the max element of cluster which contains given value
			if self.infoCluster[clustIndex] != None:
				maxIndex = self.infoCluster[clustIndex].getMax()
				# Checks whether successor is located in the same cluster as the given number
				if maxIndex != None and maxIndex > valueIndex:
					# Gets the index of the successor
					offset = self.infoCluster[clustIndex].getSuccessor(valueIndex)	
					return self._index(clustIndex, offset)
			# Successor is not in the same cluster as given value
			# Searches for the next not empty cluster using summary cluster
			if self.resume != None:
				succClust = self.resume.getSuccessor(clustIndex)
				if succClust != None:
					# Gets the least element of the next not empty cluster
					offset = self.infoCluster[succClust].getMin()
					return self._index(succClust, offset)
				else:
					return None
	def getPredecessor(self, value: int) -> int:
		"""Returns the predecessor of the given number in 'value'
		Arguments:
					value - int value
		Return:
					Int		- if the VEBTree object contains number less than given number
					None	- if the VEBTree object does not contain less value that given number
		"""
		if self._isValueValid(value) == False:
			return None
		if self.universum == 2:
			# If the given value is the greatest element in the base vEB tree
			# and previous value is in the tree
			if value == 1 and self.getMin() == 0:
				# Then previous element is the predecessor
				return 0
			else:
				return None
		# Checks whether value is greater than maxElement of current vEB object
		elif self.getMax() != None and value > self.getMax():
			return self.getMax()
		else:
			clustIndex = self._high(value)
			valueIndex = self._low(value)
			if self.infoCluster[clustIndex] != None:
				# Gets index of the min element of cluster which contains given value
				minIndex = self.infoCluster[clustIndex].getMin()
				# Checks whether predecessor is located in the same cluster as the given number
				if minIndex != None and minIndex < valueIndex:
					offset = self.infoCluster[clustIndex].getPredecessor(valueIndex)
					return self._index(clustIndex, offset)
				else:
					# Predecessor is not in the same cluster as given value
					# Searches for the previous not empty cluster using summary cluster
					predClus = self.resume.getPredecessor(clustIndex)
					if predClus != None:
						# Gets the greatest element of the next not empty cluster
						offset = self.infoCluster[predClus].getMax()
						return self._index(predClus, offset)
					elif self.getMin() != None and value > self.getMin():
						return self.getMin()
					else:
						return None
	def removeValue(self, value: int) -> bool:
		"""Removes the given number from the VEBTree object if it contains removing value
		Arguments:
					value - int value
		Return:
				True	- if function has successfully removed value from the VEBTree object
				False	- if function has not removed value from the VEBTree object
		"""
		# Flag of the successfullness of the removing
		success = False
		if self._isValueValid(value) == False:
			success = False
		# If the tree is empty then nothing to remove
		elif self.getMin() == None:
			success = False
		# If the tree contains only one element
		elif self.getMin() == self.getMax() and self.getMin() == value:
			self._minElement = None
			self._maxElement = None
			success = True
		elif self.universum == 2:
			if self.getMin() != self.getMax():
				if value == 0:
					self._minElement = 1
				else:
					self._minElement = 0
				self._maxElement = self.getMin()
				success = True
		else:
			# If removing value is the least element in the vEB tree
			if value == self.getMin():
				firstCluster = self.resume.getMin()
				if firstCluster != None:
					# Then function updates removing value to the successor of the least element of the tree/
					value = self._index(firstCluster, self.infoCluster[firstCluster].getMin())
					# And updates minElement with 'value'
					# Following actions remove presence of this value in the tree
					self._minElement = value
			clustIndex = self._high(value)
			valueIndex = self._low(value)
			if self.infoCluster[clustIndex] != None:
				success = self.infoCluster[clustIndex].removeValue(valueIndex)
				if success == True:
					if self.infoCluster[clustIndex].getMin() == None:
						# If removing the given value results in emptiness of the cluster
						# Then function accordingly updates summary clusters 
						self.resume.removeValue(clustIndex)
						# If removing value is the greatest in the vEB tree
						if value == self.getMax():
							maxClusterIndex = self.resume.getMax()
							if maxClusterIndex == None:
								# If vEB tree contains only one element
								self._maxElement = self.getMin()
							else:
								# Otherwise function sets maxElement as predecessor of the removed maxElement
								self._maxElement = self._index(maxClusterIndex, self.infoCluster[maxClusterIndex].getMax())
					elif value == self.getMax():
						# If removed value was the greatest element in the vEB tree
						# Then function sets maxElement as predecessor of the removed maxElement
						self._maxElement = self._index(clustIndex, self.infoCluster[clustIndex].getMax())
		return success
