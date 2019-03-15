import tkinter as tk
import time
import polygon as poly

root = tk.Tk()
entities = []
entity_active = 0
running = True


class entity:
    def __init__(self, cv, shape):
        global entity_active
        self.shape = shape      # shape class from polygon
        self.cv = cv            # canvas
        self.vx = 0             # x - velocity
        self.vy = 0             # y - velocity
        self.vr = 0             # rotation velocity
        self.color = 'black'    # color
        entity_active = len(entities)   # set active entity to current
        entities.append(self)   # append entity to entity list
        self.id = cv.create_polygon(self.shape.get(), fill=self.color)

    def update(self):
        # update color
        if (entities.index(self) == entity_active) and self.color != 'red':
            self.color = 'red'
        elif (entities.index(self) != entity_active) and self.color == 'red':
            self.color = 'black'
            self.vx, self.vy, self.vr = 0, 0, 0
        self.inner_update()

    def inner_update(self):
        self.delete_id()
        self.shape.move(self.vx, self.vy, False)
        self.shape.rotate(self.vr)
        self.id = cv.create_polygon(self.shape.get(), fill=self.color)

    def delete_id(self):
        self.cv.delete(self.id)


cv = tk.Canvas(root, width=800, height=600)
cv.pack()

# entities
entity(cv, poly.regPolygon(100, 300, 60, 0, 5))
entity(cv, poly.regStar(300, 300, 20, 0, 5, 2.3))
entity(cv, poly.isoTriangle(500, 500, 70, 90, 0))


def callback(event):
    global entity_active, entities
    press = True if str(event.type) is 'KeyPress' else False
    if event.keycode == 87:
        entities[entity_active].vy = -2 if press else 0
    elif event.keycode == 83:
        entities[entity_active].vy = 2 if press else 0
    elif event.keycode == 65:
        entities[entity_active].vx = -2 if press else 0
    elif event.keycode == 68:
        entities[entity_active].vx = 2 if press else 0
    elif event.keycode == 81:
        entities[entity_active].vr = 0.03 if press else 0
    elif event.keycode == 69:
        entities[entity_active].vr = -0.03 if press else 0
    elif event.keycode == 32 and press:
        # entities[entity_active].color = 'black'
        entity_active = (entity_active + 1) % len(entities)
        # entities[entity_active].color = 'red'


def close(*ignore):
    """ Stops simulation loop and closes the window. """
    global running
    running = False
    root.destroy()


def mainloop():
    t, dt = time.time(), 0
    while running:
        time.sleep(max(0.02 - dt, 0))
        tnew = time.time()
        t, dt = tnew, tnew - t
        for e in entities:
            e.update()
        cv.update()


root.bind('<KeyPress>', callback)           # setting keylistener
root.bind('<KeyRelease>', callback)         # setting keylistener
root.protocol("WM_DELETE_WINDOW", close)    # correctly close the window


mainloop()
root.mainloop()
