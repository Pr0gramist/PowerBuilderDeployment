"""
DEPLOY POWERBUILDER PACKAGES
 
                Author: Stivan Kitchoukov
 
To run created file from command line: OrcaScr126 Deploy.dat
"""
import os
import subprocess
import time

PackageList = (
    "cf_common",
    "cf_account_ip",
    "cf_ap",
    "cf_ar",
    "cf_cga",
    "cf_common_trans",
    "cf_crt",
    "cf_ddc",
    "cf_gain_loss",
    "cf_gl_reports",
    "cf_party",
    "cf_party_group",
    "cf_party_option",
    "cf_pledge",
    "cf_scheduled_reports",
    "cf_spending_rules_report",
    "cf_strategy",
    "cf_strategy_reports",
    "cf_taxforms"
)
 
LibList = ""
AppName = ""
 
for i in PackageList:
    DevDeploy = "p_" + i + "_d"
    StagingDeploy = "p_" + i + "_s"
    PackagePath = os.path.normpath("C:/iPhiCore/" + i + ".pbt")
    pbt = open(PackagePath, "r")

    while True:
    content = pbt.readline()
    if not content: break
    if content.lower().startswith("appname"):
        AppName = content.lower().replace("appname ", "")
        AppName = AppName.replace(";", "")
    if content.lower().startswith("liblist"):
        LibList = os.path.normpath(content.lower().replace('liblist "', '"' + "C:/iPhiCore/"))
        LibList = LibList.replace("\\\\", "\\")
        LibList = os.path.normpath(LibList.replace(".pbl;", ".pbl;" + "C:/iPhiCore/"))
        LibList = LibList.replace('";', ';"')

    File = open("Deploy.dat", "w")
    File.write("Start Session\n")
    File.write("set debug TRUE\n")
    File.write('Set Liblist ' + LibList)
    File.write('Set Application "' + os.path.normpath("C:/iPhiCore/" + i) + '.pbl" ' + AppName)
    File.write("build application full\n")
    File.write('build project "' + os.path.normpath("C:/iPhiCore/" + i) + '.pbl" "' + DevDeploy + '"\n')
    File.write('build project "' + os.path.normpath("C:/iPhiCore/" + i) + '.pbl" "' + StagingDeploy + '"\n')
    File.write("End Session")
    File.close()

    print(time.strftime("%H:%M:%S", time.localtime()) + " - Deploying:" + i + "...")
    command = os.path.normpath("OrcaScr126 C:/Users/skitchoukov/Desktop/Python/Deploy.dat")

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    while True:
        line = process.stdout.readline()
        if not line: break

    process.wait()
    print(time.strftime("%H:%M:%S", time.localtime()) + " - Finished: " + str(process.returncode))
    time.sleep(20)