class LCG(object):
    def __init__(self, seed): 
        self.m = 16285270385112413720426683811263350667
        self.a = 313373133731337313373133731337 # 1103515245
        self.c = 123456789012345678901234567890
        self.x = seed

    def next(self):
        self.x = (self.a * self.x + self.c) % self.m
        return self.x  