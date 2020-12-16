# coding=utf-8
import random

from conditions import Conditions
from flappybird import FlappyBird
from theory import Theory

LOWER_BLOCK = 0
UPPER_BLOCK = 1
BIRD = 2

HOLDING_KEY = True

class Agent:
    def __init__(self):
        self.theories = []
        self.flappybird = FlappyBird(self.theories)
        self.localTheory = None
        self.usedTheory = None

    def init(self):
        pass

    def act(self, action):
        if action is HOLDING_KEY:
            self.flappybird.holdKeyDown()
        elif action is not HOLDING_KEY:
            self.flappybird.releaseKey()
        else:
            raise Exception("was null action")

    def explore(self):
        return random.randint(0, 2 + self.flappybird.counter / 4) <= 2 #TODO cambiar por cant de ciclos

    def observeWorld(self):
        positions = self.flappybird.getWorldPositionObjets().tolist()
        bird = positions[BIRD] + [self.flappybird.jump, self.flappybird.jumpSpeed, self.flappybird.gravity, self.flappybird.dead]
        return [positions[LOWER_BLOCK], positions[UPPER_BLOCK], bird, self.flappybird.counter]

    def adjustUsedTheory(self, conditions):
        if self.localTheory is not None: #Completo la teoría local armada en el ciclo anterior, si la hay
            self.localTheory.setPredictedEffects(conditions)
            equalTheories = self.localTheory.getEqualTheories(self.theories)
            for theory in equalTheories: #Si hay teorias iguales las refuerzo y termino
                theory.P += 1
                theory.K += 1
            else: #No hay teorias iguales, busco similares
                similarTheories = self.localTheory.getSimilarTheories(self.theories)
                for theory in similarTheories: #Si hay similares aplico heuristica de exclusion
                    mutantTheory = theory.exclusion(self.localTheory)
                    equalTheoriesToMutant = mutantTheory.getEqualTheories(self.theories)
                    if len(equalTheoriesToMutant) == 0:
                        self.theories.append(mutantTheory)
                # Agrego la nueva teoría al conjunto
                self.localTheory.P = 1
                self.localTheory.K = 1
                self.theories.append(self.localTheory)
        elif self.usedTheory is not None: #Sino, ajusto la teoría utilizada
            if self.usedTheory.predictedEffects == conditions: #Pasó lo predecido, refuerzo la teoría
                self.usedTheory.P += 1
            else: #No pasó lo predecido, creo una nueva teoria y olvido la vieja si tiene baja tasa de exito o menor utilidad
                newTheory = Theory(self.usedTheory.initialConditions)
                newTheory.action = self.usedTheory.action
                newTheory.setPredictedEffects(conditions)
                newTheory.P = 1
                newTheory.K = 1
                self.theories.append(newTheory)
                if self.usedTheory.P / self.usedTheory.K < 0.1 or newTheory.utility > self.usedTheory.utility:
                    self.theories.remove(self.usedTheory)
        else: #Es la primera iteración
            return

    def run(self):
        self.flappybird.initGame()
        cycleCounter = -1
        while True:
            cycleCounter += 1
            #if cycleCounter % 5 != 0:
                #continue
            self.flappybird.eachCicle()
            situation = self.observeWorld()
            conditions = Conditions(situation[LOWER_BLOCK], situation[UPPER_BLOCK], situation[BIRD])
            self.adjustUsedTheory(conditions)

            #Decido que hacer en este ciclo
            self.localTheory = Theory(conditions)
            sameConditionsTheories = self.localTheory.getSameConditions(self.theories)
            if len(sameConditionsTheories) == 0: #No hay teoría, decido al azar
                if random.randint(0, 1) == 0:
                    self.act(HOLDING_KEY)
                    self.localTheory.action = HOLDING_KEY
                else:
                    self.act(not HOLDING_KEY)
                    self.localTheory.action = not HOLDING_KEY
                continue
            #Hay teorías, estan todas las acciones exploradas?
            actions = [0, 0]
            maximumUtilityTheory = sameConditionsTheories[0]
            for theory in sameConditionsTheories:
                if theory.action is HOLDING_KEY:
                    actions[0] += 1
                if theory.action is not HOLDING_KEY:
                    actions[1] += 1
                if theory.utility > maximumUtilityTheory.utility:
                    maximumUtilityTheory = theory
            if actions[0] == 0 and self.explore(): #No se que pasa si salto
                self.act(HOLDING_KEY)
                self.localTheory.action = HOLDING_KEY
            elif actions[1] == 0 and self.explore(): #No se que pasa si NO salto
                self.act(not HOLDING_KEY)
                self.localTheory.action = not HOLDING_KEY
            else: #Todas las acciones están exploradas o no quiso explorar, tomo la teoría de mayor utilidad
                self.localTheory = None
                self.usedTheory = maximumUtilityTheory
                self.act(self.usedTheory.action)
                self.usedTheory.K += 1
