file1 = open('test.py', 'r')
lines = file1.readlines()

count = 0
# Strips the newline character
for line in lines:
    count += 1
    print("Line{}: {}".format(count, line))