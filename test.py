import scipy.io as scio

datafile = "a2h1.mat"
data = scio.loadmat(datafile)
# print(type(data["all_label"]))
# print(data["all_label"].shape)
# print(data["all_data"].shape)

all_data = data["all_data"]
all_label = data["all_label"]

print(all_label.shape)
print(all_label[2440])

ans = [(0, 0)]
for i, n in enumerate(all_label):
    if i == 0: continue
    if all_label[i - 1][0] != all_label[i][0]:
        ans.append((int(all_label[i]), i))







print(ans)
