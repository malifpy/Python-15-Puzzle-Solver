import time

class PrioQueue:
    def __init__(self, layout):
        self.prioQueue = [(layout, 0, [])]
        self.entryDict = {}

    def enqueue(self, obj):
        layout_str = self.layout_to_str(obj[0])
        if (layout_str not in self.entryDict):
            idx = self.get_insert_index(obj[0], obj[1])
            self.prioQueue.insert(idx, obj)
            self.entryDict[layout_str] = True

    def layout_to_str(self, layout):
        return ";".join(layout)

    def dequeue(self):
        return self.prioQueue.pop(0)
    
    def g(self, P):
        res = 0
        for i in range(1, 17):
            if (str(i) != P[i - 1]):
                res += 1
        return res

    def get_insert_index(self, layout, fP):
        idx = 0
        for el in self.prioQueue:
            if(el[1] + self.g(el[0]) >= fP + self.g(layout)):
                break
            idx += 1
        return idx

    def show(self):
        for el in self.prioQueue:
            print(el[0], el[1], self.g(el[0]))

class PuzzleSolver:

    def solve(self, layout):
        st = time.time()
        self.prioQueue = PrioQueue(layout)

        l, fP, steps = self.prioQueue.dequeue()
        checkNum = 1
        print(f"Check Number: {checkNum}, Height: {fP}")
        while(self.g(l) != 0 and checkNum < 7500):
            self.gen_branch((l, fP, steps))
            l, fP, steps = self.prioQueue.dequeue()

            checkNum += 1
            print(f"Check Number: {checkNum}, Height: {fP}")

        return (steps, time.time() - st, self.g(l) == 0)

    # def solveRec(self):
    #     layout, fP, steps = self.prioQueue.dequeue()
    #     while(self.g(layout) != 0):
    #         self.gen_branch((layout, fP, steps))
    #         layout, fP, steps = self.prioQueue.dequeue()
        
    def show(self):
        self.prioQueue.show();

    def gen_branch(self, obj):
        layout, fP, steps = obj
        child = self.gen_child(layout)
        for c in child:
            if (c[1] != "None" and not self.is_inv_last_step(c[1], steps)):
                self.prioQueue.enqueue((c[0], fP + 1, list(steps) + [c[1]]))

    def is_inv_last_step(self, step, steps):
        if (not steps):
            return False
        else:
            return self.inv_mov(step) == steps[-1]

    def inv_mov(self, mov):
        if(mov == "Up"):
            return "Down"
        elif (mov == "Down"):
            return "Up"
        elif (mov == "Right"):
            return "Left"
        elif (mov == "Left"):
            return "Right"
        else:
            return mov

    def get_xIdx(self, layout):
        for idx, item in enumerate(layout):
            if item == "16":
                return idx
        return -1

    def g(self, P):
        res = 0
        for i in range(1, 17):
            if (str(i) != P[i - 1]):
                res += 1
        return res

    # def heuristic(self, layout, fP):
    #     return fP + self.g(layout)

    def swap(self, layout, xA, xB):
        tmp = layout[xA]
        layout[xA] = layout[xB]
        layout[xB] = tmp

    def gen_up(self, layout, xIdx):
        if(xIdx // 4 != 0):
            newLayout = list(layout)
            nLoc = xIdx - 4
            nTag = self.swap(newLayout, xIdx, nLoc)
            return (newLayout, "Up")
        return ([], "None")

    def gen_down(self, layout, xIdx):
        if(xIdx // 4 != 3):
            newLayout = list(layout)
            nLoc = xIdx + 4
            nTag = self.swap(newLayout, xIdx, nLoc)
            return (newLayout, "Down")
        return ([], "None")

    def gen_right(self, layout, xIdx):
        if(xIdx % 4 != 3):
            newLayout = list(layout)
            nLoc = xIdx + 1
            nTag = self.swap(newLayout, xIdx, nLoc)
            return (newLayout, "Right")
        return ([], "None")

    def gen_left(self, layout, xIdx):
        if(xIdx % 4 != 0):
            newLayout = list(layout)
            nLoc = xIdx - 1
            nTag = self.swap(newLayout, xIdx, nLoc)
            return (newLayout, "Left")
        return ([], "None")

    def gen_child(self, layout):
        xIdx = self.get_xIdx(layout)
        return  [self.gen_up(layout, xIdx)]    + \
                [self.gen_down(layout, xIdx)]  + \
                [self.gen_left(layout, xIdx)]  + \
                [self.gen_right(layout, xIdx)] 
#
# # l = [2, 3, 4, 16, 1, 5, 6, 7, 10, 11, 12, 8, 9, 13, 14, 15]
# # l = [1, 2, 3, 4, 5, 10, 6, 8, 9 ,14, 7, 11, 13, 15, 12, 16]
# # l = [2, 9, 3, 4, 8, 1, 10, 12, 13, 16, 5, 7, 14, 11, 6, 15]
# # layout = [str(i) for i in l]
# # layout = ['2', '3', '4', '8', '1', '5', '10', '12', '9', '7', '16', '6', '13', '14', '11', '15']
# # layout = ['3', '16', '4', '8', '2', '5', '7', '12', '1', '6', '10', '15', '9', '13', '14', '11']
# layout = ['1', '7', '2', '4', '6', '3', '11', '8', '5', '10', '9', '12', '13', '14', '16', '15']
# ps = PuzzleSolver()
# print(ps.solve(layout))
