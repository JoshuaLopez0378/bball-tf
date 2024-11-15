import pandas

df = pandas.read_csv("teams_alpha_order_region.csv")
# for i in range()
x = df[df.columns[0]].count()
l = []
for i in range(1, x + 1):
    l.append(i)

df["Count"] = l
print(df)

cols = ["Count", "Teams"]
df = df[cols]
df.to_csv("teams_alpha_count.csv", index=False)
