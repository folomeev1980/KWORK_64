import os

path = "R:/0_TBS_/Temp/copyLogs"
# for j in os.listdir(path):
#     print(j)


dictionary = {}
for k in range(1, 200):
    dictionary[k] = []

# print(dictionary)
file_names = ["00_segd_from_tape1",
              "00_segd_from_tape2",
              "00_segd_from_tape3",
              "08_SEGY_NAVMERGE",
              "08_d__check_tape1"
              ]


def last_log(flow_name):
    segy_check_tape1 = []
    for j in os.listdir(path):

        if j.split(".")[0] == flow_name:
            segy_check_tape1.append(j)

    return (int(segy_check_tape1[-1].split(".")[1][5:]), segy_check_tape1[-1])


def separator(s,n):
    temp = []
    s = s.strip().split(" ")
    for i in s:
        if i != '':
            temp.append(i)
    temp = [temp[0], int(temp[1]), int(temp[2])]
    return temp[0:n]


for file_name in file_names:
    temp = last_log(file_name)
    dictionary[temp[0]].append(path + "/" + temp[1])

print(dictionary)

for i in range(1,100):
    print(i%3+1)

# with open(dictionary[1][0],"r") as f:
#     for l in f:
#         if "ILINE..............." in l:
#             print(separator(l,3))
#         if "XLINE..............." in l:
#             print(separator(l,3))
#         if "SEQWL..............." in l:
#             print(separator(l,3))
#
