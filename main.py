#!/usr/bin/python

import subprocess
import re
import argparse
import sys
import os
import calendar, time
import subprocess
from crontab import CronTab
import getpass
import re

def run_command(command):
    return os.popen(command).read()

# Command echo "(brightness -l | pcregrep -o1 '[\s\S]+(\d+?\.\d+)$')"

if(len(sys.argv)==1):
    print "Please enter a logfile name."

logfile_titles = "Time,Battery Temperature,Core Temperature,Charge,Remaining Time,Brightness,Free Memory,Total Memory,Chrome Memory,Power\n"

logfile = sys.argv[1]
if(os.path.exists(logfile) == False):
    with open(logfile, 'w') as of:
        of.write(logfile_titles)    

# Haven't added argparse yet, I know - will do when I have time
if len(sys.argv) > 3 and sys.argv[2]=="--cron-set":
    ct = CronTab(user=getpass.getuser())
    print "Setting the following command to run ever %d minutes for user %s: python '%s/%s' '%s'" % (int(sys.argv[3]),getpass.getuser(),os.getcwd(),sys.argv[0],sys.argv[1])
    path = run_command("echo $PATH")
    shell = run_command("echo $SHELL")
    command_str = "export SHELL=%s; export PATH=%s; export MAILTO=''; python '%s/%s' '%s'" % (shell, path, os.getcwd(),sys.argv[0],sys.argv[1])
    command_str = command_str.replace('\n','')
    job = ct.new(command=command_str)
    job.minute.every(int(sys.argv[3]))
    ct.write()
    print "Crontab written."

chrome_memory_command = "ps aux | grep '/Applications/Google Chrome' | awk '{print $5}' | awk '{sum += $1 } END { print sum }'"

def get_free_and_total_memory():
    # Get process info
    ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0].decode()
    vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode()

    # Iterate processes
    processLines = ps.split('\n')
    sep = re.compile('[\s]+')
    rssTotal = 0 # kB
    for row in range(1,len(processLines)):
        rowText = processLines[row].strip()
        rowElements = sep.split(rowText)
        try:
            rss = float(rowElements[0]) * 1024
        except:
            rss = 0 # ignore...
        rssTotal += rss

    # Process vm_stat
    vmLines = vm.split('\n')
    sep = re.compile(':[\s]+')
    vmStats = {}
    for row in range(1,len(vmLines)-2):
        rowText = vmLines[row].strip()
        rowElements = sep.split(rowText)
        vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

    # print 'Wired Memory:\t\t%d MB' % ( vmStats["Pages wired down"]/1024/1024 )
    # print('Active Memory:\t\t%d MB' % ( vmStats["Pages active"]/1024/1024 ))
    # print('Inactive Memory:\t%d MB' % ( vmStats["Pages inactive"]/1024/1024 ))
    # print('Free Memory:\t\t%d MB' % ( vmStats["Pages free"]/1024/1024 ))
    # print('Real Mem Total (ps):\t%.3f MB' % ( rssTotal/1024/1024 ))

    return vmStats["Pages free"]/1024/1024, rssTotal/1024/1024

def get_power():
    amperage_regex = r"mA\):\s([\-\+\d]+?)\s"
    voltage_regex = r"mV\):\s([\-\+\d]+?)\s"
    power_info = run_command("system_profiler SPPowerDataType")
    amperes = float(re.search(amperage_regex,power_info, re.MULTILINE).groups(0)[0])
    voltage = float(re.search(voltage_regex,power_info, re.MULTILINE).groups(0)[0])
    return (voltage*amperes)/(1000000)

def write():
    curtime = calendar.timegm(time.gmtime())
    chrome_mem = os.popen("ps aux | grep '/Applications/Google Chrome' | awk '{print $5}' | awk '{sum += $1 } END { print sum }'").read()
    battery_temp = run_command("istats battery temp --no-scale --value-only")
    core_temp = run_command("istats cpu --no-scale --value-only")
    battery_charge = run_command("istats battery charge --no-scale --value-only")
    battery_remain = run_command("istats battery remain --no-scale --value-only")
    brightness = run_command("brightness -l | pcregrep -o1 '[\s\S]+(\d+?\.\d+)$'")
    power = get_power()
    free_mem, total_mem = get_free_and_total_memory()


    outstr = "%f, %s, %s, %s, %s, %s, %f, %f, %s, %f" % (curtime, battery_temp, core_temp, battery_charge, battery_remain, brightness, free_mem, total_mem, chrome_mem, power)
    outstr = outstr.replace('\n','')

    with open(logfile, 'a') as of:
        of.write("%s\n" % (outstr))

write()
