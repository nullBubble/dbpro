from trajectory import trajectory
import sys

t = trajectory(3, sys.argv[1])

print("before")
print(t.getAvailableTrajectories())
for x in range(3):
    tr = t.getNextTraj()
    print(str(tr.size)+" from "+str(tr['SHIP_ID'].unique()))
    # print(tr['SHIP_ID'].unique())
print("after popping")
print(t.getAvailableTrajectories())