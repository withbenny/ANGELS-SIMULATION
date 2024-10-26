# ANGELS-SIMULATION


## Privacy
### 痛點：
根據銀髮安居指數的計算方式，我們得知各類的分數可能有：

Action:

- 高齡者36種：$\cfrac{(65\sim 100) - 65}{35}$

- 行動不便之身心障礙者3種：$0, 0.9878, 1$

- 行動不便之長照者4種：$0, \cfrac{1}{3}, \cfrac{2}{3}, 1$

Nurse:

- 獨居；老老照顧3種：$0, 0.6128, 1$

- 老人無子女；有子女未與子女同住3種：$0, 0.6326, 1$

- 無外傭照顧之長照者2種：$0, 1$

Gold:

- 低收或中低收入戶7種：$0, \cfrac{1}{6}, \cfrac{2}{6}, \cfrac{3}{6}, \cfrac{4}{6}, \cfrac{5}{6}, 1$
- 無自有住宅3種：$0, 0.1747, 1$
- 房價行情較低3種：$0, 0.5840, 1$

Entity：

- 高屋齡21種：$\cfrac{(30\sim 50)-30}{20}$
- 居住於無電梯公寓3種：$0, 0.1815, 1$
- 非鋼骨或鋼筋混凝土結構3種：$0, 0.4147, 1$

Liberty：

- 一公里內無公車站牌2種：$0, 1$
- 一公里內無便利超商2種：$0, 1$
- 二公里內無醫院或診所2種：$0, 1$

Security：

- 位於土壤液化潛勢區4種：$0, \cfrac{1}{3}, \cfrac{2}{3}, 1$
- 位於活動斷層帶1公里內2種：$0, 1$
- 位於淹水潛勢區6種：$0, \cfrac{0.4}{3}, \cfrac{0.75}{3}, \cfrac{1.5}{3}, \cfrac{2.5}{3}, 1$

根據乘法原理，總組合數有：
$(36\times 3\times 4)\times(3\times 3\times 2)\times(7\times 3\times 3)\times (21\times 3\times 3)\times (2\times 2\times 2)\times (4\times 2\times 6) = 35,554,111,488$

因為銀髮安居指數的計算方式是公開的，所以35,554,111,488種組合數透過暴力法推算個體的隱私信息成為可能，特別是許多評分標準的資料可以通過社會工程或實地調查輕易獲得，這大大增加了隱私洩漏的風險。

### 目標：
為了解決上述問題，我們將透過兩種資料處理技術來提升資料的隱私保護強度：
1. 資料打亂（Data Swapping）： 通過使用 data_swapping_with_distribution_control function對資料進行隨機交換，降低原有數據的相關性，使攻擊者無法輕易通過統計信息推斷個體資料，這種方法能夠有效減少個資洩漏的風險。

    而參數swap_fraction控制著打亂的column的比例，較高的值會使更多數據的交換，進一步增加隱私保護的力度，但也可能對數據的整體統計特性產生影響。

    儘管數據的具體值被交換，整體的數據分佈大多數不會受到顯著影響，使得這種方法在保護隱私的同時，也可以保持數據的可用性。例如某些個體擁有相似的行為特徵時，透過資料打亂能讓攻擊者即使知道某些統計數據，也無法確定具體屬於哪個個體。

2. 加入噪音（Add Noise）
為了進一步增強隱私保護，我們選擇對三類多樣性較高的數據action、gold和entity採用加入噪音的技術，這些數據的多樣性使得在其加入隨機擾動後，混淆性顯著提升，而透過將噪音引入原始數據，使得每個數據點都變得不那麼可預測，從而降低了攻擊者根據統計數據回推原始值的可能性。

### 總結：
透過這兩種方法，我們打亂了原有數據的相關性，並透過加入噪音使計算結果有一定的震盪，進一步讓攻擊者無法順利回推目標的其他資訊。





## Reference:
1. [模擬資料欄位及格式：銀髮安居資料.docx - Google 文件](https://docs.google.com/document/d/1I9YC_yLy86W04w5yIDsURrQS6wOOiIr3/edit)

2. [108總統盃黑客松 銀髮安居計畫](https://presidential-hackathon.taiwan.gov.tw/history/2019/files/18.第十八組_銀髮天使_複選會議簡報.pdf)
