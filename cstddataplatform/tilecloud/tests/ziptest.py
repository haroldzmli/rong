import zipfile

# file_dir = '/work/data/vector/data.zip'
# zipFile = zipfile.ZipFile(file_dir)
# # print(zipinfo.compress_type)
# # print(zipFile.infolist())
# # print(zipFile.printdir())
# data = zipFile.read('data/12-3130-1547.vector.pbf')
# # print(data)

aaa = {'group':{'aaa':'data1','bbbb':'data'}}
print(aaa['group']['aaa'])

vectordataserver = {'guizhou':{'shp':'/work/data/vector','json':'/work/data/vector'}}
print(vectordataserver['guizhou']['json'])