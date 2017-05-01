FILE_NAME = "in.txt"


inFile = open(FILE_NAME, 'r')
line = inFile.readline() 
input_data = line.split()
videos = input_data[0]
endpoints = input_data[1]
request_descriptions = input_data[2]
caches = input_data[3]
caches_size = input_data[4]

summa = 0
cashes_id_size={} 
videos_id_size={}  
output = {}
outputbuf = []

for i in range(int(caches)):
    cashes_id_size[i]=caches_size
#print("Keys: id of cashes, values: size of cashes " + str(cashes_id_size))

line = inFile.readline()
input_data = line.split()

for i in range(int(videos)):
    videos_id_size[i]=input_data[i]
#print("Keys: id of videos, values: size of videos " + str(videos_id_size))


cashes_and_endpoints = []
range_to_endpoints = {}
for j in range(int(endpoints)):
    line = inFile.readline()
    input_data = line.split()
    range_to_endpoint =  input_data[0]
    linebuf = []
    endpoints_cashes = []
    endpoints_cashes.append(['data center',range_to_endpoint])
    for i in range(int(input_data[1])):
        linebuf = inFile.readline()
        input_data3 = linebuf.split()
        endpoints_cashes.append([input_data3[0],input_data3[1]])
    range_to_endpoints[j]=endpoints_cashes
#print("Keys: id of endpoints, values: id of cashes and holdback " + str(range_to_endpoints))

buff = []
videos_endpoints_request = {}

for i in range(int(request_descriptions)):
    line = inFile.readline()
    input_data = line.split()
    buff = [input_data[1],input_data[2]]
    videos_endpoints_request[int(input_data[0])] = buff
#print("Keys: id of videos, values: id of endpoints and requests " + str(videos_endpoints_request))

videos_in_data_center = 0
videos_without_request=0
result = []
for i in videos_id_size.keys():
    if videos_endpoints_request.has_key(i) == False:
        result.append(['data center',i])
        del videos_id_size[i]
        videos_in_data_center += 1
        videos_without_request += 1
        
        
print("number of videos that don't have a request: "+str(videos_without_request))
print('-------------------------------------------------------------------------------------------------------------------')

a=0
flag = 0
while flag < int(videos) - videos_without_request:
    if len(cashes_id_size) == 0:
        break
    
    if len(videos_endpoints_request) == 0:
        break
    
    buff_request = '0'
    for i in videos_endpoints_request.keys():
        if int(videos_endpoints_request[i][1]) > int(buff_request):
            buff_request = videos_endpoints_request[i][1]
            buff_id_video = i
            buff_id_endpoints = videos_endpoints_request[i][0]
    
    size_video = videos_id_size[int(buff_id_video)]
    buff_range = range_to_endpoints[int(buff_id_endpoints)][0][1]

    for i in range_to_endpoints[int(buff_id_endpoints)]:
        for j in cashes_id_size.keys():
            if i[0] == str(j):
                if int(i[1]) < int(buff_range) and int(cashes_id_size[int(i[0])]) >= int(size_video):
                    buff_range = i[1]
                    buff_id_cash1 = i[0]
                

    
    if int(caches_size) < int(size_video):
        result.append(['data center',buff_id_video])
        videos_in_data_center += 1
        flag+=1
        del videos_endpoints_request[int(buff_id_video)]
        del videos_id_size[buff_id_video]
        
    elif int(buff_range) == int(range_to_endpoints[int(buff_id_endpoints)][0][1]):
        result.append(['data center',buff_id_video])
        videos_in_data_center += 1
        flag+=1
        del videos_endpoints_request[int(buff_id_video)]
        del videos_id_size[buff_id_video]
        
    elif len(range_to_endpoints[int(videos_endpoints_request[int(buff_id_video)][0])]) == 1:
        result.append(['data center',buff_id_video])
        videos_in_data_center += 1
        flag+=1
        del videos_endpoints_request[int(buff_id_video)]
        del videos_id_size[buff_id_video]

    elif int(cashes_id_size[int(buff_id_cash1)]) >= int(size_video):
        result.append([buff_id_cash1,buff_id_video])
        flag+=1
        buff_cashes = int(cashes_id_size[int(buff_id_cash1)]) - int(size_video)
        cashes_id_size[int(buff_id_cash1)] = buff_cashes
        del videos_endpoints_request[int(buff_id_video)]
        del videos_id_size[buff_id_video]

            
            
buff_result = []        
result2 = {}        
for i in result:
    buff_result = [i[1]]
    for j in result:
        if int(i[1]) != int(j[1]) and i[0] == j[0]:
            buff_result.append(j[1])
    result2[i[0]] = buff_result
    
print("Keys: id of cashes, values: id of videos " + str(result2))
print("Nomber of videos: " + str(videos))
print("Videos in data center: " + str(videos_in_data_center))

videos_sorted = 0
for i in result2.keys():
    if i != 'data center':
        videos_sorted += len(result2[i])

print("Videos sorted: "+ str(videos_sorted))
print("Cashes used: " + str(len(result2.keys())-1) + " From " + str(caches))

outFile = open('output.txt', 'w')
line = outFile.write(str(len(result2.keys())-1))
outFile.write("\n")


for i in result2.keys():
    if i != 'data center':
        line_buff = ''
        for j in range(len(result2[i])):
            if j == len(result2[i]) - 1:
                line_buff += str(result2[i][j])
            else:
                line_buff += str(result2[i][j]) + ' '
        outFile.write(i+" "+line_buff)
        outFile.write("\n")