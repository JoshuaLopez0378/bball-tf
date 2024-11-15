# import yaml
# with open('scripts/schemas/main_tables_all_schema.yaml', 'r') as file:
#     test_read = yaml.safe_load(file)

# # print(test_read)
# # print(test_read["all_players"])
# for i in test_read['all_players']['dtypes_df']:
#     print(f" {i} | {test_read['all_players']['dtypes_df'][i]}")


# x = dict(zip([col for col in test_read['all_players']['dtypes_df']], [test_read['all_players']['dtypes_df'][col] for col in test_read['all_players']['dtypes_df']]))
# print(x)

colsing = ["test", "1"]
coldoub = ["test", "2"]
print(colsing, coldoub)
