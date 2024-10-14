import pandas as pd

class ScoreCalculator:
    def apply_score(self, data):
        classifier = Classify()
        data['a'] = data.apply(classifier.a_ability, axis=1)
        data['n'] = data.apply(classifier.n_care, axis=1)
        data['g'] = data.apply(classifier.g_economic, axis=1)
        data['e'] = data.apply(classifier.e_housing, axis=1)
        data['l'] = data.apply(classifier.l_living, axis=1)
        data['s'] = data.apply(classifier.s_safety, axis=1)
        data['score'] = data['a'] + data['n'] + data['g'] + data['e'] + data['l'] + data['s']

        result = data[['person_sn', 'is_use_long_term_care', 'age', 'disability_lv', 'family_type', 'child_cnt',
                       'is_living_same_county', 'low_type_cd', 'having_house_type', 'build_age', 'is_apartment',
                       'bus', 'store', 'hospital', 'lique', 'score']]
        print('Score calculation completed.')
        return result

class Classifier:
    def __init__(self):
        self.wa1 = 5.9760 / 100
        self.wa2 = 10.5620 / 100
        self.wa3 = 12.8426 / 100
        self.wn1 = 9.8834 / 100
        self.wn2 = 7.2051 / 100
        self.wn3 = 3.1471 / 100
        self.wg1 = 8.3630 / 100
        self.wg2 = 3.9262 / 100
        self.wg3 = 1.3964 / 100
        self.we1 = 1.5622 / 100
        self.we2 = 4.2409 / 100
        self.we3 = 7.4030 / 100
        self.wl1 = 2.1028 / 100
        self.wl2 = 1.7318 / 100
        self.wl3 = 4.2508 / 100
        self.ws1 = 4.1006 / 100
        self.ws2 = 4.6387 / 100
        self.ws3 = 6.6674 / 100
    
    def a_ability(self, row):
        a = 0

        # 年齡
        # a1 高齡者
        age = row['age']
        if age >= 100:
            a1 = 1
        elif age < 100:
            a1 = (age-65)/35
        else:
            raise ValueError(f'Invalid value for age: {age}')
        
        # 身心障礙程度
        # 0：無身心障礙
        # 1-5: 有身心障礙（數值愈低代表愈嚴重）
        # 資料中只提供了身心障礙程度，但沒有提供是否行動不便，
        # 因此，中重度（4級）以上視為行動不便，計1分
        # 中度（3級）因無法判定，按附表1計0.9878分
        # 輕度（2級）以下視為行動正常，計0分
        # a2 行動不便之身心障礙者，a3 行動不便之長照者
        d_lv = row['disability_lv']
        if d_lv == 5:
            a2 = 1
            a3 = 1
        elif d_lv == 4:
            a2 = 1
            a3 = 2/3
        elif d_lv == 3:
            a2 = 0.9878
            a3 = 1/3
        elif d_lv in [2, 1, 0]:
            a2 = 0
            a3 = 0
        elif d_lv == 'NA' or pd.isna(d_lv):
            a2 = 0
            a3 = 0
        else:
            raise ValueError(f'Invalid value for disability_lv: {d_lv}')

        a = self.wa1*a1 + self.wa2*a2 + self.wa3*a3
        return a
    
    def n_care(self, row):
        n = 0

        # 家庭型態
        # 家庭型態
        # 1: 獨居
        # 2: 老老照顧
        # 3: 其他
        # n1 獨居者；老老照顧
        f_type = row['family_type']
        if f_type == 1:
            n1 = 1
        elif f_type == 2:
            n1 = 0.6128
        elif f_type == 3:
            n1 = 0
        else:
            raise ValueError(f'Invalid value for family_type: {f_type}')
        
        # 子女數，子女是否住在同縣市
        # 子女數: int
        # 子女是否住在同縣市
        # 0: 沒有子女住在同縣市
        # 1: 有子女住在同縣市
        # n2 老人無子女；有子女未與子女同住
        c_cnt = row['child_cnt']
        is_same_county = row['is_living_same_county']
        if c_cnt == 0:
            n2 = 1
        elif c_cnt >= 1:
            if is_same_county == 0:
                n2 = 0.6326
            elif is_same_county == 1:
                n2 = 0
            else:
                raise ValueError(f'Invalid value for is_living_same_county: {is_same_county}')
        else:
            raise ValueError(f'Invalid value for child_cnt: {c_cnt}')

        # 資料中沒有提供有無外傭照顧之長照者，因此此項目不計分
        # n3 無外傭照顧之長照者
        n3 = 0

        n = self.wn1*n1 + self.wn2*n2 + self.wn3*n3
        return n
    
    def g_economic(self, row):
        g = 0

        # 低收或中低收入戶
        # 0-4: 低收入戶(數值愈低代表愈嚴重)
        # 5: 中低收入戶
        # 99: 非低收中低收入戶
        # g1 低收或中低收入戶
        low_type = row['low_type_cd']
        if low_type == 0:
            g1 = 1
        elif low_type == 1:
            g1 = 5/6
        elif low_type == 2:
            g1 = 4/6
        elif low_type == 3:
            g1 = 3/6
        elif low_type == 4:
            g1 = 2/6
        elif low_type == 5:
            g1 = 1/6
        elif low_type == 99:
            g1 = 0
        else:
            raise ValueError(f'Invalid value for low_type_cd: {low_type}')
        
        # 有無殼類別
        # 1: 標準有殼
        # 2: 有住宅(本縣市)但非所在戶籍
        # 3: 有住宅(外縣市)但非所在戶籍
        # 4: 戶籍地所有者之配偶、父母及未成年子女
        # 5: 戶籍地所有者之成年子女及其他親友
        # 6: 無法判斷
        # 7: 標準無殼
        # g2 無自有住宅
        house_type = row['having_house_type']
        if house_type in [1, 2, 3, 4, 5]:
            g2 = 0
        elif house_type == 6:
            g2 = 0.1747
        elif house_type == 7:
            g2 = 1
        else:
            raise ValueError(f'Invalid value for having_house_type: {house_type}')

        # 資料中沒有提供房價行情，因此此項按附表1計0.5840分
        # g3 房價行情較低
        g3 = 0.5840

        g = self.wg1*g1 + self.wg2*g2 + self.wg3*g3
        return g
    
    def e_housing(self, row):
        e = 0
        # 屋齡: int
        # e1 高屋齡
        build_age = row['build_age']
        if build_age >= 50:
            e1 = 1
        elif build_age < 30:
            e1 = 0
        elif build_age >= 30 and build_age < 50:
            e1 = (build_age-30)/20
        else:
            build_age = 34
            e1 = (build_age-30)/20
        
        # 是否為無電梯公寓
        # 以戶籍地是否為5樓建築，且住在非1樓住戶做判斷。
        # 0: 不符合上述條件
        # 2-5: 符合上述條件(數值愈高表示居住樓層愈高)
        # 99: NULL或無法判斷
        # e2 居住於無電梯公寓
        is_apartment = row['is_apartment']
        if is_apartment == 0:
            e2 = 0
        elif is_apartment in [2, 3, 4, 5]:
            e2 = 1
        elif is_apartment == 99:
            e2 = 0.1815
        else:
            raise ValueError(f'Invalid value for is_apartment: {is_apartment}')
        
        # 資料中沒有提供建築結構，因此此項按附表1計0.4147分
        # e3 非鋼骨或鋼筋混凝土結構
        e3 = 0.4147

        e = self.we1*e1 + self.we2*e2 + self.we3*e3
        return e
    
    def l_living(self, row):
        l = 0

        # 與交通站牌距離
        # 數值愈高表示距離交通站牌愈遠，-1則為無法判斷。
        # 1: 500公尺以上才有公車站牌
        # 0.8: 400-未滿500公尺才有公車站牌
        # 0.6: 300-未滿400公尺才有公車站牌
        # 0.4: 200-未滿300公尺才有公車站牌
        # 0.2: 100-未滿200公尺才有公車站牌
        # 0: 100公尺內有公車站牌
        # l1 一公里無公車站牌，但資料數字最高為500公尺，因此評分按照500公尺無公車站牌計算，無法判斷按500公尺以上計算
        bus = row['bus']
        if bus == 1:
            l1 = 1
        elif bus in [0.8, 0.6, 0.4, 0.2, 0, -1]:
            l1 = 0
        else:
            raise ValueError(f'Invalid value for bus: {bus}')

        # 與零售商距離
        # 數值愈高表示距離交通站牌愈遠，-1則為無法判斷。
        # 1: 500公尺以上才有便利超商
        # 0.8: 400-未滿500公尺才有便利超商
        # 0.6: 300-未滿400公尺才有便利超商
        # 0.4: 200-未滿300公尺才有便利超商
        # 0.2: 100-未滿200公尺才有便利超商
        # 0: 100公尺內有便利超商
        # l2 一公里無便利商店，但資料數字最高為500公尺，因此評分按照500公尺無便利商店計算，無法判斷按500公尺以上計算
        store = row['store']
        if store == 1:
            l2 = 1
        elif store in [0.8, 0.6, 0.4, 0.2, 0, -1]:
            l2 = 0
        else:
            raise ValueError(f'Invalid value for store: {store}')
        
        # 與醫院診所距離
        # 數值愈高表示距離交通站牌愈遠，-1則為無法判斷。
        # 1: 1000公尺以上才有醫院或診所
        # 0.8: 800-未滿1000公尺才有醫院或診所
        # 0.6: 600-未滿800公尺才有醫院或診所
        # 0.4: 400-未滿600公尺才有醫院或診所
        # 0.2: 200-未滿400公尺才有醫院或診所
        # 0: 200公尺內有醫院或診所
        # l3 二公里無醫院或診所，但資料數字最高為1000公尺，因此評分按照1000公尺無醫院或診所計算，無法判斷按1000公尺以上計算
        hospital = row['hospital']
        if hospital == 1:
            l3 = 1
        elif hospital in [0.8, 0.6, 0.4, 0.2, 0, -1]:
            l3 = 0
        else:
            raise ValueError(f'Invalid value for hospital: {hospital}')
        
        l = self.wl1*l1 + self.wl2*l2 + self.wl3*l3
        return l
    
    def s_safety(self, row):
        # 土壤液化區
        # 0: 建物非落在土壤液化區
        # 1: 建物落在低潛勢土壤液化區
        # 2: 建物落在中潛勢土壤液化區
        # 3: 建物落在高潛勢土壤液化區
        # 4: NULL
        # s1 位於土壤液化潛勢區，NULL視為非落在土壤液化區
        lique = row['lique']
        if lique == 0:
            s1 = 0
        elif lique == 1:
            s1 = 1/3
        elif lique == 2:
            s1 = 2/3
        elif lique == 3:
            s1 = 1
        elif lique == 4:
            s1 = 0
        else:
            raise ValueError(f'Invalid value for lique: {lique}')
        
        # 資料中沒有提供活動斷層帶以及淹水潛勢區，因此均按0分計算
        s2 = 0
        s3 = 0

        s = self.ws1*s1 + self.ws2*s2 + self.ws3*s3
        return s
    
    def apply_class(self, data):
        data['a'] = data.apply(self.a_ability, axis=1)
        data['n'] = data.apply(self.n_care, axis=1)
        data['g'] = data.apply(self.g_economic, axis=1)
        data['e'] = data.apply(self.e_housing, axis=1)
        data['l'] = data.apply(self.l_living, axis=1)
        data['s'] = data.apply(self.s_safety, axis=1)
        data['score'] = data['a'] + data['n'] + data['g'] + data['e'] + data['l'] + data['s']

        result = data[['person_sn', 'is_use_long_term_care',
                       'a', 'n', 'g', 'e', 'l', 's', 'score']]
        print('Classification completed.')
        return result