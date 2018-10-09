import csv
import sys
import time 




class StepDetector:
	lowerThreshold = 10
	higherThreshold = 20

	def __init__(self):
		self.previousHeelStrikeTime = 0
		self.nextHeelStrikeTime = 0
		self.toeOffTime = 0
		self.percentStance = 0

		self.firstAx = True
		self.prevAx = 0
		self.prevTime = 0

		self.stepCounter = 1

		self.firstThresholdUp = False
		self.secondThresholdUp = False
		self.secondThresholdDown = False
		self.firstThresholdDown = False
		self.nextFirstThresholdUp = False
		self.nextSecondThresholdUp = False



	def calculatePercentStance(self, PHS, NHS, TO):
		return 100 * ((TO - PHS) / (NHS - PHS))


	def interpolateLower(self, prevAx, afterAx, prevTime, afterTime):
		slope = (afterAx - prevAx) / (afterTime - prevTime)
		b = afterAx - slope * afterTime
		return (self.lowerThreshold - b) / slope


	def detectStep(self, pyr_ax, time):
		if (self.firstAx):
			self.firstAx = False

		else:
			slope = pyr_ax - self.prevAx

			# Resets to account for noise
			if (pyr_ax < self.lowerThreshold and self.firstThresholdUp and not self.secondThresholdUp):
				self.firstThresholdUp = False
				self.previousHeelStrikeTime = 0

			if (pyr_ax < self.lowerThreshold and self.firstThresholdUp and self.secondThresholdUp and 
					self.secondThresholdDown and self.firstThresholdDown and self.nextFirstThresholdUp and not self.nextSecondThresholdUp): 
				self.nextFirstThresholdUp = False
				self.nextHeelStrikeTime = 0




			if (pyr_ax > self.lowerThreshold and pyr_ax < self.higherThreshold and slope > 0):
				if (self.firstThresholdUp and self.secondThresholdUp and self.secondThresholdDown and self.firstThresholdDown and not self.nextFirstThresholdUp):
					self.nextHeelStrikeTime = self.interpolateLower(self.prevAx, pyr_ax, self.prevTime, time)
					self.nextFirstThresholdUp = True
				elif (not self.firstThresholdUp):
					self.previousHeelStrikeTime = self.interpolateLower(self.prevAx, pyr_ax, self.prevTime, time)
					self.firstThresholdUp = True

			elif (pyr_ax > self.higherThreshold and slope > 0 and self.firstThresholdUp):
				if (self.firstThresholdUp and self.secondThresholdUp and self.secondThresholdDown and self.firstThresholdDown and self.nextFirstThresholdUp): 
					self.nextSecondThresholdUp = True
				else: 
					self.secondThresholdUp = True

			elif (pyr_ax > self.lowerThreshold and pyr_ax < self.higherThreshold and slope < 0 and self.firstThresholdUp and self.secondThresholdUp):
				self.secondThresholdDown = True

			elif (pyr_ax < self.lowerThreshold and slope < 0 and self.firstThresholdUp and self.secondThresholdUp and self.secondThresholdDown and not self.firstThresholdDown):
				self.toeOffTime = self.interpolateLower(self.prevAx, pyr_ax, self.prevTime, time)
				self.firstThresholdDown = True
            


			self.prevAx = pyr_ax
			self.prevTime = time

			if (self.nextSecondThresholdUp):
				self.percentStance = self.calculatePercentStance(self.previousHeelStrikeTime, self.nextHeelStrikeTime, self.toeOffTime)
				strideTime = self.nextHeelStrikeTime - self.previousHeelStrikeTime
				print(self.stepCounter, ' ', self.previousHeelStrikeTime,  '  ', self.toeOffTime, '  ', self.nextHeelStrikeTime, '   ', self.previousHeelStrikeTime,
					'    ', strideTime)
				self.firstThresholdUp = True       
				self.secondThresholdUp = True       
				self.secondThresholdDown = False
				self.firstThresholdDown = False
				self.nextFirstThresholdUp = False
				self.nextSecondThresholdUp = False	
				self.previousHeelStrikeTime = self.nextHeelStrikeTime;
				self.stepCounter += 1

				return True
   

		return False











def main():
	fileInput = sys.argv[1]
	fileType = int(sys.argv[2])  # 0: just axial      1: six data channels

	myStepDetector = StepDetector()
	t = 0
	print('                    PHS', '                       TO',   '              NHS',
	 '               percentStance', '               strideTime')
	with open(fileInput, 'r') as fileIn:
		csvReader = csv.reader(fileIn)
		for row in csvReader:
			if (fileType == 0):
				myStepDetector.detectStep(float(row[0]), t)
			else:
				packet = row.split(',')
				myStepDetector.detectStep(float(packet[2]), t)

			#time.sleep(.01)
			t += 10




	return










