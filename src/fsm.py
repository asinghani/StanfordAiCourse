# Used for visualization
from graphviz import Digraph

class FSM:
    def __init__(self, states, initialState, linearTransitions = False, callback = lambda action, state, newState: None, failActionSilently = False, verbose = False):
        self.states = states
        self.currentState = initialState
        self.transitions = {}
        self.allTransitionCallback = callback
        self.failSilently = failActionSilently
        self.verbose = verbose
        self.enterCallbacks = {}
        self.exitCallbacks = {}

        # used for formatting verbose
        self.longestState = 1
        self.longestAction = 1

        # used for formatting verbose
        for state in states:
            if len(state) > self.longestState:
                self.longestState = len(state)

        if linearTransitions:
            for i in range(len(states)):
                addTransition("next", states[i], states[(i + 1) % len(states)])

        if not (self.currentState in self.states):
            raise ValueError("Initial state must be in states")

    def setEnterCallback(self, state, callback):
        self.enterCallbacks[state] = callback

    def setExitCallback(self, state, callback):
        self.exitCallbacks[state] = callback

    # used for formatting verbose
    def _leftPad(self, string, finalLen):
        if len(string) < finalLen:
            return (" " * (finalLen - len(string))) + string

        return string

    def addTransition(self, action, state, newState,
            beforeChange = lambda action, state, newState: None,
            afterChange = lambda action, state, newState: None):

        # used for formatting verbose
        if len(action) > self.longestAction:
            self.longestAction = len(action)

        if (state not in self.states):
            raise ValueError("State "+state+" not in states list")

        if not callable(newState):
            if (newState not in self.states):
                raise ValueError("State "+newState+" not in states list")

        if not (action in self.transitions):
            self.transitions[action] = {}

        if state in self.transitions[action]:
            raise ValueError("State "+state + "and action " + action + " already in transitions")
        else:
            self.transitions[action][state] = {"newState": newState,
                    "beforeChange": beforeChange, "afterChange": afterChange}

    def addMultipleTransitions(self, action, initialStates, newState,
            beforeChange = lambda action, state, newState: None,
            afterChange = lambda action, state, newState: None):

        for state in initialStates:
            self.addTransition(action, state, newState, beforeChange, afterChange)

    def runAction(self, action):
        if (action not in self.transitions) or (self.currentState not in self.transitions[action]):
            if not self.failSilently:
                raise ValueError("No transition found for state "+self.currentState+" and action "+action)
        else:
            transition = self.transitions[action][self.currentState]
            previousState = self.currentState + ""
            newState = transition["newState"]
            newState = newState() if callable(newState) else newState

            if self.verbose:
                print("Transition: Action = {}    Prev State = {}    New State = {}"
                        .format(self._leftPad(action, self.longestAction), self._leftPad(previousState, self.longestState), self._leftPad(newState, self.longestState)))

            transition["beforeChange"](action, self.currentState, newState)
            if self.currentState in self.exitCallbacks:
                self.exitCallbacks[self.currentState]()

            self.currentState = newState
            transition["afterChange"](action, previousState, newState)
            if self.currentState in self.enterCallbacks:
                self.enterCallbacks[self.currentState]()

            self.allTransitionCallback(action, previousState, newState)

    def next(self):
        self.runAction("next")

    def getState(self):
        return self.currentState

    def makeVis(self):
        f = Digraph("fsm", filename="fsm.gv")
        f.attr(rankdir="LR", size="8,5")
        for action in self.transitions:
            for initialState in self.transitions[action]:
                finalState = self.transitions[action][initialState]["newState"]
                finalState = finalState() if callable(finalState) else finalState
                f.edge(initialState, finalState, action)

        print("Rendered to " + f.render())
