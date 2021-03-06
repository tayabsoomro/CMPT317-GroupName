from problemState import State, Vehicle, Package
from dataStructures import HashableDictionary
from searchNode import SearchNode
import copy


"""
    Problem class that defines the blueprint for the problems used in the MNKY
    problem. The class also contains methods to read a problem from standard
    input, return successors of a particular state, and a method for checking
    whether a given state is the goal state.

    Authors: Mahmud Ahzam*, Tayab Soomro*, Flaviu Vadan*
    Class: CMPT317
    Instructor: Michael Horsch
    Assignment: 1

    * - all authors equally contributed to the implementation
"""

class Problem():
    """ Problem Class """
    m = None
    n = None
    k = None
    y = None
    initState = None

    def __init__(self, _m, _n, _k, _y, packs):
        """
        Initializes a problem.
        :param _m: number of vehicles.
        :param _n: number of packages.
        :param _k: capacity of each vehicle.
        :param _y: dimension of the space.
        """
        self.m = _m
        self.n = _n
        self.k = _k
        self.y = _y
        vehicles = HashableDictionary("VEHICLES")
        packages = HashableDictionary("PACKAGES")
        for i in range(_m):
            vehicles[i] = Vehicle(tuple([0 for i in range(_y)]), i, _k)
        for j in range(len(packs)):
            packages[j] = Package(packs[j][0], packs[j][1], j, None)
        self.initState = State(vehicles, packages)

    def getInitState(self):
        """
        Return current state.
        :return: state.
        """
        return SearchNode(self.initState, None, "Begin\n")

    def readProblem():
        """
        Reads a problem from standard input.
        Input format: <m>
                      <n>
                      <k>
                      <y>
                      s11 s12 s13 ... s1y | d11 d12 d13 ... d1y
                      s21 s22 s23 ... s2y | d21 d22 d23 ... d2y
                      ...
                      ...
                      sn1 sn2 sn3 ... sny | dn1 dn2 dn3 ... dny
        """
        m = int(input())
        n = int(input())
        k = int(input())
        y = int(input())
        packages = []
        for i in range(n):
            interm = list(map(float,input().strip().split(' ')))
            src = tuple(interm[0:int(len(interm)/2)])
            des =  tuple(interm[int(len(interm)/2):len(interm)])
            packages.append((src, des))

        return Problem(m, n, k, y, packages)

    def successors(self, node):
        """
        Set of possible transitions from the current state.
        :return: list of all possible states.
        """

        possibleSuccessors = []
        for k1, v in node.getState().getVehicles().items():
            for k2, p in node.getState().getPackages().items():

                # Vehicle is not carrying this package and it has no more room:
                if p.carrier() != v.getIndex() and v.getRoom() <= 0:
                    # it can neither pickup this package nor deliver it:
                    continue

                # First, cover the case when you can deliver something
                # For each package picked up by/moving with v:
                else:
                    if p.carrier() == v.getIndex():
                        # Change copied state to reflect a delivery:
                        currVehicle = Vehicle(p.getDestination(),\
                                                v.getIndex(), v.getRoom() + 1)
                        vehicles = node.getState().getVehicles().clone()
                        vehicles[v.getIndex()] = currVehicle

                        # Make sure that no vehicle carries beyond capacity:
                        assert(currVehicle.getRoom() <= self.k)
                        assert(currVehicle.getRoom() >= 0)

                        packages = node.getState().getPackages().clone()
                        packages.pop(p.getIndex())
                        # Append to list of possible states:
                        planStep = "V" + str(v.getIndex()) + " delivers " +\
                            "P" + str(p.getIndex()) + "\n"
                        newNode = SearchNode(State(vehicles,packages),node,
                                                planStep)
                        possibleSuccessors.append(newNode)

                    # If the vehicle can pick up more packages:
                    elif (v.getRoom() > 0) and (p.carrier() is None):
                        # Change copied state to reflect a pick up of package
                        # p by v:
                        currVehicle = Vehicle(p.getPosition(),\
                                                v.getIndex(), v.getRoom() - 1)
                        vehicles = node.getState().getVehicles().clone()
                        vehicles[v.getIndex()] = currVehicle

                        # Make sure that no vehicle carries beyond capacity:
                        assert(currVehicle.getRoom() <= self.k)
                        assert(currVehicle.getRoom() >= 0)

                        # Set package as carried
                        pickUp = Package(p.getPosition(),p.getDestination(),
                                            p.getIndex(),v.getIndex())
                        packages = node.getState().getPackages().clone()
                        packages[p.getIndex()] = pickUp

                        planStep = "V" + str(v.getIndex()) + " picks up " +\
                            "P" + str(p.getIndex()) + "\n"

                        newNode = SearchNode(State(vehicles,packages),node,
                                                planStep)

                        # Append to the list of possible states:
                        possibleSuccessors.append(newNode)

            # Vehicle is empty, an option is to go back to origin:
            if v.getRoom() == self.k\
                    and v.getPosition() != tuple([0 for x in range(self.y)]):
                # Define origin
                garage = tuple([0 for x in range(self.y)])
                currVehicle = Vehicle(garage, v.getIndex(),v.getRoom())
                vehicles = node.getState().getVehicles().clone()
                vehicles[v.getIndex()] = currVehicle
                packages = node.getState().getPackages().clone()
                planStep = "V" + str(v.getIndex()) + " returns to origin\n"
                newNode = SearchNode(State(vehicles,packages), node, planStep)
                # Append state to the possible successor
                possibleSuccessors.append(newNode)
        return possibleSuccessors

    def isGoal(self, state):
        """
        Returns whether the given state is the goal state.
        :param state: a State.
        :return: true if goal state, false otherwise.
        """
        origin = tuple([0 for i in range(self.y)])
        for k, v in state.getVehicles().items():
            if v.getPosition() != origin:
                return False
        if len(state.getPackages()) != 0:
            return False
        return True

    def __str__(self):
        """  String representation of Problem """
        return "(M, N, K, Y) := " + str((self.m, self.n, self.k, self.y)) +\
            "\n" + "Initial State:\n" + str(self.initState)

    def getValues(self):
        """ String representation of the current values used """
        return("(M, N, K, Y) := " + str((self.m, self.n, self.k, self.y)))
