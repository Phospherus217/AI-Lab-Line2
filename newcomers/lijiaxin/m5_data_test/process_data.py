import pandas as pd

# 1. 读取数据
print("--- 原始数据 ---")
df = pd.read_csv('data.csv')
print(df)

# 2. 清洗
print("\n--- 清洗后数据 ---")
df = df.drop_duplicates()
df['薪资'] = df['薪资'].fillna(0)
df['部门'] = df['部门'].fillna('未知部门')
print(df)

# 3. 统计
print("\n--- 部门的平均薪资 ---")
avg_salary = df.groupby('部门')['薪资'].mean()
print(avg_salary)

# 4. 输出
df.to_csv('clean_data.csv', index=False)
print("\n保存成功！请看左侧新生成的 clean_data.csv 文件")
 

