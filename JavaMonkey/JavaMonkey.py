'''
Created on May 13, 2014

@author: pli
'''
import Utils,os,jpype,time

class JavaMonkey:
    WAIT_FOR_CONNECTION_TIMEOUT = 5000
    def __init__(self, device_id = None):
        try:
            adblocation = os.path.join(os.environ["ANDROID_HOME"],"platform-tools","adb")
            print "ADB Locaton: %s" % adblocation
            options = jpype.JClass("java.util.TreeMap")()
            options.put("backend","adb")
            options.put("adbLocation", adblocation)
            self.package = jpype.JPackage("com.android.chimpchat")
            print dir(self.package.ChimpChat)
            self.mChimpchat = self.package.ChimpChat.getInstance(options)
            if device_id:
                self.device = self.mChimpchat.waitForConnection(self.WAIT_FOR_CONNECTION_TIMEOUT, jpype.JString(device_id))
            else:
                self.device = self.mChimpchat.waitForConnection(self.WAIT_FOR_CONNECTION_TIMEOUT, jpype.JString(".*"))
                print "connect is done"
                self.TouchPressType = self.package.core.TouchPressType
                self.PhysicalButton = self.package.core.PhysicalButton
                self.By = self.package.core.By
        except Exception,e:
            import traceback
            traceback.print_exc()   
            
    def get_device(self):
        return self.device
    
    def shutdown(self):
        self.mChimpchat.shutdown()
    
    def get_rootview(self):
        self.device_wake()
        return self.device.getRootView()
    
    def get_view_id_list(self):
        view = self.device.getViewIdList()
        return view
    
    def get_views_by_text(self, text):
        self.device_wake()
        try:
            rawviews = self.device.getViews(self.By.text(text))
            if not rawviews or rawviews.isEmpty():
                rawviews = []
            views = []
            for view in rawviews:
                views.append(view)
        except Exception,e:
            print "Cannot retrieve views with error %s" % str(e)
            views = []
        if views:
            iterator = rawviews.iterator()
            while iterator.hasNext():
                views.append(rawviews.next())
        return views
        
    def get_view_by_id(self, vid, timeout = 5):
        self.device_wake()
        try:
            while timeout > 0:
                ids = self.device.getViewIdList()
                if vid in ids:
                    return self.device.getView(self.By.id(vid))
                time.sleep(0.5)
                timeout -= 0.5
        except Exception,e:
            print "Cannot retrieve views with error %s" % str(e)
            return None
        print "Cannot find view which id is %s" % vid
        return None
    
    def view_getlocation(self, view):
        rect = view.getLocation()
        return rect.left, rect.top, rect.right, rect.bottom
    
    def view_getcenter(self, view):
        rect = view.getLocation()
        return (rect.left + rect.right)/2, (rect.top + rect.bottom)/2
    
    def view_click_center(self, view):
        x, y = self.view_getcenter(view)
        self.device_click(x, y)

    def view_longclick_center(self, view, length = 0.5):
        x, y = self.view_getcenter(view)
        self.device_longclick(x, y, length)
        
    def view_gettext(self, view):
        return view.getText()
    
    def view_setfocused(self, view, is_focused):
        view.setFocused(is_focused)
        
    def view_isfocused(self, view):
        return view.getFocused()
    
    def view_setselected(self, view, is_selected):
        view.setSelected(is_selected)
        
    def view_isselected(self, view):
        return view.getSelected()
    
    def view_isenabled(self, view):
        return view.getEnabled()
    
    def view_ischecked(self, view):
        return view.getChecked()
    
    def view_get_accessibility_ids(self, view):
        return view.getAccessibilityIds()
    
    def view_get_children(self, view):
        return view.getChildren()
        
    def view_get_parent(self, view):
        return view.getParent()
    
    def device_wake(self):
        self.device.wake()
    
    def device_dispose(self):
        self.device.dispose()
        
    def device_type(self, text):
        self.device_wake()
        self.device.type(text)
    
    def device_press_home(self):
        self.device.press(self.PhysicalButton.HOME, self.TouchPressType.DOWN_AND_UP)
    
    def device_press_back(self):
        self.device.press(self.PhysicalButton.BACK, self.TouchPressType.DOWN_AND_UP)
    
    def device_drag(self, startX, startY, endX, endY, steps, ms = 0):
        self.device_wake()
        self.device.drag(startX, startY, endX, endY, steps, ms)
    
    def device_click(self, x, y):
        self.device.touch(x, y, self.TouchPressType.DOWN_AND_UP)
        
    def device_longclick(self, x, y, length = 0.5):
        self.device_wake()
        self.device.touch(x, y, self.TouchPressType.DOWN)
        time.sleep(length)
        self.device.touch(x, y, self.TouchPressType.UP)
    
    def device_press_enter(self):
        self.device.press(self.PhysicalButton.ENTER, self.TouchPressType.DOWN_AND_UP)
    
    def get_screenshot_as_file(self, filename = "default-java_monkey_screenshot.png"):
        image = self.device.takeSnapshot()
        print self.device
        print 'RGBA'
        b = image.convertToBytes('PNG')
        print len(b)
        image.writeToFile(filename, 'PNG')
        
    def get_screenshot_without_items(self, filename, items = None, coordinates = None):
        self.get_screenshot_as_file(filename)
        if coordinates:
            cords = []
            for cord in coordinates:
                cords.append(cord)
            self.drawRec(filename, cords)
        
    def drawRec(self,filename, cordlist, color=(0,0,0)):
        '''
        draw rectangles to images
        '''
        import Image, ImageDraw
        im = Image.open(filename)
        #solve the device reslution problem
        #simulator's reslution width is 320
        ratio = 1
        draw = ImageDraw.Draw(im)
        for cord in cordlist:
            newcord = (cord[0]*ratio, cord[1]*ratio, cord[2]*ratio, cord[3]*ratio)
            draw.rectangle(newcord, fill=color)
            #im.show()
        del draw
        newfile = filename
        im.save(newfile)
        return newfile
    
    
if __name__ == "__main__":
    Utils.startJVM()
    monkey = JavaMonkey("SH18TT504938")
    print monkey.get_device()
#     monkey.wake()
    By = monkey.package.core.By
    print monkey.By.text("abc")
    print monkey.get_screenshot_as_file("a.jpg")