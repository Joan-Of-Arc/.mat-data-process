import scipy.io as scio

class MatDataProcess:
    """ 处理mat数据, 返回附带测量角度的信息 """
    def __init__(self, data, data_key, label_key) -> None:
        """ 初始化传入一个mat对象(文件路径), 先对all_label进行划分 """
        self.data = scio.loadmat(data)
        self.data_key = data_key
        self.label_key = label_key

        # 做数据的预处理
        kind, devide, numbers = [], [], []
        data_label = self.data[self.label_key]  # 获得mat文件里的label
        for i, _ in enumerate(data_label):
            if i == 0: continue
            if data_label[i - 1][0] != data_label[i][0]:
                kind.append(int(data_label[i - 1]))
                devide.append(i - 1)
        kind.append(int(data_label[-1]))  # 不同种类出现的先后顺序
        devide.append(len(data_label) - 1)  # 每个种类的右边界
        numbers.append(devide[0] + 1)  # 每个种类的数目
        for i in range(1, len(devide)):
            numbers.append(devide[i] - devide[i - 1])

        self.kind = kind
        self.devide = devide
        self.numbers = numbers
        # 以下两项用作迭代器的计数
        self.len = len(data_label)  
        self.cnt = 0

    def __iter__(self):
        return self

    def __next__(self):
        """ 定义迭代时的方法 """
        cnt = self.cnt  # 目前读到的行数
        data_data = self.data[self.data_key]  # 获取到数据
        if cnt >= self.len: 
            raise StopIteration  # 迭代终止
        
        # 以下为角度计算
        cur = 0
        for i, n in enumerate(self.devide):
            if cnt > n: 
                cur = n
                continue
        if cur: cnt -= cur + 1
        # 角度范围为 0 - 350, 以10°为间隔将同一类的数据进行连续划分
        angle = int((((cnt / self.numbers[i]) * 360) // 10) * 10)
        cur = data_data[self.cnt]
        self.cnt += 1
        # 将角度与原数据打包返回
        return (cur, angle)

if __name__ == "__main__":
    data = "a2h1.mat"
    M = MatDataProcess(data, "all_data", "all_label")
    print(M.devide, M.kind, M.numbers, len(M.data[M.label_key]))
    cnt = 0
    for m in M: 
        if cnt >= 80: break
        print(m[1])
        cnt += 1
    


