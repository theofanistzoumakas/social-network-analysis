import copy
import math
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


def floyd_warshcall(graph):
    V = len(graph)
    for i in range(V):
        for j in range(V):
            if i == j:
                graph[i][j] = 0
            elif i != j and graph[i][j] != 1:
                graph[i][j] = 9999

    for i in range(V):
        for j in range(V):
            for k in range(V):
                graph[j][k] = min(graph[j][k], graph[j][i] + graph[i][k])
    return graph


f = open("your_source_file", "r")
print("Give N: ")
N = int(input())
t_min = int(f.readline().split()[2])
t_max = int(f.readlines()[-1].split()[2])
print("t min is: ", t_min, ", t max is: ", t_max)
f.close()
dt = int((t_max - t_min) / N)

print("Dt is: ", dt)

f = open("your_source_file", "r")

dataset = []
dataset.append([])
counter = 1
times = [t_min]
for line in f:

    t = int(line.split()[2])
    if t < t_min + counter * dt:
        dataset[-1].append(line)
    else:
        while t > t_min + counter * dt:
            times.append(t_min + counter * dt)
            dataset.append([])
            counter += 1
        dataset[-1].append(line)
    #Για υπολογιστική απλούστευση λαμβάνονται υπόψη τα δεδομένα μόνο των 3 + 1 πρώτων χρονικών περιόδων
    #Η 4η Χρονική Περίοδος δεν είναι ολόκληρη και για αυτό δε λαμβάνεται τελικά υπόψη
    if counter >= 4:
        times.append(t_min + counter * dt)
        break
f.close()
#Αφαίρεση της 4ης χρονικής περιόδου
times.pop()
dataset.pop()
print("The timesstamps are:", times)


e_list = []
v_list = []
for sublist in dataset:
    e_list.append([])
    v_list.append([])
    for line in sublist:
        source_node = int(line.split()[0])
        target_node = int(line.split()[1])
        e_list[-1].append((source_node, target_node))
        v_list[-1].append(source_node)
        v_list[-1].append(target_node)
    v_list[-1] = list(set(v_list[-1]))

dataset = []
arrays = []

for selected_node_list, selected_edge_list in zip(v_list, e_list):
    arrays.append([])
    for node in selected_node_list:
        rows = []
        for node in selected_node_list:
            rows.append(0)
        arrays[-1].append(rows)

    for (i, j) in selected_edge_list:
        position_1 = selected_node_list.index(i)
        position_2 = selected_node_list.index(j)
        arrays[-1][position_1][position_2] = 1
        arrays[-1][position_2][position_1] = 1

print("The adjacency matrices are:")
matrcices_counter = 0
for i in arrays:
    print("---------------------------Matrix,", matrcices_counter)
    for row in i:
        print(row)
    matrcices_counter += 1
    print("\n")
print("---------------------------End-of-adjacency-matrices---------------------------")

arrays1 = copy.deepcopy(arrays)
arrays2 = copy.deepcopy(arrays)
arrays3 = copy.deepcopy(arrays)

degree_centralities_all = []
for a in arrays:
    degree_centralities = []
    max_value = len(a)-1
    for rows in a:
        sum_ = rows.count(1)
        degree_centralities.append(sum_ / max_value)
    degree_centralities_all.append(degree_centralities)


closeness_centrlity_all = []

for a in arrays1:
    a = floyd_warshcall(a)
    max_value = len(a)-1
    result = []
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] == 9999:
                a[i][j] = 0
        if (sum(a[i]) == 0):
            result.append(9999)
        else:
            result.append(max_value / sum(a[i]))
    closeness_centrlity_all.append(result)


betweness_centrlity_all = []

for a in arrays2:
    a = floyd_warshcall(a)
    number_of_v = len(a)
    betweness_centrlity = []
    for v in range(number_of_v):
        counter = 0
        counter2 = 0
        for i in range(number_of_v):
            if i == v:
                continue
            for j in range(number_of_v):
                if j == v:
                    continue

                if a[i][j] != 9999:
                    counter += 1

                    if a[i][j] == a[i][v] + a[v][j]:
                        counter2 += 1
        betweness_centrlity.append(counter2 / counter)
    betweness_centrlity_all.append(betweness_centrlity)

eigenvector_centrlity_all = []
for a in arrays3:
    number_of_v = len(a)
    if number_of_v == 0:
        eigenvector_centrlity_all.append([])
        continue
    e = []
    e_prev = []
    for i in range(number_of_v):
        e.append(1)
        e_prev.append(10000)
    e_arr = np.array(e)
    e_prev_arr = np.array(e_prev)
    sum2 = 10000
    while sum2 > 0.01:
        a_arr = np.array(a)
        e_prev_arr = e_arr
        e_arr = a_arr @ e_arr
        sum_ = 0
        for i in e_arr:
            sum_ += pow(i, 2)
        sum_ = math.sqrt(sum_)
        e_arr = (1 / sum_) * e_arr
        sum2 = 0
        for i, j in zip(e_arr, e_prev_arr):
            sum2 += pow(i - j, 2)
        sum2 = math.sqrt(sum2)
    eigenvector_centrlity_all.append(e_arr)

katz_centrlity_all = []
for A in arrays:
    number_of_v = len(A)
    if number_of_v == 0:
        katz_centrlity_all.append([])
        continue
    l = np.max(np.linalg.eigvals(A)).real
    a = random.uniform(0, 1 / l)
    b = np.ones(number_of_v)
    k_arr = np.ones(number_of_v)
    sum_ = 10000
    while sum_ > 0.01:
        k_prev = k_arr
        k_arr = a * (A @ k_arr) + b
        sum_ = 0
        for i, j in zip(k_arr, k_prev):
            sum_ += pow(i - j, 2)
        sum_ = math.sqrt(sum_)
    katz_centrlity_all.append(k_arr)

plt.hist(degree_centralities_all[0], color='green')
plt.title(label='degree centralities for T0')
plt.show()
plt.hist(closeness_centrlity_all[0], color='red')
plt.title(label='closeness centralities for T0')
plt.show()
plt.hist(betweness_centrlity_all[0], color='orange')
plt.title(label='betweness centralities for T0')
plt.show()
plt.hist(eigenvector_centrlity_all[0], color='yellow')
plt.title(label='eigenvector centralities for T0')
plt.show()
plt.hist(katz_centrlity_all[0])
plt.title(label='katz centralities for T0')
plt.show()

E_star_all = []
V_star_all = []
time_counter = 0
for i in range(len(v_list) - 1):
    print("In time period:" + str(t_min + time_counter * dt) + "," + str(t_min + (time_counter + 2) * dt))
    v_star = []
    for node1 in v_list[i]:
        for node2 in v_list[i + 1]:
            if node1 == node2:
                v_star.append(node1)
    print("V-star from time period:" + str(t_min + time_counter * dt) + "," + str(
        t_min + (time_counter + 2) * dt) + " is:,\n", v_star, "\n")
    V_star_all.append(v_star)
    e_star_1 = []
    for (x, y) in e_list[i]:
        if x in v_star and y in v_star:
            e_star_1.append((x, y))
    print("E-star from time period:" + str(t_min + time_counter * dt) + "," + str(
        t_min + (time_counter + 1) * dt) + " is:,\n", e_star_1, "\n")
    E_star_all.append(e_star_1)
    e_star_2 = []
    for (x, y) in e_list[i + 1]:
        if x in v_star and y in v_star:
            e_star_2.append((x, y))
    print("E-star from time period:" + str(t_min + (time_counter + 1) * dt) + "," + str(
        t_min + (time_counter + 2) * dt) + " is:,\n", e_star_2, "\n")
    E_star_all.append(e_star_2)
    time_counter += 1


train_matrices = []
test_matrices = []
for i in range(len(V_star_all)):
    train_matrices.append([])
    test_matrices.append([])
    for node1 in V_star_all[i]:
        rows = []
        for node2 in V_star_all[i]:
            rows.append(0)
        train_matrices[-1].append(rows.copy())
        test_matrices[-1].append(rows.copy())

    for (x, y) in E_star_all[2 * i]:
        position_1 = V_star_all[i].index(x)
        position_2 = V_star_all[i].index(y)
        train_matrices[-1][position_1][position_2] = 1
        train_matrices[-1][position_2][position_1] = 1

    for (x, y) in E_star_all[2 * i + 1]:
        position_1 = V_star_all[i].index(x)
        position_2 = V_star_all[i].index(y)
        test_matrices[-1][position_1][position_2] = 1
        test_matrices[-1][position_2][position_1] = 1


def Sgd(matrices):
    Sgd_all = []
    for i in matrices:
        distances = floyd_warshcall(i)
        for j in range(len(distances)):
            for k in range(len(distances)):
                if distances[j][k] == 0:
                    distances[j][k] = 0
                else:
                    distances[j][k] = 1 / distances[j][k]
        Sgd_all.append(distances)
    return Sgd_all


def Scn(matrices):
    Scn_all = []
    for i in matrices:
        Scn_all.append([])
        for node1 in range(len(i)):
            rows = []
            for node2 in range(len(i)):
                rows.append(0)
            Scn_all[-1].append(rows)
        for node1 in range(len(i)):
            for node2 in range(len(i)):
                if node1 == node2:
                    continue
                counter = 0
                for column in range(len(i)):
                    if i[node1][column] == 1 and i[node2][column] == 1:
                        counter += 1
                Scn_all[-1][node1][node2] = counter
                Scn_all[-1][node2][node1] = counter
    return Scn_all


def Sjc(matrices):
    Sjc_all = []
    for i in matrices:
        Sjc_all.append([])
        for node1 in range(len(i)):
            rows = []
            for node2 in range(len(i)):
                rows.append(0)
            Sjc_all[-1].append(rows)

        for node1 in range(len(i)):
            for node2 in range(len(i)):
                if node1 == node2:
                    continue
                counter1 = 0
                counter2 = 0
                for column in range(len(i)):
                    if i[node1][column] == 1 and i[node2][column] == 1:
                        counter1 += 1
                    if i[node1][column] == 1 or i[node2][column] == 1:
                        counter2 += 1
                if counter2 == 0:
                    continue
                Sjc_all[-1][node1][node2] = counter1 / counter2
                Sjc_all[-1][node2][node1] = counter1 / counter2
    return Sjc_all


def Sa(matrices):
    Sa_all = []
    for i in matrices:
        Sa_all.append([])
        for node1 in range(len(i)):
            rows = []
            for node2 in range(len(i)):
                rows.append(0)
            Sa_all[-1].append(rows)

        for node1 in range(len(i)):
            for node2 in range(len(i)):
                if node1 == node2:
                    continue
                gama_union = []
                for column in range(len(i)):
                    if i[node1][column] == 1 and i[node2][column] == 1:
                        gama_union.append(column)
                sum_all = 0
                sum_ = 0
                for neighbour in gama_union:
                    sum_ = sum(i[neighbour])
                    if sum_ == 0:
                        continue
                    sum_ = 1 / math.log(sum_, 2)
                    sum_all += sum_
                Sa_all[-1][node1][node2] = sum_all
                Sa_all[-1][node2][node1] = sum_all
    return Sa_all


def Spa(matrices):
    Spa_all = []
    for i in matrices:
        Spa_all.append([])
        for node1 in range(len(i)):
            rows = []
            for node2 in range(len(i)):
                rows.append(0)
            Spa_all[-1].append(rows)

        for node1 in range(len(i)):
            for node2 in range(len(i)):
                if node1 == node2:
                    continue
                counter1 = sum(i[node1])
                counter2 = sum(i[node2])
                Spa_all[-1][node1][node2] = counter1 * counter2
                Spa_all[-1][node2][node1] = counter1 * counter2
    return Spa_all


def get_data(matrices, action):
    result = []
    Sgd_all = Sgd(matrices)
    Scn_all = Scn(matrices)
    Sjc_all = Sjc(matrices)
    Sa_all = Sa(matrices)
    Spa_all = Spa(matrices)
    if action == "train":
        print("From time period T0:" + str(t_min) + "," + str(t_min + 2 * dt))
        print("\nSgd is:", Sgd_all[0], "\n")
        print("\nScn is:", Scn_all[0], "\n")
        print("\nSjc is:", Sjc_all[0], "\n")
        print("\nSa is:", Sa_all[0], "\n")
        print("\nSpa is:", Spa_all[0], "\n")
    for Sqd_, Scn_, Sjc_, Sa_, Spa_ in zip(Sgd_all, Scn_all, Sjc_all, Sa_all, Spa_all):
        result.append(np.dstack((np.array(Sqd_), np.array(Scn_), np.array(Sjc_), np.array(Sa_), np.array(Spa_))))
    return result


scale = StandardScaler()

X_train = get_data(train_matrices, "train")
for i in range(len(X_train)):
    X_train[i] = X_train[i].reshape(-1, 5)
    if len(X_train[i]) == 0:
        continue
    X_train[i] = scale.fit_transform(X_train[i])

Y_train = train_matrices
for i in range(len(Y_train)):
    Y_train[i] = np.array(Y_train[i]).flatten()
    if len(Y_train[i]) == 0:
        continue
    for x in range(len(Y_train[i])):
        if (Y_train[i][x] == 0):
            Y_train[i][x] = -1

Xtest = get_data(test_matrices, "test")
for i in range(len(Xtest)):
    Xtest[i] = Xtest[i].reshape(-1, 5)
    if len(Xtest[i]) == 0:
        continue
    Xtest[i] = scale.fit_transform(Xtest[i])

Y_test = test_matrices
for i in range(len(Y_test)):
    Y_test[i] = np.array(Y_test[i]).flatten()
    if len(Y_test[i]) == 0:
        continue
    for x in range(len(Y_test[i])):
        if (Y_test[i][x] == 0):
            Y_test[i][x] = -1


def LineAdd(a, arr1, b, arr2):
    arrCombine = []
    for i in range(len(arr1)):
        arrCombine.append(a * arr1[i] + b * arr2[i])
    return arrCombine


def LineMultiply(a, arr1, b, arr2):
    result = 0
    for i in range(len(arr1)):
        result += a * arr1[i] * b * arr2[i]
    return result


def LeastSquares(X, Y, startingW):
    # X = {x1,x2,...}, xi = [...]
    # Y = {y1,y2,...}, yi in {+1,-1}
    # startingW = [0,0,...], len(w) = len(xi)
    w = startingW
    for i in range(len(Y)):
        w = LineAdd(1, w, (Y[i] - LineMultiply(1, w, 1, X[i])) / (i + 1), X[i])
    return w


Ws = []
for i in range(len(X_train)):
    Ws.append(LeastSquares(X_train[i], Y_train[i], [0, 0, 0, 0, 0]))


results = []
mean_square_errors = []
mean_absolute_errors = []
for i in range(len(Xtest)):
    results.append(0)
    mean_square_errors.append(0)
    mean_absolute_errors.append(0)
    count = 0
    if len(Xtest[i]) == 0:
        count = 1
    for testing_data in Xtest[i]:
        result = LineMultiply(1, Ws[i], 1, testing_data)
        y = 0
        if result > 0:
            y = 1
        else:
            y = -1
        if (y - Y_test[i][count]) == 0:
            results[-1] += 1
        else:
            mean_square_errors[-1] += 1
            mean_absolute_errors[-1] += 1
        count += 1
    results[-1] /= count
    mean_square_errors[-1] /= count
    mean_absolute_errors[-1] /= count

print("The success rates are :", results)
print("The mean square errors are:", mean_square_errors)
print("The mean absolute errors are:", mean_absolute_errors)