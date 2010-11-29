import gtk

def button_label_from_stock(stock,label_text):
    """
    creates an gtk.Alignment widget with stock icon and label
    """
    img=gtk.Image()
    img.set_from_stock(stock, gtk.ICON_SIZE_BUTTON)
    label=gtk.Label(label_text)
    box=gtk.HBox(spacing=2)
    box.pack_start(img,False)
    box.pack_start(label,False)
    alignment = gtk.Alignment(0.5, 0.5)
    alignment.add(box)
    return alignment, label
