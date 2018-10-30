import numpy as np
import queue

q = queue.Queue()
interArrivalTimes = []
serviceTimes = []
arrivalTimes = []
averageWaitingTime = 0
averageJobDelayTime = 0
averageJobsWaitingInQueue = 0
serverBusy = False

totalSimulationTime = int(input("Enter Total Time(Hours): "))
jobArrivalRate = int(input("Enter IAT Rate(per Hour): "))
jobServiceRate = int(input("Enter ST Rate(per Hour): "))

numberOfProcesses = int(np.random.poisson(jobArrivalRate)*totalSimulationTime)

print("Number of Processes")
print(numberOfProcesses)

interArrivalTimes.append(0)

while not len(interArrivalTimes) == numberOfProcesses:
    temp = np.random.exponential(1/jobArrivalRate)*60*60
    if not temp < 1:
        interArrivalTimes.append(int(temp-temp%1))

while not len(serviceTimes) == numberOfProcesses:
    temp = np.random.exponential(1/jobServiceRate)*60*60
    if not int(temp-temp%1) < 1:
        serviceTimes.append(int(temp-temp%1))

for i in range(numberOfProcesses):
    if i == 0:
        arrivalTimes.append(0)
    else:
        arrivalTimes.append(arrivalTimes[i-1] + interArrivalTimes[i])

currentTime = 0
processesCompleted = 0
indexofProcessWhichWillArriveNext = 0
startTimeOfService = 0
indexBeingServiced = 0
rho = jobArrivalRate/jobServiceRate

while (currentTime < totalSimulationTime*60*60 and processesCompleted < numberOfProcesses):
    if indexofProcessWhichWillArriveNext < numberOfProcesses and currentTime == arrivalTimes[indexofProcessWhichWillArriveNext]:
        q.put(indexofProcessWhichWillArriveNext)
        indexofProcessWhichWillArriveNext = indexofProcessWhichWillArriveNext + 1
    if serverBusy == True:
        if currentTime == startTimeOfService + serviceTimes[indexBeingServiced]:
            serverBusy = False
            processesCompleted = processesCompleted + 1
    if serverBusy == False:
        if not q.empty():
            indexBeingServiced = q.get()
            serverBusy = True
            startTimeOfService = currentTime
            averageWaitingTime = averageWaitingTime + currentTime - arrivalTimes[indexBeingServiced]
            averageJobDelayTime = averageJobDelayTime + currentTime - arrivalTimes[indexBeingServiced] + serviceTimes[indexBeingServiced]
    currentTime = currentTime + 1
    averageJobsWaitingInQueue = averageJobsWaitingInQueue + q.qsize()

print("Avg waiting time")
print(averageWaitingTime/(numberOfProcesses*60*60))
print("Avg delay time")
print(averageJobDelayTime/(numberOfProcesses*60*60))
print("Avg jobs waiting")
print(averageJobsWaitingInQueue/currentTime)


print("Queuing theory")
print("Avg waiting time")
print(rho/((1-rho)*jobServiceRate))
print("Avg delay time")
print(1/((1-rho)*jobServiceRate))
print("Avg jobs waiting")
print((rho*rho)/(1-rho))