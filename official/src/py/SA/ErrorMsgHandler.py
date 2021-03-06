from enum import Enum


class AnsiEscapeCodes(Enum):
	Red = 1
	Purple = 2
	Clean = 3

	def __str__(self):
		if self.value == AnsiEscapeCodes.Red.value:
			return "\033[1;31m"
		elif self.value == AnsiEscapeCodes.Purple.value:
			return "\033[1;35m"
		elif self.value == AnsiEscapeCodes.Clean.value:
			return "\033[0m"


class ExType(Enum):
	error = 1
	warning = 2

	def __str__(self):
		if self.value == ExType.error.value:
			return "Error: "
		elif self.value == ExType.warning.value:
			return "Warning: "
		return ""

	def getColor(self):
		if self.value == ExType.error.value:
			return str(AnsiEscapeCodes.Red)
		elif self.value == ExType.warning.value:
			return str(AnsiEscapeCodes.Purple)
		return str(AnsiEscapeCodes.Clean)




def determineExPrefix(exType, position):
	return exType.getColor() + \
		("" if position == None else "(" + ",".join([str(i) for i in position]) + ") ") + \
		str(exType) + str(AnsiEscapeCodes.Clean)




class ErrorMsgHandler:
	@staticmethod
	def throwErrorMessage(exType, errorString, node=None):
		raise Exception(determineExPrefix(exType, (None if node == None else node.position)) + errorString)

	# =============================
	# SymboltableBuilder exceptions
	# =============================
	@staticmethod
	def functionAlreadyInitialised(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Function '" + str(node.value) + "' has already been initialized.", node)

	@staticmethod
	def symbolAlreadyDeclared(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Symbol '" + str(node.value) + "' has already been declared in this scope.", node)
	

	# ===========================
	# ExistenceChecker exceptions
	# ===========================
	@staticmethod
	def varRefBeforeDecl(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Variable '" + str(node.value) + "' referenced before declaration.", node)

	@staticmethod
	def functionBeforeDecl(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Function '" + str(node.value) + "' called before declaration.", node)

	@staticmethod
	def functionBeforeInit(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Function '" + str(node.value) + "' called before initialization.", node)

	@staticmethod
	def mainDoesntExist():
		ErrorMsgHandler.throwErrorMessage(ExType.error, "The program does not contain a 'main' function.")

	@staticmethod
	def undefinedFunction(node, functionName, hint=""):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "'" + functionName + "' was not declared in this scope" + \
			("" if hint == "" else " (try including header '" + hint + "')") + ".", node)


	# ===================
	# VarTypes exceptions
	# ===================
	@staticmethod
	def extensiveDereferencing():
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot dereference variable more times than its pointer count.")

	@staticmethod
	def addrOfFunction():
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Address of functions is not supported.")

	# ======================
	# TypeChecker exceptions
	# ======================
	@staticmethod
	def typesAssignmentWrong(node, type1, type2):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Types for assignment don't match ('" + type1.getStrType() + "' and '" + type2.getStrType() + "').", \
			node)

	@staticmethod
	def typesComparisonWrong(node, type1, type2):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Types for comparison don't match ('" + type1.getStrType() + "' and '" + type2.getStrType() + "').", \
			node)

	@staticmethod
	def returnTypeWrong(node, functionSymbol, requiredType, givenType):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Return type doesn't match '" + functionSymbol + "' signature ('" + requiredType.getStrType() + "' required, '" + givenType.getStrType() + "' given).", \
			node)

	@staticmethod
	def typeInitWrong(node, type1, type2):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Types for initialization don't match ('" + type1.getStrType() + "' and '" + type2.getStrType() + "').", \
			node)
		pass

	@staticmethod
	def arrayElementWrongAccess(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Elements of array '" + str(node.value) + "' should be accessed with an integer.", node)

	@staticmethod
	def functionArgsInvalid(node, amtRequired, amtGiven):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Function arguments invalid: '" + str(node.value) + "' takes " \
			+ str(amtRequired) + " " + ("arguments" if amtRequired != 1 else "argument") + " " + \
			"(" + str(amtGiven) + " " + ("arguments" if amtGiven != 1 else "argument") + " given).", \
			node)

	@staticmethod
	def functionArgWrong(node, typeReq, typeGiven, index):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Argument for function call '" + str(node.value) + "' did not match the signature ('" \
			+ typeReq.getStrType() + "' required, '" + typeGiven.getStrType() + "' given, argument #" + str(index) + ").", \
			node)


	# =======================
	# TypeDeductor exceptions
	# =======================
	@staticmethod
	def derefMultipleVars(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot dereference more than 1 variable.", node)

	@staticmethod
	def derefInvalidExpression(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot dereference non-int/pointer expressions.", node)

	@staticmethod
	def derefNonPointer(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot dereference non-pointer variable '" + str(node.value) + "'.", node)

	@staticmethod
	def overDereferencing(node, maxAmt, amt):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Cannot dereference variable '" + str(node.value) + "' " + str(amt) + " times (only " \
			+ str(maxAmt) + (" times" if maxAmt != 1 else " time") + " allowed).", \
			node)

	@staticmethod
	def typesOperationWrong(node, type1, type2, operationNode):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Types for operation '" + str(operationNode.type.name) + "' don't match ('" + type1.getStrType() + "' and '" + type2.getStrType() + "').", \
			node)

	@staticmethod
	def referenceArgumentInvalid(node, requiredType, index):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Argument for function call '" + str(node.value) + "' is not a valid reference argument ('" \
			+ requiredType.getStrType() + "' reference required, argument #" + str(index) + ").", \
			node)

	@staticmethod
	def negateInvalid(node, givenType):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot negate '" + givenType.getStrType() + "' (only 'int' and 'float' allowed).", node)

	@staticmethod
	def addressOpNonInt(node, givenType):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot add '" + givenType.getStrType() + "' value to pointer dereference.", node)


	# ======================
	# PTranslator exceptions
	# ======================
	@staticmethod
	def typeFormatWrong(node, typeRequired, givenType, position):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Type '" + givenType.getStrType() + "' does not match the argument in the formatstring " +\
			"('" + typeRequired.getStrType() + "' required, argument #" + str(position) + ").", \
			node)

