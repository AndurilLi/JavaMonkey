'''
Created on May 7, 2014

@author: pli
'''
import jpype,os

def list_jarfile():
    current_dir_abs = os.path.abspath(os.path.dirname(__file__))
    jarfolder = os.path.join(current_dir_abs, "jarfile")
    jarfiles = os.listdir(jarfolder)
    jarfile_fullpaths = []
    for jarfile in jarfiles:
        if os.path.splitext(jarfile)[1]==".jar":
            jarfile_fullpaths.append(os.path.join(jarfolder, jarfile))
    return jarfile_fullpaths

def startJVM(jarfiles = list_jarfile()):
    '''jarfiles = filefullpath1<os.pathsep>filefullpath2...'''
    if not jarfiles:
        jarfiles = list_jarfile()
    else:
        for jarfile in jarfiles:
            if not os.path.isfile(jarfile):
                raise Exception("Cannot load filepath %s" % jarfile)
    print "Start JVM with jarfiles: %s" % jarfiles
    jvmpath = jpype.getDefaultJVMPath()
    jpype.startJVM(jvmpath, "-Djava.class.path=%s" % os.pathsep.join(jarfiles))
     
def shutdownJVM():
    jpype.shutdownJVM()

if __name__ == "__main__":
#     startJVM("jarfile")
#     try:
#         package = jpype.JPackage("com.android.chimpchat")
#         ChimpChat = jpype.JPackage("com.android.chimpchat").ChimpChat
# #         map = jpype.JClass("java.util.Properties")(jpype.JString,jpype.JString)
#         print dir(ChimpChat)
# #         ChimpChat.getInstance()
# #         mdevice = jpype.JPackage("com.android.chimpchat").core.IChimpDevice()#jpype.JClass("com.android.chimpchat.core.IChimpDevice")
# #         print dir(mdevice)
# #         mdevice.wait()
#     except Exception,e:
#         print e
#         pass
# #     mdevice = package.core.IChimpDevice
# #     print dir(mdevice)
# #     mdevice.wake()
#     shutdownJVM()
#     print list_jarfile()
    startJVM()
    shutdownJVM()