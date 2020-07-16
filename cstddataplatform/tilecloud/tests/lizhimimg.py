
map_data_str='1,2,3'

arr = map_data_str.split(',')
print(arr)


list_str = [int(v) for v in map_data_str.split(',')]
print(list_str)


# arr = ['a','b']
# str = ','.join(arr)
#
# arr = [1,2,3]
# str = ','.join(str(i) for i in b)
