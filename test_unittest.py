import unittest
import pandas as pd
from Models_diffusion_innovations import *


sales = tuple([8.26192344363636, 9.20460066059596, 12.0178164697778, 15.921260267805, 21.2161740066094, 31.420434564131, 38.3904519471421, 52.3307819867071, 62.9113953016839, 85.1161924282732, 104.083879757882, 132.859216030029, 170.682620580279, 220.600045153997, 276.020526299077, 346.465021938078, 440.385091980306, 530.55442135112, 635.49205101167, 705.805860788812, 831.42968828187, 962.227395409379, 1140.31094904253, 1269.52053571083, 1418.17004626655, 1591.2135122193])
total = [13375.2439634053, 13789.2495277064, 14120.5171345097, 14502.9192434368, 14917.7637553936, 15555.5482906317, 15788.8606107222, 16345.4843195876, 16924.0184060025, 17726.7475122076, 18454.1188104507, 19155.2911176488, 20045.9829957051, 20421.6373537822, 20264.8910596484, 21570.6888619834, 22256.9952443638, 22806.2764799403, 23435.2382123808, 24031.7070496167, 24270.5009409496, 24915.1871081891, 25623.8922507836, 26659.1362380925, 27000.9508509267, 26823.2483500223]
costs = [0.196, 0.178, 0.157, 0.139, 0.134, 0.142, 0.126, 0.119, 0.106, 0.111, 0.104, 0.105, 0.098, 0.088, 0.087, 0.086, 0.083, 0.083, 0.082, 0.076, 0.069, 0.066, 0.064, 0.058, 0.053, 0.05]
data = pd.DataFrame({'generate': sales, 'total': total, 'costs': costs})
data0 = data['generate'][0]

data2 = {'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
    'generate': [8.26192344363636, 9.20460066059596, 12.0178164697778, 15.921260267805, 21.2161740066094, 31.420434564131, 38.3904519471421, 52.3307819867071, 62.9113953016839, 85.1161924282732, 104.083879757882, 132.859216030029, 170.682620580279, 220.600045153997, 276.020526299077, 346.465021938078, 440.385091980306, 530.55442135112, 635.49205101167, 705.805860788812, 831.42968828187, 962.227395409379, 1140.31094904253, 1269.52053571083, 1418.17004626655, 1591.2135122193],
    'total':[13375.2439634053, 13789.2495277064, 14120.5171345097, 14502.9192434368, 14917.7637553936, 15555.5482906317, 15788.8606107222, 16345.4843195876, 16924.0184060025, 17726.7475122076, 18454.1188104507, 19155.2911176488, 20045.9829957051, 20421.6373537822, 20264.8910596484, 21570.6888619834, 22256.9952443638, 22806.2764799403, 23435.2382123808, 24031.7070496167, 24270.5009409496, 24915.1871081891, 25623.8922507836, 26659.1362380925, 27000.9508509267, 26823.2483500223],
    'costs':[0.196, 0.178, 0.157, 0.139, 0.134, 0.142, 0.126, 0.119, 0.106, 0.111, 0.104, 0.105, 0.098, 0.088, 0.087, 0.086, 0.083, 0.083, 0.082, 0.076, 0.069, 0.066, 0.064, 0.058, 0.053, 0.05]}
finalYear = 2025
model = Bass1
metod = 'Nelder-Mead'

# print(data['costs'])

class TestFunction(unittest.TestCase):

    def test_Bass1(self):
        # Параметры для теста
        x = 21.29121628
        P = 0.0005727
        Q = 0.249517965
        M = 2407.09678
        # Ожидаемый результат
        expected_result = 6.631900642
        # Вызываем функцию и проверяем результат
        result = Bass1(x, P, Q, M)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_squareMistakeBass1(self):
        # Параметры для теста
        k = [0.0005727, 0.249517965, 2407.09678]
        # Ожидаемый результат
        expected_result = 4722.498315
        # Вызываем функцию и проверяем результат
        result = squareMistakeBass1(k, sales)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_Bass2(self):
        # Параметры для теста
        x = [14502.9192434368, 20.3462795784015]
        P = 0.000820214
        Q = 0.263879857
        M = 0.087482053
        # Ожидаемый результат
        expected_result = 6.302953179
        # Вызываем функцию и проверяем результат
        result = Bass2(x, P, Q, M)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_squareMistakeBass2(self):
        # Параметры для теста
        k = [0.000820214, 0.263879857, 0.087482053]
        # Ожидаемый результат
        expected_result = 4048.370363
        # Вызываем функцию и проверяем результат
        result = squareMistakeBass2(k, sales, total)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_Bass3(self):
        # Параметры для теста
        x = (14502.9192434368, 18.4315366239359, 0.139)
        P = 0.0
        Q = 0.315550089618395
        K = 0.00508027974311906
        # Ожидаемый результат
        expected_result = 5.6064433
        # Вызываем функцию и проверяем результат
        result = Bass3(x, P, Q, K)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_squareMistakeBass3(self):
        # Параметры для теста
        k = [0.0, 0.315550089618395, 0.00508027974311906]
        # Ожидаемый результат
        expected_result = 2586.297671
        # Вызываем функцию и проверяем результат
        result = squareMistakeBass3(k, sales, total, costs)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_Logic1(self):
        # Параметры для теста
        x = 8.26192344363636, 4
        B = 0.241884653890683
        C = 22.7134364527308
        M = 2460.53700033328
        # Ожидаемый результат
        expected_result = 34.59646254
        # Вызываем функцию и проверяем результат
        result = Logic1(x, B, C, M)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_squareMistakeLogic1(self):
        # Параметры для теста
        k = [0.241884653890683, 22.7134364527308, 2460.53700033328]
        # Ожидаемый результат
        expected_result = 6103.38713320634
        # Вызываем функцию и проверяем результат
        result = squareMistakeLogic1(k, sales)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_Logic2(self):
        # Параметры для теста
        x = (8.26192344363636, 4, 14502.9192434368)
        B = 0.226659184
        C = 21.37602152
        M = 0.083369463
        # Ожидаемый результат
        expected_result = 31.36361361
        # Вызываем функцию и проверяем результат
        result = Logic2(x, B, C, M)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_squareMistakeLogic2(self):
        # Параметры для теста
        k = [0.226659184207978, 21.3760215248117, 0.0833694625461306]
        # Ожидаемый результат
        expected_result = 5138.36154948632
        # Вызываем функцию и проверяем результат
        result = squareMistakeLogic2(k, sales, total)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_Logic3(self):
        # Параметры для теста
        x = (8.26192344363636, 4, 14502.9192434368, 0.139)
        B = 0.286694795453112
        C = 16.0139238583913
        M = 0.00362975634363548
        # Ожидаемый результат
        expected_result = 19.68073397
        # Вызываем функцию и проверяем результат
        result = Logic3(x, B, C, M)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_squareMistakeLogic3(self):
        # Параметры для теста
        k = [0.286694795, 16.01392386, 0.003629756]
        # Ожидаемый результат
        expected_result = 6743.699883
        # Вызываем функцию и проверяем результат
        result = squareMistakeLogic3(k, sales, total, costs)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_Gompertz1(self):
        # Параметры для теста
        x = 8.26192344363636, 4
        B = 2.149635573
        C = 0.067589208
        M = 7713.562703
        # Ожидаемый результат
        expected_result = 19.3066784
        # Вызываем функцию и проверяем результат
        result = Gompertz1(x, B, C, M)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_squareMistakeGompertz1(self):
        # Параметры для теста
        k = [2.14963557345369, 0.0675892079091823, 7713.56270310079]
        # Ожидаемый результат
        expected_result = 2488.69694313136
        # Вызываем функцию и проверяем результат
        result = squareMistakeGompertz1(k, sales)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_Gompertz2(self):
        # Параметры для теста
        x = (8.26192344363636, 4, 14502.9192434368)
        B = 2.01551543764232
        C = 0.0770259576006086
        M = 0.174912702867331
        # Ожидаемый результат
        expected_result = 18.47805612
        # Вызываем функцию и проверяем результат
        result = Gompertz2(x, B, C, M)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_squareMistakeGompertz2(self):
        # Параметры для теста
        k = [2.015515438, 0.077025958, 0.174912703]
        # Ожидаемый результат
        expected_result = 3654.402894
        # Вызываем функцию и проверяем результат
        result = squareMistakeGompertz2(k, sales, total)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_Gompertz3(self):
        # Параметры для теста
        x = (8.26192344363636, 4, 14502.9192434368, 0.139)
        B = 2.34706418652626
        C = 0.160488687350149
        M = 0.00416046333406784
        # Ожидаемый результат
        expected_result = 9.980983742
        # Вызываем функцию и проверяем результат
        result = Gompertz3(x, B, C, M)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_squareMistakeGompertz3(self):
        # Параметры для теста
        k = [2.347064187, 0.160488687, 0.004160463]
        # Ожидаемый результат
        expected_result = 13566.32952
        # Вызываем функцию и проверяем результат
        result = squareMistakeGompertz3(k, sales, total, costs)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_func_dif_innov(self):
        # Ожидаемый результат
        expected_result = (8.26192344363636, 11.69019995, 15.96482366, 21.29132153, 27.92323179, 36.17226326, 46.42001035, 59.13110882, 74.86744991, 94.30264141, 118.2352515, 147.5984296, 183.4622237, 227.0233142, 279.5751248, 342.4497493, 416.9226748, 504.0731951, 604.5994473, 718.5987948, 845.3421144, 983.0914021, 1129.025997, 1279.341211, 1429.552876, 1574.981988, 1711.324371, 1835.165784, 1944.312628, 2037.872671, 2116.106031), (1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025), (0.000572697, 0.249513259, 2407.246347), (0.0008791697309390024, 0.1925282635241272, 3328.919450741432)
        expected_result = tuple([int(k) for i in expected_result for k in i])
        # Вызываем функцию и проверяем результат
        datatest = pd.DataFrame(data2)
        datatest['cum_sum'] = datatest['generate'].cumsum()
        datatest['Sales'] = [0]+[datatest['generate'][i+1]-datatest['generate'][i] for i in range(datatest.shape[0]-1)]
        datatest['data0'] = datatest['generate'][0]
        result = func_dif_innov(datatest, finalYear, model, metod)
        result = tuple([int(k) for i in result for k in i])
        # Проверяем получаемый и ожидаемый результаты
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
