# coding=utf-8
from copy import deepcopy

HOLDING_KEY = True


class Theory:
    def __init__(self, conditions):
        self.initialConditions = conditions
        self.predictedEffects = None
        self.action = None
        self.P = None
        self.K = None
        self.utility = None

    def exclusion(self, theory):
        mutantTheory = deepcopy(self)
        mutantTheory.initialConditions.exclude(theory.initialConditions)
        return mutantTheory

    def getSameConditions(self, theories):
        sameConditionsTheories = []
        for theory in theories:
            if theory.initialConditions == self.initialConditions and theory != self:
                sameConditionsTheories.append(theory)
        return sameConditionsTheories

    def hasMoreSpecificConditions(self, theory):
        return False

    def getEqualTheories(self, theories):
        equalTheories = []
        for theory in theories:
            if theory.initialConditions == self.initialConditions and theory.action == self.action and theory.predictedEffects == self.predictedEffects and theory != self:
                equalTheories.append(theory)
        return equalTheories

    def getEqualOrMoreGenericTheories(self, theories):
        equalOrMoreGenericTheories = []
        for theory in theories:
            if (theory.initialConditions == self.initialConditions or theory.hasMoreSpecificConditions(self)) \
                    and theory.action == self.action \
                    and (theory.predictedEffects == self.predictedEffects or theory.hasMoreSpecificConditions(self.predictedEffects)) \
                    and theory != self:
                equalOrMoreGenericTheories.append(theory)
        return equalOrMoreGenericTheories

    def getSimilarTheories(self, theories):
        similarTheories = []
        for theory in theories:
            if theory.action == self.action and theory.hasMoreSpecificEffects(self.predictedEffects) and theory != self:
                similarTheories.append(theory)
        return similarTheories

    def hasMoreSpecificEffects(self, other):
        return self.predictedEffects == other

    def setPredictedEffects(self, conditions):
        self.predictedEffects = conditions
        self.calculateUtility()

    def calculateUtility(self):
        IC = self.initialConditions
        PE = self.predictedEffects
        self.utility = 0

        if PE.jump == 16:
            jumped = True
        else:
            jumped = False

        if IC.closeToCeiling:
            if not jumped:
                self.utility += 5
            else:
                self.utility -= 20
        elif IC.closeToFloor:
            if jumped:
                if IC.risingSlow:
                    self.utility += 5
                elif IC.risingFast:
                    self.utility += 2
            else:
                self.utility -= 20

        partialUtility = 0
        below = IC.yDistanceToGapCenter < 0
        if below:
            if jumped:
                if IC.gapCentered:
                    partialUtility -= 10
                elif IC.fallingFast:
                    partialUtility += 10
                elif IC.fallingSlow:
                    partialUtility += 5
                elif IC.risingSlow:
                    partialUtility += 3
                elif IC.risingFast:
                    partialUtility += 1
            else:
                if IC.risingFast:
                    partialUtility += 5
                elif IC.risingSlow:
                    partialUtility += 3
                elif IC.fallingSlow:
                    partialUtility -= 5
                elif IC.fallingFast:
                    partialUtility -= 10
        elif not below:
            if jumped:
                if IC.fallingFast:
                    partialUtility -= 10
                elif IC.fallingSlow:
                    partialUtility -= 8
                elif IC.risingSlow:
                    partialUtility -= 5
                elif IC.risingFast:
                    partialUtility -= 3
            else:
                if IC.fallingFast:
                    partialUtility += 3
                elif IC.fallingSlow:
                    partialUtility += 5
                elif IC.risingSlow:
                    partialUtility += 8
                elif IC.risingFast:
                    partialUtility += 10

        partialUtility = partialUtility
        self.utility += partialUtility
