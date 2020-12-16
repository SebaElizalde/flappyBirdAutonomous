LEFT = 0
TOP = 1
WIDTH = 2
HEIGHT = 3
JUMP = 4
JUMPSPEED = 5
GRAVITY = 6
DEAD = 7


class Conditions:
    def __init__(self, lowerBlock, upperBlock, bird):
        self.lowerBlock = lowerBlock
        self.upperBlock = upperBlock
        self.bird = bird

        self.farFromWall = 50 <= self.xDistanceToWall()
        self.closeToWall = 0 <= self.xDistanceToWall() < 50
        self.pastWall = self.xDistanceToWall() < 0

        self.farAboveGap = 150 <= self.yDistanceToGapCenter()
        self.closeAboveGap = 70 <= self.yDistanceToGapCenter() < 150
        self.gapTop = 23 <= self.yDistanceToGapCenter() < 70 # Gap / 3 = 140 / 3 ~= 46
        self.gapCentered = -23 < self.yDistanceToGapCenter() < 23
        self.gapBottom = -70 <= self.yDistanceToGapCenter() <= -23
        self.closeBelowGap = -150 <= self.yDistanceToGapCenter() < -70
        self.farBelowGap = self.yDistanceToGapCenter() < -150

        self.closeToCeiling = bird[TOP] < 30
        self.closeToFloor = bird[TOP] + bird[HEIGHT] > 690

        self.gravity = bird[GRAVITY]
        self.jump = bird[JUMP]
        self.jumpSpeed = bird[JUMPSPEED]
        self.risingSlow = self.jumpSpeed >= 5
        self.risingFast = 0 < self.jumpSpeed < 5
        self.fallingSlow = (-4 < self.jumpSpeed <= 0 and self.jump >= 0) or 0 <= self.gravity < 4
        self.fallingFast = (self.jumpSpeed <= -4 and self.jump >= 0) or 4 <= self.gravity
        self.dead = bird[DEAD]

    def xDistanceToWall(self):
        return self.upperBlock[LEFT] - (self.bird[LEFT] + self.bird[WIDTH])

    def yDistanceToGapCenter(self):
        gap = (self.lowerBlock[TOP] - (self.upperBlock[TOP] + self.upperBlock[HEIGHT]))
        assert gap == 140
        gapY = self.lowerBlock[TOP] - (gap / 2)
        return gapY - (self.bird[TOP] + (self.bird[HEIGHT] / 2)) #If minus, bird is below gap

    def isBirdBetweenWalls(self, lowerBlock, upperBlock, bird):
        return self.isInXRange(lowerBlock, upperBlock, bird) and self.isInYRange(lowerBlock, upperBlock, bird)

    def isInXRange(self, lowerBlock, upperBlock, bird):
        birdRight = bird[LEFT] + bird[WIDTH]
        if lowerBlock[LEFT] <= bird[LEFT] and (birdRight <= lowerBlock[LEFT] + lowerBlock[WIDTH]):
            if upperBlock[LEFT] <= bird[LEFT] and (
                    birdRight <= upperBlock[LEFT] + upperBlock[WIDTH]):  # actually redundant
                return True
        return False

    def isInYRange(self, lowerBlock, upperBlock, bird):
        birdBottom = bird[TOP] + bird[HEIGHT]
        if bird[TOP] > (upperBlock[TOP] + upperBlock[HEIGHT]) and birdBottom < lowerBlock[TOP]:
            return True
        return False

    def exclude(self, initialConditions):
        if initialConditions.farAboveGap is not None and self.farAboveGap != initialConditions.farAboveGap:
            self.farAboveGap = None
        if initialConditions.closeAboveGap is not None and self.closeAboveGap != initialConditions.closeAboveGap:
            self.closeAboveGap = None
        if initialConditions.gapTop is not None and self.gapTop != initialConditions.gapTop:
            self.gapTop = None
        if initialConditions.gapCentered is not None and self.gapCentered != initialConditions.gapCentered:
            self.gapCentered = None
        if initialConditions.gapBottom is not None and self.gapBottom != initialConditions.gapBottom:
            self.gapBottom = None
        if initialConditions.closeBelowGap is not None and self.closeBelowGap != initialConditions.closeBelowGap:
            self.closeBelowGap = None
        if initialConditions.farBelowGap is not None and self.farBelowGap != initialConditions.farBelowGap:
            self.farBelowGap = None
        if initialConditions.risingSlow is not None and self.risingSlow != initialConditions.risingSlow:
            self.risingSlow = None
        if initialConditions.risingFast is not None and self.risingFast != initialConditions.risingFast:
            self.risingFast = None
        if initialConditions.fallingSlow is not None and self.fallingSlow != initialConditions.fallingSlow:
            self.fallingSlow = None
        if initialConditions.fallingFast is not None and self.fallingFast != initialConditions.fallingFast:
            self.fallingFast = None
        if initialConditions.farFromWall is not None and self.farFromWall != initialConditions.farFromWall:
            self.farFromWall = None
        if initialConditions.closeToWall is not None and self.closeToWall != initialConditions.closeToWall:
            self.closeToWall = None
        if initialConditions.pastWall is not None and self.pastWall != initialConditions.pastWall:
            self.pastWall = None
        if initialConditions.dead is not None and self.dead != initialConditions.dead:
            self.dead = None

    def __eq2__(self, other):
        if not isinstance(other, Conditions):
            return NotImplemented
        return self.farAboveGap == other.farAboveGap \
                and self.closeAboveGap == other.closeAboveGap \
                and self.gapTop == other.gapTop \
                and self.gapCentered == other.gapCentered \
                and self.gapBottom == other.gapTop \
                and self.closeBelowGap == other.closeBelowGap \
                and self.farBelowGap == other.farBelowGap \
                and self.risingSlow == other.risingSlow \
                and self.risingFast == other.risingFast \
                and self.fallingSlow == other.fallingSlow \
                and self.fallingFast == other.fallingFast \
                and self.dead == other.dead \
                and self.farFromWall == other.farFromWall \
                and self.closeToWall == other.closeToWall \
                and self.pastWall == other.pastWall

    def __eq__(self, other):
        if not isinstance(other, Conditions):
            return NotImplemented
        if self.farAboveGap is not None and other.farAboveGap is not None and self.farAboveGap != other.farAboveGap:
            return False
        if self.closeAboveGap is not None and other.closeAboveGap is not None and self.closeAboveGap != other.closeAboveGap:
            return False
        if self.gapTop is not None and other.gapTop is not None and self.gapTop != other.gapTop:
            return False
        if self.gapCentered is not None and other.gapCentered is not None and self.gapCentered != other.gapCentered:
            return False
        if self.gapBottom is not None and other.gapBottom is not None and self.gapBottom != other.gapBottom:
            return False
        if self.closeBelowGap is not None and other.closeBelowGap is not None and self.closeBelowGap != other.closeBelowGap:
            return False
        if self.farBelowGap is not None and other.farBelowGap is not None and self.farBelowGap != other.farBelowGap:
            return False
        if self.risingSlow is not None and other.risingSlow is not None and self.risingSlow != other.risingSlow:
            return False
        if self.risingFast is not None and other.risingFast is not None and self.risingFast != other.risingFast:
            return False
        if self.fallingSlow is not None and other.fallingSlow is not None and self.fallingSlow != other.fallingSlow:
            return False
        if self.fallingFast is not None and other.fallingFast is not None and self.fallingFast != other.fallingFast:
            return False
        if self.dead is not None and other.dead is not None and self.dead != other.dead:
            return False
        if self.farFromWall is not None and other.farFromWall is not None and self.farFromWall != other.farFromWall:
            return False
        if self.closeToWall is not None and other.closeToWall is not None and self.closeToWall != other.closeToWall:
            return False
        if self.pastWall is not None and other.pastWall is None and self.pastWall != other.pastWall:
            return False
        return True
