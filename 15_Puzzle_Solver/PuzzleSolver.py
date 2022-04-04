import time

class PrioQueue:
    def __init__(self, layout):
        self.prioQueue = [(layout, 0, 0)]
        self.stepTree = [("None", 0)]
        self.treeLastIdx = 0
        self.lastIdx = 0
        self.entryDict = {}

    def enqueue(self, nObj, nStep):
        layout_str = self.layout_to_str(nObj[0])
        # Cek apakah kondisi puzzle sudah pernah muncul
        if (layout_str not in self.entryDict):

            # Tambahin step di tree
            self.stepTree.append(nStep)
            self.treeLastIdx += 1

            # Tambahin node
            idx = self.get_insert_index(nObj[0], nObj[1])
            self.prioQueue.insert(idx, (nObj[0], nObj[1], self.treeLastIdx))

            self.entryDict[layout_str] = True

            self.lastIdx += 1

    def layout_to_str(self, layout):
        return ";".join(layout)

    def dequeue(self):
        self.lastIdx -= 1
        return self.prioQueue.pop(0)
    
    def g(self, P):
        res = 0
        for i in range(1, 17):
            if (str(i) != P[i - 1]):
                res += 1
        return res

    def get_insert_index(self, layout, fP):
        # Menggunakan binary search
        lBound = 0
        uBound = self.lastIdx
        if uBound < 0:
            return 0
        elL = self.prioQueue[(lBound + uBound) // 2]
        elHR = self.h(elL[1], elL[0])
        crHR  = self.h(fP, layout)
        while(lBound != uBound and elHR != crHR):
            if(elHR < crHR):
                lBound = (lBound + uBound) // 2 + 1
            elif (elHR > crHR):
                uBound = (lBound + uBound) // 2

            elL = self.prioQueue[(lBound + uBound) // 2]
            elHR = self.h(elL[1], elL[0])

        return lBound + (lBound <= crHR)

    def h(self, fP, layout):
        return fP + self.g(layout)

    def get_step(self, nObj):
        return self.stepTree[nObj[2]]

    def get_full_step(self, nIdx):
        # Mengambil langkah-langkah
        if nIdx == 0:
            return []
        else:
            step, pIdx = self.stepTree[nIdx]
            return self.get_full_step(pIdx) + [step]

    def show(self):
        for el in self.prioQueue:
            print(el[0], el[1], self.g(el[0]))

class PuzzleSolver:

    def solve(self, layout):
        st = time.time()
        self.prioQueue = PrioQueue(layout)

        nObj = self.prioQueue.dequeue()
        checkNum = 1
        print(f"Check Number: {checkNum}, Height: {nObj[1]}") # Logging

        # Diulang selama bukan solusi dan dibawah 5 menit
        while(self.g(nObj[0]) != 0 and time.time() - st < 300):
            self.gen_branch(nObj)
            nObj = self.prioQueue.dequeue()

            checkNum += 1
            print(f"Check Number: {checkNum}, Height: {nObj[1]}") # Logging

        # Langkah, Waktu Eksekusi, Apakah berhasil, jumlah simpul yang dieksekusi
        return (
            self.prioQueue.get_full_step(nObj[2]), 
            time.time() - st, 
            self.g(nObj[0]) == 0, 
            self.prioQueue.treeLastIdx + 1
        )

    def show(self):
        self.prioQueue.show();

    def gen_branch(self, nObj):
        layout, fP, sIdx = nObj
        child = self.gen_child(layout)
        for c in child:
            # Bukan lawan dari langkah sebelumnya
            # Contoh:
            #   Kalau sebelumnya Left, kali ini gak bisa Right
            if (c[1] != "None" and \
                self.prioQueue.get_step(nObj) != self.inv_mov(c[1])):
                self.prioQueue.enqueue((c[0], fP + 1, 0), (c[1], sIdx))

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
        # Membuat anak di segala arah
        xIdx = self.get_xIdx(layout)
        return  [self.gen_up(layout, xIdx)]    + \
                [self.gen_down(layout, xIdx)]  + \
                [self.gen_left(layout, xIdx)]  + \
                [self.gen_right(layout, xIdx)] 
