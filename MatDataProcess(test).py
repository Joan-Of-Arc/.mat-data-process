import scipy.io as scio

class MatDataProcess:
    """ 处理mat数据, 返回附带测量角度的信息 """
    def __init__(self, mat) -> None:
        """ 
        初始化传入一个mat对象(文件路径), 先对all_label进行划分 
        self.data 为读取的mat文件
        devide 为该mat文件的分割, 其中:
        devide[0] 中是目标种类
        devide[1] 为目标种类对应的范围
        """
        self.data = scio.loadmat(mat)
        kind, devide, bound = [], [], []

        data_label = self.data["a"]  # 获得mat文件里的label
        for i, _ in enumerate(data_label):
            if i == 0: continue
            if data_label[i - 1][0] != data_label[i][0]:
                kind.append(int(data_label[i - 1]))
                devide.append(i - 1)
        kind.append(int(data_label[-1]))
        devide.append(len(data_label) - 1)

        bound.append(devide[0] + 1)
        for i in range(1, len(devide)):
            bound.append(devide[i] - devide[i - 1])

        self.kind = kind
        self.devide = devide
        self.bound = bound
        self.len = len(data_label)
        self.cnt = 0
        # self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        # print(self.cnt)
        cnt = self.cnt
        data_data = self.data["b"]
        if cnt >= self.len: raise StopIteration

        cur = 0
        for i, n in enumerate(self.devide):
            if cnt > n: 
                cur = n
                continue
        if cur: cnt -= cur + 1
        # 角度范围为 0 - 350
        angle = int((((cnt / self.bound[i]) * 360) // 10) * 10)
        cur = data_data[self.cnt]
        self.cnt += 1
        return (cur, angle)



if __name__ == "__main__":
    data = "testdata.mat"
    M = MatDataProcess(data)
    print(M.devide, M.kind, M.bound, len(M.data["b"]))
    for m in M: 
        print(m[0], m[1])

    


