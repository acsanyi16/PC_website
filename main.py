import psutil

print('The CPU usage is: ', psutil.cpu_percent(4))
cpu_usage = psutil.cpu_percent(4)


print('RAM memory used:', psutil.virtual_memory()[2], '%')

disk_usage = psutil.disk_usage('/')[0]
print(disk_usage/1024/1024)