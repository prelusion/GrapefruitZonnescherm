import datetime
import wx

def note_book(self):
    # don't want to be typing 'self.' a bunch of times ;)
    notebook = self.notebook

    # make the notebook pages:
    # in this case each notebook page (or panel) is its own class, they are too
    # large to keep all in one file. The function called is
    # the panel constructor (wx.Panel). They need to be passed the 'notebook' so
    # they know what their parent is.
    pickerPanel = wxc.picker.pickerPanel(notebook)
    mainPanel = main.mainPanel(notebook)
    numberPanel = numbering.numberingPanel(notebook)
    DateTimePanel = DateTime.DateTimePanel(notebook)
    errorPanel = errors.errorPanel(notebook)

    # add notebook pages to notebook:
    # 1st variable of 'AddPage' is previously described panel, 2nd
    # variable is text to be displayed
    notebook.AddPage(pickerPanel, 'Picker')
    notebook.AddPage(mainPanel, '- Main -')
    notebook.AddPage(numberPanel, 'Numbering')
    notebook.AddPage(DateTimePanel, 'Date and Time ')
    notebook.AddPage(errorPanel, 'Errors: 0    ')

    # list containing notebook images:
    # .ico seem to be more OS portable 
    il = wx.ImageList(16, 16)  # the (16, 16) is the size in pixels of the images
    img0 = il.Add(wx.Bitmap('art/icons/picker.ico', wx.BITMAP_TYPE_ICO))
    img1 = il.Add(wx.Bitmap('art/icons/main.ico', wx.BITMAP_TYPE_ICO))
    img2 = il.Add(wx.Bitmap('art/icons/numbering.ico', wx.BITMAP_TYPE_ICO))
    img3 = il.Add(wx.Bitmap('art/icons/date_time.ico', wx.BITMAP_TYPE_ICO))
    img4 = il.Add(wx.Bitmap('art/icons/errors.png', wx.BITMAP_TYPE_PNG))

    # set images to pages:
    # first assign image list created above to notebook:
    notebook.AssignImageList(il)
    # then assign each image in list to coresponding page.
    # the sharp-eyed will see you could use a loop for this,
    # but for maximum clarity/understanding I'm using the long way...
    notebook.SetPageImage(0, img0)
    notebook.SetPageImage(1, img1)
    notebook.SetPageImage(2, img2)
    notebook.SetPageImage(3, img3)
    notebook.SetPageImage(4, img4)

    # if this isn't called the notebook background color doesn't work right when switching
    # themes in XP.
    self.notebook.SetBackgroundColour(self.notebook.GetThemeBackgroundColour())