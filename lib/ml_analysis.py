dataframe['baseline'] = 0

i = 0
j = 0

while(True):
    if j+42 < len(urls):
        dataframe.loc[j:j+42,:].baseline = i
        j = j+43
        i = i+1
    else:
        dataframe.loc[j:len(urls),:].baseline = i
        break
        
def error(column):
    total = 0
    for j in range(0,50):
        sum = 0
        for i in range(0,10):
            sum += pow(dataframe[dataframe[column] == j].iloc[:,i] - dataframe[dataframe[column] == j].mean()[i], 2).sum()
        total += sum
    return total


error('cluster')
error('baseline')
