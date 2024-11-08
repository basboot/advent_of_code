from itertools import combinations

import numpy as np
from scipy.spatial.distance import cityblock

# real puzzle
centers = [np.array([0, 0, 0]), np.array([  48,   24, 1236]), np.array([   53, -1135,   150]), np.array([-1177,     2,    72]), np.array([   65,   158, -1138]), np.array([-1111,     7,  1260]), np.array([   56, -1146,  1291]), np.array([1241,  135, 1231]), np.array([ -95, 1211, 1289]), np.array([-1169,  1270,    54]), np.array([ 1105,    18, -1070]), np.array([   81,   187, -2426]), np.array([-2327,   187,  1231]), np.array([-1134,  1273,  1212]), np.array([   31, -1102,  2545]), np.array([ 1242, -1058,  1199]), np.array([2489,  134, 1292]), np.array([ 1250,     1, -2322]), np.array([  -93,  1387, -2307]), np.array([-1306,   169, -2358]), np.array([-2347,  1214,  1158]), np.array([-3687,    44,  1184]), np.array([-1279,  1199,  2383]), np.array([  -12, -2286,  2381]), np.array([2483,   66,   -2]), np.array([ 1099, -1070, -2439]), np.array([-1172,   153, -3530]), np.array([-2441,  1193,  2417]), np.array([-2451,  2494,  1205]), np.array([-3638,  1215,  1196]), np.array([-3524,     0,  2360]), np.array([-2353,   113, -3622]), np.array([-2410,  1215,  3673]), np.array([-3619,  1377,   118]), np.array([-4845,  1199,  1175])]

# example
#centers = [np.array([0, 0, 0]), np.array([   68, -1246,   -43]), np.array([  -92, -2380,   -20]), np.array([  -20, -1133,  1061]), np.array([ 1105, -1205,  1229])]

print(max([cityblock(scanner1, scanner2) for scanner1, scanner2 in combinations(centers, 2)]))
