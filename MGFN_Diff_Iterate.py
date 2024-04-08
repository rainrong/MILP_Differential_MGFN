"""
x_i_63,x_i_62,....x_i_0 denote the input to the (i+1)-th round.
"""
from os import read

from gurobipy import *

import time


class MGFN:
	def __init__(self, Round):
		self.Round = Round
		self.blocksize = 64
		self.filename_model = "MGFN1_" + str(self.Round) +"_" + "round_iteration" + "_MGFN_SBOX" + ".lp"
		self.filename_result = "result_MGFN1_" + str(self.Round) + "round_iteration"+ "_MGFN_SBOX" + ".txt"
		fileobj = open(self.filename_model, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "w")
		fileobj.close()
		self.Globaly = 0
		self.Xorcount = 0


	# linear layer for the MGFN cipher
	P_Layer = [4,11,18,7,23,19,2,25,14,26,1,28,20,8,29,0,31,5,15,21,9,13,24,6,17,12,22,3,16,30,10,27]

	# Linear inequalities for the MGFN Sbox
	S_T = [
			#MGFN SBOX
			[4, 2, 4, 3, -2, -1, 1, -1, 0],
			[-1, 2, -2, -1, 2, 3, 3, 4, 0],
			[-3, -2, -3, 1, -2, -3, -1, 3, 10],
			[-3, -1, 3, 1, 2, 3, 1, -1, 2],
			[3, -1, -2, -2, -1, 3, -2, 1, 5],
			[-1, -3, 4, -2, -1, -2, -3, -4, 12],
			[3, 4, 1, 4, 3, -2, -2, 1, 0],
			[2, -3, 1, 1, 2, 1, 2, 3, 0],
			[1, 2, 3, -1, 1, -2, 3, -2, 2],
			[-1, 3, -1, 3, 1, 2, 3, -1, 0],
			[-2, 1, -2, -3, 1, -2, -2, 1, 8],
			[1, -1, -1, 1, -1, -1, 1, 1, 2],
			[0, -2, -1, -2, 2, -1, -1, -2, 7],
			[3, 3, 4, 1, 1, 3, -2, -2, 0],
			[-1, 1, 2, 1, -2, 2, -1, 2, 2],
			[-1, 0, -1, 1, -1, 0, -1, -1, 4],
			[-1, -1, -1, -1, -1, 0, 1, -1, 5],
			[1, 2, -1, 1, -2, 2, 0, -2, 3],
			[1, 2, -1, -2, -1, -1, -2, 2, 5],
			[1, -2, 2, -1, -1, -1, 0, -2, 5],
			[-2, 1, 1, -1, 2, -1, -2, 2, 4],
			[-1, 0, -1, -1, 1, -1, 0, -1, 4],
			[-2, -1, -2, 2, -1, 1, -2, -1, 7],
			[1, 1, -1, -1, -1, 0, 1, -1, 3],
			[1, -2, -2, 3, 3, 1, 4, 3, 0],
			[0, 1, 1, 1, 1, -1, 1, 0, 0],
			[-1, -1, 1, -1, 2, 3, 3, 2, 0],
			[-1, 1, 1, -1, -1, -1, 1, 0, 3],
			[1, -2, -1, -1, 2, -1, -1, -2, 6]

		# #NEW SBOX
		# 	[5, 4, -2, 7, -1, 7, -1, -3, 0],
		# 	[2, 1, 1, -5, 3, 4, 3, 2, 0],
		# 	[2, -1, -1, -2, 0, -2, 0, -1, 5],
		# 	[2, -1, 1, 2, 0, -1, 0, 2, 0],
		# 	[-2, 0, -2, 0, -1, 2, -1, -1, 5],
		# 	[-2, 0, 1, 0, 2, 2, 1, 1, 0],
		# 	[-3, 3, 1, -1, -1, -1, 3, -2, 5],
		# 	[-1, -1, 0, 0, 0, -1, -1, -1, 4],
		# 	[2, 1, 2, 1, 0, -2, 0, 1, 0],
		# 	[-1, 1, 2, 3, 3, -1, -1, 3, 0],
		# 	[2, -1, 2, -1, 0, 2, 0, 1, 0],
		# 	[3, 0, -1, -1, 3, 2, 2, -1, 0],
		# 	[-1, 0, 1, -1, -1, -1, 0, 1, 3],
		# 	[-1, 0, -1, 1, 1, -1, 0, -1, 3],
		# 	[-1, 0, -1, -1, -1, 0, 0, -1, 4],
		# 	[1, -1, 0, 0, 0, 1, 1, 1, 0],
		# 	[-1, 0, 2, 0, 1, 2, 2, -1, 0],
		# 	[2, 1, 1, 0, -1, 1, -1, 1, 0],
		# 	[0, -2, -1, -2, 1, -1, -2, -1, 7],
		# 	[-1, -1, -1, 1, 1, -1, 1, 0, 3],
		# 	[-1, 1, -1, -1, 1, -1, 1, 0, 3],
		# 	[-1, 1, -1, 1, -1, -1, 1, 0, 3],
		# 	[0, -1, -1, -1, -1, -1, 1, 0, 4],
		# 	[-2, -2, -3, 1, -2, 1, -2, -1, 9],
		# 	[-1, 1, -2, -1, -2, 1, -2, 1, 6]

		# #present_sbox
		#    [3, 4, 4, 1, -2, 0, -2, 1, 0],
        #    [0, -2, -2, 3, 4, 1, 4, 1, 0],
        #    [-2, 1, 1, 3, 1, -1, 1, 2, 0],
        #    [1, -3, -2, -2, 3, -4, 1, -3, 10],
        #    [-1, -2, -2, -1, -1, 2, -1, 0, 6],
        #    [2, 1, 1, -3, 1, 2, 1, 2, 0],
        #    [-2, -2, 1, -1, -2, -1, 1, 0, 6],
        #    [-1, 2, -3, 1, -1, -2, -3, -3, 10],
        #    [-1, 1, 1, -1, 0, 0, 0, -1, 2],
        #    [2, -1, 2, 2, 2, 3, -1, -1, 0],
        #    [2, 3, -2, -4, -4, -4, -1, 1, 11],
        #    [2, 2, -1, 2, -1, 3, 2, -1, 0],
        #    [-1, -3, 2, 1, -3, -2, -1, -3, 10],
        #    [-1, 0, -1, -1, 1, 0, -1, 0, 3],
        #    [0, -1, -1, 1, -1, 0, -1, 1, 3],
        #    [0, -1, 1, -1, 0, -1, -1, 1, 3],
        #    [-2, 0, 0, 1, 2, 1, 2, 1, 0],
        #    [0, -2, -2, -2, -1, 2, -1, -1, 7],
        #    [2, 3, 3, 2, 1, -4, 1, 1, 0],
        #    [1, -2, -3, -2, 1, -4, 3, -3, 10],
        #    [0, 1, 1, -1, -1, 1, -1, 0, 2],
        #    [1, 1, 1, 1, 1, 1, -2, 1, 0],
        #    [2, 1, 1, 0, -2, 1, 1, 2, 0]
	]
	NUMBER = 9

	def CreateObjectiveFunction(self):
		"""
		Create objective function of the MILP model
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("MINIMIZE\n")
		eqn = []
		for i in range(0, self.Round * 8):
			eqn.append("y" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

	@staticmethod
	def CreateVariables(n, pos):
		"""
		Generate the variables used in the model.
		"""
		array = []
		for i in range(0, 32):
			array.append(("x" + "_" + str(n) + "_" + str(pos) + "_" + str(i)))
		return array

	@staticmethod
	def CreateTempVariables(n):
		array = []
		for i in range(0, 32):
			array.append(("temp" + "_" + str(n) + "_" + str(i)))
		return array

	def ConstraintsBySbox(self, variable1, variable2):
		"""
		Generate the constraints by sbox layer.
		"""
		fileobj = open(self.filename_model, "a")
		for k in range(0, 8):
			for coff in MGFN.S_T:
				temp = []
				for u in range(0, 4):
					temp.append(str(coff[u]) + " " + variable1[(k * 4) + u])
				for v in range(0, 4):
					temp.append(str(coff[v + 4]) + " " + variable2[(k * 4) + v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coff[MGFN.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")
			eqn = [' + '.join(variable1[(k * 4) + 3 - u] for u in range(0, 4)) + ' - y' + str(self.Globaly) + ' >= 0']
			for t in range(0, 4):
				eqn.append(variable1[(k * 4) + 3 - t] + ' - y' + str(self.Globaly) + ' <= 0')
			for var in eqn:
				fileobj.write(var + '\n')
			self.Globaly += 1
		fileobj.close()

	@staticmethod
	def LinearLaryer(variable):
		"""
		Linear layer.
		"""
		array = ["" for i in range(0, 32)]
		for i in range(0, 32):
			array[MGFN.P_Layer[i]] = variable[i]
		return array
	
	def inverse_LinearLaryer(self, variable):
		"""
		inverse_Linear layer.
		"""
		array = ["" for i in range(0, 32)]
		for i in range(0, 32):
			array[i] = variable[MGFN.P_Layer[i]]
		return array

	def rotateLayer(self, variable1):
		return variable1[:16][13:] + variable1[:16][:13] + variable1[16:][8:] + variable1[16:][:8]

	def inverse_rotateLayer(self, variable2):
		return variable2[:16][3:] + variable2[:16][:3] + variable2[16:][8:] + variable2[16:][:8]

	def XORLayer(self, variable1, variable2, variable3):
		fileobj = open(self.filename_model, "a")
		for i in range(32):
			fileobj.write(
				str(variable1[i]) + " + " + str(variable2[i]) + " + " + str(variable3[i]) + " - 2 a" + str(
					self.Xorcount) + " >= 0\n")
			fileobj.write('a' + str(self.Xorcount) + ' - ' + variable1[i] + " >= 0\n")
			fileobj.write('a' + str(self.Xorcount) + ' - ' + variable2[i] + " >= 0\n")
			fileobj.write('a' + str(self.Xorcount) + ' - ' + variable3[i] + " >= 0\n")
			fileobj.write(str(variable1[i]) + " + " + str(variable2[i]) + " + " + str(variable3[i]) + " <= 2\n")
			self.Xorcount += 1
		fileobj.close()

	def Constraint(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert (self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")
		fileobj.close()
		# forword
		variableinL = MGFN.CreateVariables(0, "L")
		variableinR = MGFN.CreateVariables(0, "R")
		variableoutR = MGFN.CreateVariables(1, "L")
		variableoutL = variableinL
		variabletemp = MGFN.CreateTempVariables(1)

		variableinL = self.rotateLayer(variableinL)
		self.ConstraintsBySbox(variableinL, variabletemp)
		variabletemp = self.LinearLaryer(variabletemp)
		
		self.XORLayer(variableinR, variabletemp, variableoutR)

		for i in range(2, self.Round + 1):
			variableinL = variableoutR
			variableinR = variableoutL
			variabletemp = MGFN.CreateTempVariables(i)
			variableoutR = MGFN.CreateVariables(i, "L")
			variableoutL = variableinL

			variableinL = self.rotateLayer(variableinL)
			self.ConstraintsBySbox(variableinL, variabletemp)
			variabletemp = self.LinearLaryer(variabletemp)
			self.XORLayer(variableinR, variabletemp, variableoutR)
		return variableoutL, variableoutR


	def VariableBinary(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0, self.Round + 1):
			varinL = self.CreateVariables(i, 'L')
			for item in varinL:
				fileobj.write(str(item) + "\n")
			if i == 0:
				varinR = self.CreateVariables(i, 'R')
				for item in varinR:
					fileobj.write(str(item) + "\n")
		for i in range(1, self.Round + 1):
			vartemp = self.CreateTempVariables(i)
			for item in vartemp:
				fileobj.write(str(item) + "\n")
		for i in range(0, self.Xorcount):
			fileobj.write('a' + str(i) + '\n')
		for i in range(0, self.Globaly):
			fileobj.write('y' + str(i) + '\n')
		fileobj.write("END")
		fileobj.close()


	def WriteObjective(self, obj):
		"""
		Write the objective value into filename_result.
		"""
		fileobj = open(self.filename_result, "a")
		fileobj.write("The objective value = %d\n" % obj.getValue())
		eqn1 = []
		eqn2 = []
		for i in range(0, self.blocksize):
			u = obj.getVar(i)
			if u.getAttr("x") != 0:
				eqn1.append(u.getAttr('VarName'))
				eqn2.append(u.getAttr('x'))
		length = len(eqn1)
		for i in range(0, length):
			s = eqn1[i] + "=" + str(eqn2[i])
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()

	def Init(self, endL, endR):
		"""
		迭代差分限制
		"""
		fileobj = open(self.filename_model, "a")
		startL, startR = MGFN.CreateVariables(0, "L"), MGFN.CreateVariables(0, "R")
		for i in range(32):
			fileobj.write(str(startR[i]) + " - " + str(endL[i]) + " = 0 " "\n")
			fileobj.write(str(startL[i]) + " - " + str(endR[i]) + " = 0 " "\n")
		fileobj.close()
		"""
		限制输入不可全为0
		"""
		fileobj = open(self.filename_model, "a")
		Init_str = ' + '.join('x_0_L_' + str(i) for i in range(0, 32)) + ' + ' + ' + '.join('x_0_R_' + str(i) for i in range(0, 32)) + ' >= 1' #   语法留意学习,注意元素与计算符号间存在空格要
		fileobj.write(Init_str + '\n')
		fileobj.close()

	def MakeModel(self):
		"""
		Generate the MILP model of MGFN given the round number and activebits.
		"""
		self.CreateObjectiveFunction()
		outL, outR = self.Constraint()
		self.Init(outL, outR)
		self.VariableBinary()

	def SolveModel(self):
		"""
		Solve the MILP model to search the .
		"""
		time_start = time.time()
		m = read(self.filename_model)
		m.optimize()
		fileobj = open(self.filename_result, "a")
		if m.Status == 2:
			listrecoverorder = list(range(0,32))
			listrecoverorder_rotate = self.inverse_rotateLayer(listrecoverorder)
			listrecoverorder_P = self.inverse_LinearLaryer(listrecoverorder)
			listorder_rotate = self.rotateLayer(listrecoverorder)
			listorder_P = self.LinearLaryer(listrecoverorder)


			print("feasible")
			fileobj.write('ROUND_1:')
			fileobj.write("\n")

			fileobj.write('LEFT_IN:' )
			for j in range(32):					
				a = m.getVarByName('x_' + str(0) + "_L_" + str(j))					
				fileobj.write(str(int(a.getAttr("x"))))					
			fileobj.write("\n")		

			fileobj.write('RIGHT_IN:' )
			for j in range(0, 32):					
				a = m.getVarByName('x_' + str(0) + "_R_" + str(j))					
				fileobj.write(str(int(a.getAttr("x"))))						
			fileobj.write("\n")

			# fileobj.write('SBOX_IN:' )
			for j in range(0, 32):			
				if j%4 == 0:
					fileobj.write('_')	
				a = m.getVarByName('x_' + str(0) + "_L_" + str(listorder_rotate[j]))					
				fileobj.write(str(int(a.getAttr("x"))))	
			fileobj.write('__SBOX_IN' )					
			fileobj.write("\n")

			# fileobj.write('SBOX_OUT:' )
			for j in range(0, 32):	
				if j%4 == 0:
					fileobj.write('_')									
				a = m.getVarByName('temp_' + str(1) + "_" + str(j))					
				fileobj.write(str(int(a.getAttr("x"))))
			fileobj.write('__SBOX_OUT' )						
			fileobj.write("\n")
			# fileobj.write('SBOX_IN:' )
			# for j in range(0, 32):					
			# 	a = m.getVarByName('x_' + str(0) + "_L_" + str(listorder_rotate[j]))					
			# 	fileobj.write(str(int(a.getAttr("x"))))						
			# fileobj.write("\n")

			# fileobj.write('SBOX_OUT:' )
			# for j in range(0, 32):					
			# 	a = m.getVarByName('temp_' + str(1) + "_" + str(j))					
			# 	fileobj.write(str(int(a.getAttr("x"))))						
			# fileobj.write("\n")

			fileobj.write('LEFT_OUT:' )
			for j in range(0, 32):					
				a = m.getVarByName('x_' + str(1) + "_L_" + str(j))					
				fileobj.write(str(int(a.getAttr("x"))))						
			fileobj.write("\n")

			fileobj.write('RIGHT_OUT:' )
			for j in range(0, 32):					
				a = m.getVarByName('x_' + str(0) + "_L_" + str(j))				
				fileobj.write(str(int(a.getAttr("x"))))					
			fileobj.write("\n")	
				

			for i in range(2, self.Round+1):
				fileobj.write('ROUND_' + str(i) + ':')
				fileobj.write("\n")

				fileobj.write('LEFT_IN:' )
				for j in range(0, 32):					
					a = m.getVarByName('x_' + str(i-1) + "_L_" + str(j))					
					fileobj.write(str(int(a.getAttr("x"))))					
				fileobj.write("\n")		

				fileobj.write('RIGHT_IN:' )
				for j in range(0, 32):					
					a = m.getVarByName('x_' + str(i-2) + "_L_" + str(j))					
					fileobj.write(str(int(a.getAttr("x"))))						
				fileobj.write("\n")

				# fileobj.write('SBOX_IN:' )
				for j in range(0, 32):
					if j%4 == 0:
						fileobj.write('_')											
					a = m.getVarByName('x_' + str(i-1) + "_L_" + str(listorder_rotate[j]))					
					fileobj.write(str(int(a.getAttr("x"))))						
				fileobj.write('__SBOX_IN' )	
				fileobj.write("\n")

				# fileobj.write('SBOX_OUT:' )
				for j in range(0, 32):	
					if j%4 == 0:
						fileobj.write('_')										
					a = m.getVarByName('temp_' + str(i) + "_" + str(j))					
					fileobj.write(str(int(a.getAttr("x"))))	
				fileobj.write('__SBOX_OUT' )				
				fileobj.write("\n")
				# fileobj.write('SBOX_IN:' )
				# for j in range(0, 32):					
				# 	a = m.getVarByName('x_' + str(i-1) + "_L_" + str(listorder_rotate[j]))					
				# 	fileobj.write(str(int(a.getAttr("x"))))						
				# fileobj.write("\n")

				# fileobj.write('SBOX_OUT:' )
				# for j in range(0, 32):					
				# 	a = m.getVarByName('temp_' + str(i) + "_" + str(j))					
				# 	fileobj.write(str(int(a.getAttr("x"))))						
				# fileobj.write("\n")

				fileobj.write('LEFT_OUT:' )
				for j in range(0, 32):					
					a = m.getVarByName('x_' + str(i) + "_L_" + str(j))					
					fileobj.write(str(int(a.getAttr("x"))))						
				fileobj.write("\n")

				fileobj.write('RIGHT_OUT:' )
				for j in range(0, 32):					
					a = m.getVarByName('x_' + str(i-1) + "_L_" + str(j))					
					fileobj.write(str(int(a.getAttr("x"))))					
				fileobj.write("\n")


			# fileobj.write('ROUND_' + str(self.Round) + ':')
			# fileobj.write("\n")

			# fileobj.write('LEFT_IN:' )
			# for j in range(0, 32):					
			# 	a = m.getVarByName('x_' + str(self.Round-1) + "_L_" + str(j))					
			# 	fileobj.write(str(int(a.getAttr("x"))))					
			# fileobj.write("\n")		

			# fileobj.write('RIGHT_IN:' )
			# for j in range(0, 32):					
			# 	a = m.getVarByName('x_' + str(self.Round-2) + "_L_" + str(j))					
			# 	fileobj.write(str(int(a.getAttr("x"))))						
			# fileobj.write("\n")

			# fileobj.write('SBOX_IN:' )
			# for j in range(0, 32):					
			# 	a = m.getVarByName('x_' + str(self.Round-1) + "_L_" + str(listorder_rotate[j]))					
			# 	fileobj.write(str(int(a.getAttr("x"))))						
			# fileobj.write("\n")

			# fileobj.write('SBOX_OUT:' )
			# for j in range(0, 32):					
			# 	a = m.getVarByName('temp_' + str(self.Round) + "_" + str(j))					
			# 	fileobj.write(str(int(a.getAttr("x"))))						
			# fileobj.write("\n")

			# fileobj.write('LEFT_OUT:' )
			# for j in range(0, 32):					
			# 	a = m.getVarByName('x_' + str(self.Round-1) + "_L_" + str(j))					
			# 	fileobj.write(str(int(a.getAttr("x"))))						
			# fileobj.write("\n")

			# fileobj.write('RIGHT_OUT:' )
			# for j in range(0, 32):					
			# 	a = m.getVarByName('x_' + str(self.Round) + "_L_" + str(j))					
			# 	fileobj.write(str(int(a.getAttr("x"))))					
			# fileobj.write("\n")
			



			for i in range(0, self.Globaly):
				a = m.getVarByName('y' + str(i))
				fileobj.write('y' + str(i) + ": " + str(a.getAttr("x")))
				fileobj.write("\n")
		print(m.getObjective().getValue())
		time_end = time.time()
		print(("Time used = " + str(time_end - time_start)))
		fileobj.close()


if __name__ == "__main__":
	ROUND = int(input("Input the target round number: "))
	while not (ROUND > 0):
		print("Input a round number greater than 0.")
		ROUND = int(input("Input the target round number again: "))
	
	mgfn = MGFN(ROUND)
	
	mgfn.MakeModel()
	
	mgfn.SolveModel()
	# for i in range(0, 32 * 31 + 31):
	# 	first = i // 32
	# 	second = i % 32
	# 	activateseart = [first, second]
	# 	for j in range(0, 32 * 31 + 31):
	# 		first = j // 32
	# 		second = j % 32
	# 		activateend = [first, second]
	# 		mgfn = MGFN(9)
	# 		mgfn.MakeModel(activateseart, activateend)
	# 		mgfn.SolveModel(activateseart, activateend)
