# See http://ami.ektf.hu/uploads/papers/finalpdf/AMI_43_from29to41.pdf Eq. 2.1

# Curve: y^2 = x^3 + (400 + 120 -3)x^2 + 32 * 13 x
N = 10
k = 7
E = EllipticCurve([0, 517, 0, 416, 0])
P = E.point_search(k)[0] # E(-36, 780)
print(E)
print(P)

# Code to find k = 7 and m=13
lower_bound = -2 * (N+3) * (N - sqrt(N^2 - 4))
upper_bound = -4 * ((N+3)/(N+2))

# for j in range(20):
#    P = E.point_search(j)[0] # E(-36, 780)
#    for i in range(1000):
#        Pt = i*P
#        x = Pt[0]
#        y = Pt[1]
#        # check if abc would be positive
#        if lower_bound < x < upper_bound:
#            print("Found for ", j, " m =", i, Pt)
#            break

Pt = 13*P
x = Pt[0]
y = Pt[1]

assert lower_bound < x < upper_bound

# Map to solutions
a = ((8 * (N + 3)) - x + y) / (2*(4-x)*(N+3))
b = ((8 * (N + 3)) - x - y) / (2*(4-x)*(N+3))
c = (-4*(N+3) - (N + 2) * x) / ((4 - x) * (N+3))

# Turn rational solutions to integer ones
lcm_ = LCM([a.denominator(), b.denominator(), c.denominator()])
print(lcm_ * a)
print(lcm_ * b)
print(lcm_ * c) 



