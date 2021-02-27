import sys
import subprocess
import re
import shlex

ips = [line.strip() for line in open("ips.txt", "r")]
n = len(ips)

ins = [line.split("|")[0] for line in ips]
outs = [line.split("|")[1] for line in ips]

hostname = subprocess.run(["hostname"],capture_output=True).stdout.decode('utf8')
# hostname = "node2"
id = re.findall("(?<=node)[0-9]",hostname)[0]

port = "9000"
thread = int(sys.argv[1])
ratio = int(sys.argv[2])


# ratios = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# locks = [1]
lock = 1

def get_cmd(n, i):
  cmd = ""
  for j in range(n):
    if j > 0:
      cmd += ";"
    if id == j:
      cmd += ins[j] + ":" + str(port+i)
    else:
      cmd += outs[j] + ":" + str(port+i)
  return cmd

# for lock in locks:
#   for ratio in ratios:    
#     for i in range(3):
#       cmd = get_cmd(n, i)
#       print('./bench_ycsb --logtostderr=1 --id=%d --servers="%s" --protocol=Calvin --partition_num=%d --threads=12 --batch_size=10000 --replica_group=4 --lock_manager=%d --read_write_ratio=90 --cross_ratio=%d' % (id, cmd, 12*n, lock, ratio))


# for lock in locks:
#   for ratio in ratios:    
    # for i in range(3):
ips = [ip+":"+port for ip in ins]
# print(ips)
ips = ";".join(ips)
cmd = '../bench_tpcc --logtostderr=1 --id=%s --servers="%s" --protocol=Calvin --partition_num=%d --threads=%d --batch_size=10000 --replica_group=8 --lock_manager=%d --query=mixed --neworder_dist=%d --payment_dist=%d' % (id, ips, 20*n, thread, lock, ratio, ratio)
print("###{}".format(ratio))
# print(shlex.split(cmd))
subprocess.run(shlex.split(cmd))