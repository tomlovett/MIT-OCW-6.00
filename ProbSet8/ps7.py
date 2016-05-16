# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):
    def __init__(self, maxBirthProb, clearProb):
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def __str__(self):
        return 'Virus with maxBirthProb ' + str(self.maxBirthProb) + ' and' + \
        ' clearProb of ' + str(self.clearProb)

    def doesClear(self):
        if random.random() < self.clearProb:
            return True
        else:
            return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() < (self.maxBirthProb * (1-popDensity)):
            return True
##            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            return NoChildException()

class SimplePatient(object):
    def __init__(self, viruses, maxPop):
        self.viruses = viruses
        self.maxPop = maxPop
        self.popDensity = None

    def getTotalPop(self):
        return len(self.viruses)       

    def setpopDensity(self):
        self.popDensity = float(len(self.viruses))/self.maxPop

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        for v in self.viruses:
            if v.doesClear() is True:
                self.viruses.remove(v)
        self.setpopDensity()
        copylist = []
        for v in self.viruses:
            if v.reproduce(self.popDensity) is True:
                copylist.append(v)
        for v in copylist:
            self.viruses.append(SimpleVirus(v.maxBirthProb, v.clearProb))
        return self.getTotalPop()

#
# PROBLEM 2
#
def simulationWithoutDrug():

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    viruses, yValues, xValues = [], [], []
    for i in range(100):
        viruses.append(SimpleVirus(.1, .05)) # birthProb, clearProb
    sickSid = SimplePatient(viruses, 1000)
    for i in range(300):
        yValues.append(sickSid.update())
        xValues.append(i)
    pylab.plot(xValues, yValues)
    pylab.title('Viruses in Sick Sid over time')
    pylab.xlabel('Time steps')
    pylab.ylabel('Viruses')
    pylab.show()

##simulationWithoutDrug()

## Population stops growing at 500 virii. At that point the clear ratio of .05
## matches the computed birth ratio of .1 * (1 - popDensity(1/2))
##
##1.1 - 1/8
##1.2 - 1/8
##1.3 - 3/8
##1.4 - 4/8 or 1/2

##2. (1/6)**4 or 6/(6**5)

##3. Monte Carlo sim
1
def MC(trials):
    yahtzees = 0
    for i in range(trials):
        data = roll()
        rev = data[:]
        rev.reverse()
        if rev == data and data[:2] == data[2:4]:
            yahtzees += 1
    return yahtzees

def roll():
    data = []
    for i in range(6):
        data.append(random.randint(1,6))
    return data
    

def bigMC(trials):
    end = 0
    for i in range(trials):
        end += MC(77760)
    return end/float(trials *77760)
