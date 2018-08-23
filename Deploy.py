"""
    AUTOMATED POWERBUILDER DEPLOYMENT

        Author: Stivan Kitchoukov

    To run created file from command line: OrcaScr126 Deploy.dat
"""
import os
import subprocess
import time

PackageList = (
    "cf_account_ip",
    "cf_cga"
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
        if content.startswith("appname"):
            AppName = content.replace("appname ", "")
            AppName = AppName.replace(";", "")
        if content.startswith("LibList"):
            LibList = os.path.normpath(content.replace('LibList "', '"' + "C:/iPhiCore/"))
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

    print("Deploying:" + i + "...")
    command = os.path.normpath("OrcaScr126 C:/Users/skitchoukov/Desktop/Python/Deploy.dat")

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    while True:
        line = process.stdout.readline()
        if not line: break

    process.wait()
    print("Finished: " + str(process.returncode))
    time.sleep(20)