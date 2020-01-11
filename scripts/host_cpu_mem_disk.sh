#/bin/bash
#cpu
cpus=`top -d1 -bn3 | grep "%Cpu(s)" | tail -1 | awk '{ print $2,$4 }'`
cpus_1_temp=`echo $cpus | awk '{print $1}'`
cpus_2_temp=`echo $cpus | awk '{print $2}'`
cpus_sum=$(echo "scale=3; $cpus_1_temp + $cpus_2_temp" | bc)
echo $cpus_sum%
#mem
mem_sum=`free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB %.2f%%\n", $3,$2,$3*100/$2 }'`
echo $mem_sum
#disk
disks_sum=`df -h -t ext2 -t ext4 -t xfs -t tmpfs | grep -vE '^Filesystem|cdrom' | awk '{ print "Disk Usage:"" " $1 " " $3"/"$2" """$5""}'`
echo $disks_sum

