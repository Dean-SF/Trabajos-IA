from random import sample

class Stroke:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return str(self.value)

a = [Stroke(1), Stroke(2), Stroke(3)]
b = [Stroke(4), Stroke(5), Stroke(6)]

# Modify the second object in list a
a[1] = Stroke(b[1])

a[1].value = 2

# Print the second object in list b
print(a[1].value)  # Output: 20
print(b[1].value)  # Output: 20

print("-------------")
sisisi=sample(a,2)
print(sisisi)
print(a)
sisisi[0].value = 234143
print("-------------")
print(sisisi)
print(a)