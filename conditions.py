LEFT = 0
TOP = 1
WIDTH = 2
HEIGHT = 3
JUMP = 4
JUMPSPEED = 5
GRAVITY = 6


class Conditions:
    def __init__(self, lowerBlock, upperBlock, bird):
        xDistanceToWall = self.xDistanceToWall(upperBlock, bird)
        self.farFromWall = 50 <= xDistanceToWall
        self.closeToWall = 0 <= xDistanceToWall < 50
        self.pastWall = xDistanceToWall < 0

        self.yDistanceToGapCenter = self.yDistanceToGapCenter(lowerBlock, upperBlock, bird)
        self.aboveGap = 70 <= self.yDistanceToGapCenter
        self.gapTop = 23 <= self.yDistanceToGapCenter < 70 # Gap / 3 = 140 / 3 ~= 46
        self.gapCentered = -23 < self.yDistanceToGapCenter< 23
        self.gapBottom = -70 <= self.yDistanceToGapCenter <= -23
        self.belowGap = self.yDistanceToGapCenter < -70

        self.closeToCeiling = bird[TOP] < 30
        self.closeToFloor = bird[TOP] + bird[HEIGHT] > 690

        self.jump = bird[JUMP]
        self.risingSlow = bird[JUMPSPEED] >= 5
        self.risingFast = 0 < bird[JUMPSPEED] < 5
        self.fallingSlow = (-4 < bird[JUMPSPEED] <= 0 and self.jump >= 0) or 0 <= bird[GRAVITY] < 4
        self.fallingFast = (bird[JUMPSPEED] <= -4 and self.jump >= 0) or 4 <= bird[GRAVITY]

    def xDistanceToWall(self, upperBlock, bird):
        return upperBlock[LEFT] - (bird[LEFT] + bird[WIDTH]) #If minus, the bird is passing through the gap

    def yDistanceToGapCenter(self, lowerBlock, upperBlock, bird):
        gap = (lowerBlock[TOP] - (upperBlock[TOP] + upperBlock[HEIGHT]))
        assert gap == 140
        gapY = lowerBlock[TOP] - (gap / 2)
        return gapY - (bird[TOP] + (bird[HEIGHT] / 2)) #If minus, bird is below the gap center

    def exclude(self, initialConditions):
        if initialConditions.aboveGap is not None and self.aboveGap != initialConditions.aboveGap:
            self.aboveGap = None
        if initialConditions.gapTop is not None and self.gapTop != initialConditions.gapTop:
            self.gapTop = None
        if initialConditions.gapCentered is not None and self.gapCentered != initialConditions.gapCentered:
            self.gapCentered = None
        if initialConditions.gapBottom is not None and self.gapBottom != initialConditions.gapBottom:
            self.gapBottom = None
        if initialConditions.belowGap is not None and self.belowGap != initialConditions.belowGap:
            self.belowGap = None
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

    def __eq__(self, other):
        if not isinstance(other, Conditions):
            return NotImplemented
        if self.aboveGap is not None and other.aboveGap is not None and self.aboveGap != other.aboveGap:
            return False
        if self.gapTop is not None and other.gapTop is not None and self.gapTop != other.gapTop:
            return False
        if self.gapCentered is not None and other.gapCentered is not None and self.gapCentered != other.gapCentered:
            return False
        if self.gapBottom is not None and other.gapBottom is not None and self.gapBottom != other.gapBottom:
            return False
        if self.belowGap is not None and other.belowGap is not None and self.belowGap != other.belowGap:
            return False
        if self.risingSlow is not None and other.risingSlow is not None and self.risingSlow != other.risingSlow:
            return False
        if self.risingFast is not None and other.risingFast is not None and self.risingFast != other.risingFast:
            return False
        if self.fallingSlow is not None and other.fallingSlow is not None and self.fallingSlow != other.fallingSlow:
            return False
        if self.fallingFast is not None and other.fallingFast is not None and self.fallingFast != other.fallingFast:
            return False
        if self.farFromWall is not None and other.farFromWall is not None and self.farFromWall != other.farFromWall:
            return False
        if self.closeToWall is not None and other.closeToWall is not None and self.closeToWall != other.closeToWall:
            return False
        if self.pastWall is not None and other.pastWall is None and self.pastWall != other.pastWall:
            return False
        return True
