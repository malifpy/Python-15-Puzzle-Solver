from os.path import exists

class Parser:
    def load_file(filename):
        f = open(filename, "r")
        res = f.read().split()
        print(res)
        return res

    def exist_check(filename):
        return exists(filename)

    def format_check(arr):
        l = len(arr)
        if(l != 16):
            return False
        else:
            for i in range(1, 17):
                if (str(i) not in arr):
                    return False
            return True

    def parse(filename):
        if(not Parser.exist_check(filename)):
            raise Exception("Error: File not Exist")

        l = Parser.load_file(filename)

        if(not Parser.format_check(l)):
            raise Exception("Error: Wrong Format")

        return l
