# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb

    def selfproduce(self):
        resistances = {}
        for r in self.resistances:
            if random.random() < (1-self.mutProb):
                resistances[r] = self.switcheroo(self.resistances[r])
            else:
                resistances[r] = self.resistances[r]
        return ResistantVirus(self.maxBirthProb, self.clearProb, resistances, self.mutProb)

    def switcheroo(self, resistance):
        if resistance is True:
            return False
        if resistance is False:
            return True

    def isResistantTo(self, drug):
        return self.resistances[drug]
        
    def reproduce(self, popDensity, activeDrugs):
        for d in activeDrugs:
            if self.resistances[d] is False:
                return False
        if random.random() < (self.maxBirthProb * (1-popDensity)):
            return True
        return False            

class Patient(SimplePatient):
    def __init__(self, viruses, maxPop):
        self.viruses = viruses
        self.maxPop = maxPop
        self.activeDrugs = []
    
    def addPrescription(self, newDrug):
        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)

    def getPrescriptions(self):
        return self.activeDrugs
        
    def getResistPop(self, drugResist):
        funzies, counter = {}, 0
        for v in self.viruses:
            funzies[v] = True
            for drug in drugResist:
                if funzies[v] is False:
                    break
                if v.resistances[drug] is False:
                    funzies[v] = False
        for i in funzies:
            if funzies[i] is True:
                counter += 1
        return counter
                
    def update(self):
        """    
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        for v in self.viruses:
            if v.doesClear() is True:
                self.viruses.remove(v)
        self.setpopDensity()
        copylist = []
        for v in self.viruses:
            if v.reproduce(self.popDensity, self.activeDrugs) is True:
                copylist.append(v)
        for v in copylist:
            self.viruses.append(v.selfproduce())
        return len(self.viruses)


Sid = Patient([], 1000)
for i in range(100):
    Sid.viruses.append(ResistantVirus(.1, .05, {'guttagonol': False}, .005))
drugs = ['guttagonol', 'tomonol']
#
# PROBLEM 2
#

def simulationWithDrug():
    """
    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    viruses, xValues, yAverage, yResistant = [], [], [], []
    for i in range(100):
        viruses.append(ResistantVirus(.1, .05, {'guttagonol':False}, .005))
    Sid = Patient(viruses, 1000)
    for i in range(150):
        yAverage.append(Sid.update())
        yResistant.append(Sid.getResistPop(['guttagonol']))
    Sid.addPrescription('guttagonol')
    for i in range(150):
        yAverage.append(Sid.update())
        yResistant.append(Sid.getResistPop(['guttagonol']))
    pylab.plot(yAverage, 'b-', yResistant, 'r-')
    pylab.title('Number of viruses in Sid over time')
    pylab.xlabel('Time steps')
    pylab.ylabel('Viruses')
    pylab.show()

#
# PROBLEM 3
#        

def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    trials = [0, 75, 150, 300]
    zero, seven_five, one_fifty, three_hundo = [], [], [], []
    master = {0 : zero, 75 : seven_five, 150 : one_fifty, 300 : three_hundo}
    for i in range(numTrials):
        zero.append(twelve_step_program(0))
        seven_five.append(twelve_step_program(75))
        one_fifty.append(twelve_step_program(150))
        three_hundo.append(twelve_step_program(300))
    return master
                
def genSid():
    viruses = []
    for i in range(100):
        viruses.append(ResistantVirus(.1, .05, {'guttagonol':False, 'grimpex' : False}, .005))
    Sid = Patient(viruses, 1000)
    return Sid

def finish_him(patient):
    for i in range(150):
        patient.update()

def twelve_step_program(time_steps):
    Sid = genSid()
    for i in range(time_steps):
        Sid.update()
##    print 'Resist population after ' + str(time_steps) + 'time steps: ' + str(Sid.getResistPop(['guttagonol']))
    Sid.addPrescription('guttagonol')
    finish_him(Sid)
    return len(Sid.viruses)

def genHisty(key):
##    pylab.xlim(0, 10)
    pylab.hist(master[key], 15)
    pylab.xlabel('Final number of viruses')
    pylab.ylabel('Number of patients')
    pylab.title('Fifty trials of beginning treatment after ' + str(key) + ' time-steps')
    pylab.show()

##master = simulationDelayedTreatment(40)
##for i in master.keys():
##    genHisty(i)

# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    trials = [0, 75, 150, 300]
    zero, seven_five, one_fifty, three_hundo = [], [], [], []
    master = {0 : zero, 75 : seven_five, 150 : one_fifty, 300 : three_hundo}
    for i in range(50):
        zero.append(dual_threat(0))
        seven_five.append(dual_threat(75))
        one_fifty.append(dual_threat(150))
        three_hundo.append(dual_threat(300))
    return master

def dual_threat(time_steps):
    Sid = genSid()
    for i in range(150):
        Sid.update()
    Sid.addPrescription('guttagonol')
    for i in range(time_steps):
        Sid.update()
    Sid.addPrescription('grimpex')
    finish_him(Sid)
    return len(Sid.viruses)

def gendoubleHisty(key):
    pylab.xlim(0, 10)
    pylab.hist(master[key], 10)
    pylab.xlabel('Final number of viruses')
    pylab.ylabel('Number of patients')
    pylab.title('Fifty trials of beginning treatment after ' + str(key) + ' time-steps')
    pylab.show()

#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    #TODO

## Sid's population levels off around 500 after seventy_five steps. The resistance
## ratio also levels off at 50% at that time. Introducing a drug quickly kills
## the population regardless of how much time it is allowed.
