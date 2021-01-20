def printDigits(filename,outFileName, num):
    f = open(filename, "r")
    w = open(outFileName, "w+")

    for i in range(num):
        line = f.readline().split(',')
        count = 0
        for pixel in line[:-1]:
            if int(pixel) == 0:
                w.write(' ')
            else:
               w.write('@')
            count += 1

            if count == 28:
                count = 0
                w.write("\n")
        w.write("\n" +line[-1])
    f.close()
    w.close()


printDigits("ddigits-testing-converted.txt","digits.txt", 100)