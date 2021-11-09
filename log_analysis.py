txt = open('log.txt', 'r')
text_data = txt.readlines()
log_sum = [0 for i in range(23)]
for i in range(len(text_data)):
    text = text_data[i]
    data = str(text[1:-1]).split(', ')
    myindex = 0
    loss = 0
    if len(data) == 23:
        for k in range(len(data)):
            tgt=data[k].split(": ")
            if str(tgt[0][1:-1]) == "epoch":
                myindex = int(tgt[1])
            if str(tgt[0][1:-1]) == "loss":
                loss += float(tgt[1])
        log_sum[myindex-1] += loss
print(log_sum)
print(log_sum.index(min(log_sum))+1)