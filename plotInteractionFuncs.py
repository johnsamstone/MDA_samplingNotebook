import sys, os
sys.path.append(os.path.abspath('..'))

from matplotlib import pyplot as plt
import numpy as np


#First define some helpful function

def MDA_simpleOverlap(ages,errors,xSigmaOverlap = 2,n = 3,excludeExtraOverlap = False):
    '''
    Identify the youngest suit of ages that overlap within the specified error
    :param ages: The mean values
    :param errors: The error ranges where uncertainty is tolerated
    :param xSigmaOverlap: With in how many standard deviations of the uncertainty to we want to look for overlap?
    :param n: The minimum number of grains that are required to overlap
    :param excludeExtraOverlap: boolean, do you only want the n youngest overlapping grains (True), or will you take at least n (False)?
    :return:
    '''

    #First sort the grains from youngest to oldest
    agesSrtd, errorsSrtd = sortAgesErrors(ages,errors)
    errorsSrtd*=xSigmaOverlap

    minMax = np.zeros((len(ages),2)) #Initialize an array with two colums, one for the min one for max of each grain

    #Populate with the range
    minMax[:,0] = agesSrtd - errorsSrtd
    minMax[:,1] = agesSrtd + errorsSrtd

    #Did we find a result?
    foundResult = False

    #Look through the sorted ranges from youngest to oldest, there is also a recursive approach to this. Starting
    #from each point in the sorted array search your neighbors, if they are within bounds search their neighbors, just have
    #to be careful with that - because one sample may have a higher mean but broader spread, causing it to sit farther away
    #in the array but stilloverlap
    for i in range(len(ages)):
        thisMinMax = minMax[i]

        #How many places is this upper bound within other ranges
        upperInBounds = (thisMinMax[1] >= minMax[:,0]) & (thisMinMax[1] <= minMax[:,1])

        #How many places is this upper bound within other ranges
        lowerInBounds = (thisMinMax[0] >= minMax[:,0]) & (thisMinMax[0] <= minMax[:,1])

        #How many total matches
        totalMatches = upperInBounds | lowerInBounds
        nMatches = np.sum(totalMatches)
        #If we found enough matching grains, quit
        if nMatches >= n:
            foundResult = True

            # If we found too many overlapping grains, just take the first n
            if (nMatches > n) & excludeExtraOverlap:
                matchAges = agesSrtd[totalMatches][:n]
                matchErrors = errorsSrtd[totalMatches][:n]
            else:
                matchAges = agesSrtd[totalMatches]
                matchErrors = errorsSrtd[totalMatches]
            break

    #If we found a result calculate a weighted mean, if not return nan
    if foundResult:
        mean,error = weightedMean(matchAges,matchErrors)
        mswd = np.sum((mean - matchAges)**2/matchErrors**2)/(len(matchAges) - 1)
    else:
        mean, error = np.nan, np.nan
        mswd = np.nan
    return mean,error,mswd

def sortAgesErrors(ages,errors):
    '''
    Return a sorted copy of the ages and errors
    :param ages:
    :param errors:
    :return:
    '''

    #First sort the grains from youngest to oldest
    srtIdx = np.argsort(ages)
    agesSrtd = ages[srtIdx]
    errorsSrtd = errors[srtIdx]

    return agesSrtd, errorsSrtd

def weightedMean(ages,errors):
    '''
    Calculate a weighted mean age
    :param ages:
    :param errors:
    :return:
    '''

    weights = 1.0/(errors**2)

    meanAge = np.sum(weights * ages) / np.sum(weights)

    meanError = 1.0 / np.sqrt(np.sum(weights))

    return meanAge,meanError
    

#Now define some code for interacting with plots

class distributionMaker:
    def __init__(self, line,PDPAgeAxis,relError = 0.1):

        #### LEft off here - trying to make a PDF click maker.
        self.line = line
        self.PDPAgeAxis = PDPAgeAxis
        self.relErr = relError
        self.ages = list(line.get_xdata())
        self.errors = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes!=self.line.axes: return
        self.ages.append(event.xdata)
        self.errors = [self.relErr*age for age in self.ages]
        self.p = self._createPDF_()

        self.line.set_data(self.PDPAgeAxis, self.p/np.max(self.p))
        self.line.figure.canvas.draw()

    def _createPDF_(self):

        p = np.zeros_like(self.PDPAgeAxis)

        for age, error in zip(self.ages, self.errors):
            p += (1.0 / np.sqrt(2.0 * error ** 2 * np.pi)) * np.exp(-(self.PDPAgeAxis - age) ** 2 / (2.0 * error ** 2))


        return p


class pointGetter:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.ys = [y / np.sum(self.ys) for y in self.ys]

        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()


class MDAExample:
    def __init__(self, dataline,mdaline, relError = 0.1,MDAfunc = None):
        self.line = dataline
        self.mdaLine = mdaline
        self.relError = relError
        self.xs = list(dataline.get_xdata())
        self.ys = list(dataline.get_ydata())
        self.cid = dataline.figure.canvas.mpl_connect('button_press_event', self)

        if MDAfunc is None:
            MDAfunc = lambda age,error: MDA_simpleOverlap(age,error)[0]

        self.MDAFunc = MDAfunc

    def __call__(self, event):
        if event.inaxes!=self.line.axes: return

        #Sort for clean plotting
        self.xs.append(event.xdata)
        srtIdcs= np.argsort(self.xs)
        self.xs = [self.xs[i] for i in srtIdcs]
        self.ys = (np.linspace(0,1,len(self.xs)))

        MDA = self.MDAFunc(np.array(self.xs),np.array(self.xs)*self.relError)

        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

        self.mdaLine.set_data([MDA,MDA],[0,1])
