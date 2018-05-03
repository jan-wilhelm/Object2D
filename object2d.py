
FONT = pygame.font.SysFont('Arial', 30)

'''Enum class for directions

Values are LEFT, RIGHT, UP and DOWN and can be accessed via Direction.LEFT etc.
'''
class Direction:
    LEFT= (0,1)
    RIGHT= (0,-1)
    UP= (1,1)
    DOWN= (1,-1)

    def values():
        return [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]

class ClickType:
    LEFT_UP = 0
    LEFT_DOWN = 1
    RIGHT_UP = 2
    RIGHT_DOWN = 3
    

class ClickHandlerReceiver:
    
    def __init__(self):
    	self._click_handlers = []
        
        for i in range(0,4):
            self._click_handlers.append([])
            
        self._mouse_drag_handlers = []
        self._dragging = False
        
        
        
    ##################################################
    #####       MOUSE CLICK HANDLERS          #####
    ##################################################
    def getClickHandlers(self, clickType):
        return self._click_handlers[clickType]
    
    def addClickHandler(self, handler, clickType = ClickType.LEFT_UP, index = -1):
        index = max(index, min(len(self._click_handlers[clickType]), 0) )
        self._click_handlers[clickType].insert(index, handler)
        return self
        
    def removeClickHandler(self, handler):
        for i in range(len(self._click_handlers)):
            if handler in self.getClickHandlers(i):
                self.getClickHandlers(i).remove(handler)
        return self
    
    def click(self, pos, clickType):
        for handler in self.getClickHandlers(clickType):
            handler(self, pos, clickType)
            
            
    
    ##################################################
    #####        MOUSE DRAG HANDLERS          #####
    ##################################################
    def getMouseDragHandlers(self):
        return self._mouse_drag_handlers
    
    def addMouseDragHandler(self, handler, index = -1):
        index = max(index, min(len(self._mouse_drag_handlers), 0) )
        self._mouse_drag_handlers.insert(index, handler)
        return self
        
    def removeMouseDragHandler(self, handler):
        self._mouse_drag_handlers.remove(handler)
        return self

    def mouseDrag(self, pos):
        for handler in self.getMouseDragHandlers():
            handler(self, pos)
    
    
'''Highlevel abstract class representing any kind of shape or object that can be drawn or displayed in a 2d space

This is a parent class for all other 2d objects.
It also provides all the general mathematical and logical functions that can be overridden by inheriting classes.
'''
class Object2D(ClickHandlerReceiver):
    
    '''Constructor for any 2d object
    
    The corners should be tuples, lists or arrays of two elements. Example: corners = [(1,1), (-2,4), (0,2)]
    Color is 
    '''
    def __init__(self, corners, color = 'White'):
        '''
        ' (x,y) is the position of the object.
        ' The default color is white.
        '''
        ClickHandlerReceiver.__init__(self)
        listOfCorners = []
        for corner in corners:
            listOfCorners.append(list(corner))
        self._position = listOfCorners
        self._color = color
        self._draw_handlers = []
        self._animations = []
        self._rotation = 0
                  
    
    ##################################################
    #####           DRAW HANDLERS             #####
    ##################################################
    def addDrawHandler(self, handler, zindex = -1):
        zindex = max(zindex, min(len(self._draw_handlers), 0) )
        self._draw_handlers.insert(zindex, handler)
        return self
        
    def removeDrawHandler(self, handler):
        self._draw_handlers.remove(handler)
        return self
    
    def getDrawHandlers(self):
        return self._draw_handlers
            
            
    
    
    ##################################################
    #####           GETTER / SETTER           #####
    ##################################################
    def setColor(self, color):
        self._color = color
        
    def setPosition(self, position):
        self._position = list(position)
        
    def getColor(self):
        return self._color
    
    def getPosition(self):
        return self._position
    
    def getRotation(self):
        return self._rotation
            
            
    
    
    ##################################################
    #####              ANIMATIONS             #####
    ##################################################
    def getAnimations(self):
        return self._animations
    
    def addAnimation(self, animation):
        self._animations.append(animation)
        return self
    
    def stopAnimation(self, anim):
        self._animations.remove(anim)
    
    def stopAnimations(self):
        for animation in self.getAnimations():
            animation.stop()
        del self._animations[:]
        self._animations = []
        return self
    
    
    
    
    ##################################################
    #####            MOVE / SCALE             #####
    ##################################################
        
    def move(self, moveDirection, value):
        for i in range( len(self._position)):
            self._position[i][moveDirection[0]] -= moveDirection[1] * value
        return self
                
    def moveToPosition(self, pos):
        xs = []
        ys = []
        for point in self.getPosition():
            xs.append(point[0])
            ys.append(point[1])
        avg = [sum(xs) / len(xs), sum(ys) / len(ys)]
        deltas = []
        deltas.append(pos[0] - avg[0])
        deltas.append(pos[1] - avg[1])
        for i in range(len(self._position)):
            for j in range(2):
                self._position[i][j] += deltas[j]
        return self
        
    def scale(self, factor):            
        minX, minY = self.getPosition()[0]
        for point in self.getPosition()[1:]:
            if point[0] < minX:
                minX = point[0]
            if point[1] < minY:
                minY = point[1]
                
        minCoords = [minX, minY]     
        for i in range(len(self._position)):
            for j in range(2):
                delta = self._position[i][j] - minCoords[j]
                newCoord = minCoords[j] + (delta * factor)
                self._position[i][j] = newCoord
        return self
    
    def rotatePoint(centerPoint, point, angle):
        newPoint = [
            point[0] - centerPoint[0],
            point[1] - centerPoint[1]
        ]
        newPoint = [
            newPoint[0] * math.cos(angle) - newPoint[1] * math.sin(angle) ,
            newPoint[0] * math.sin(angle) + newPoint[1] * math.cos(angle)
        ]
        newPoint = [
            newPoint[0] + centerPoint[0],
            newPoint[1] + centerPoint[1]
        ]
        return newPoint
                
    def rotate(self, angle):
        self._rotation = angle
        xs = []
        ys = []
        for point in self.getPosition():
            xs.append(point[0])
            ys.append(point[1])
        center = [sum(xs) / len(xs), sum(ys) / len(ys)]
        
        angle = math.radians(angle)
        newPositions = []
        for corner in self.getPosition():
            newPositions.append( Object2D.rotatePoint(center, corner, angle) )
        self.setPosition(newPositions)
        return self
    
    def getBoundingRectangle(self):
        minX, minY = maxX, maxY = self.getPosition()[0]
        for point in self.getPosition()[1:]:
            if point[0] < minX:
                minX = point[0]
            elif point[0] > maxX:
                maxX = point[0]
            if point[1] < minY:
                minY = point[1]
            if point[1] > maxY:
                maxY = point[1]
                
        return [
            [minX, minY],
            [maxX, minY],
            [maxX, maxY],
            [minX, maxY],
        ]

    def draw(self, display):
        for handler in self.getDrawHandlers():
            handler(self, display)

        for ani in self.getAnimations():
            if not ani.running():
                self.stopAnimation(ani)
                continue
            elif (time.time() - ani.last) * 1000 >= ani.getInterval():
                ani.doTick()
                ani.last = time.time()
    
class Point( Object2D ):
    def __init__(self, x, y, color = 'White'):
        Object2D.__init__(self, [[x, y]], color = color)
        
    def draw(self, display):
        Object2D.draw(self, display)
        canvas.draw_point(self.getPosition()[0], self.getColor())
        
    def scale(self, factor):
        return
    
    def isPointInside(self, x, y):
        return [x, y] == self.getPosition()[0]

class Text( Object2D ):

    def __init__(self, pos, message, color = "white"):
        Object2D.__init__(self, [pos], color)
        self.message = message

    def draw(self, display):
        global FONT
        Object2D.draw(self, display)
        display.blit(FONT.render(self.message, False, (0, 0, 0)), self.getPosition()[0])

class Line( Object2D ):
    def __init__(self, points, color = 'White'):
        Object2D.__init__(self, points, color)
        
    def draw(self, display):
        Object2D.draw(self, display)
        
    def isPointInside(self, x, y, tolerance = 0):
        a  = self.getPosition()[0]
        b  = self.getPosition()[1]
        lengthca2  = (x - a[0])*(x - a[0]) + (y - a[1])*(y - a[1])
        lengthba2  = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
        if lengthca2 > lengthba2: return False
        dotproduct = (x - a[0])*(b[0] - a[0]) + (y - a[1])*(b[1] - a[1])
        if dotproduct <= 0.0: return False
        if abs(dotproduct*dotproduct - lengthca2*lengthba2) > (self.getLineWidth() + tolerance) * 62500: return False 
        return True

class Circle( Object2D ):
    """
    " Class for a circle.
    """
    def __init__(self, x, y, r, fillColor = "transparent"):
        Object2D.__init__(self, [[x, y]], color = fillColor)
        assert r > 0, "Radius must be greater than 0"
        self._radius = r
        
    def getRadius(self):
        return self._radius
    
    def getDiameter(self):
        return 2 * self._radius
    
    def setRadius(self, radius):
        self._radius = radius
    
    def getDisplayedDiameter(self):
        return 2 * self.getRadius()
        
    def draw(self, display):
        Object2D.draw(self, display)
    
    def scale(self, factor):
        self._radius *= factor
        
    def getArea(self):
        return math.pi * (self.getRadius() ** 2)
    
    def isPointInside(self, x, y):
        absX = x - self.getPosition()[0][0]
        absY = y - self.getPosition()[0][1]
        return absY ** 2 + absX ** 2 <= self.getRadius() ** 2
    
    def getBoundingRectangle(self):
        rad = self.getDisplayedDiameter() / 2
        x, y = self.getPosition()[0]
        return [
            [x - rad, y - rad],
            [x + rad, y - rad],
            [x + rad, y + rad],
            [x - rad, y + rad],
        ]

class Polygon( Object2D ):
    """
    " Class for a polygon.
    """
    def __init__(self, corners, fillColor = "transparent"):
        
        assert len(corners) >= 2, "Corners must be a list of at least 2 elements"
        Object2D.__init__(self, corners, color = fillColor)
        
        for corner in corners:
            assert len(corner) is 2, "Corner element must be a list of X,Y"
        
    def draw(self, display):
        Object2D.draw(self, display)
        pygame.draw.polygon(display, self.getColor(), self.getPosition())
        
    def isPointInside(self, x, y):
        n = len(self.getPosition())
        inside = False

        p1x,p1y = self.getPosition()[0]
        for i in range(n+1):
            p2x,p2y = self.getPosition()[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside
    
    def setCorner(self, idx, pos):
        p = self.getPosition()
        p[idx] = pos
        self.setPosition(p)
        
    def addToCorner(self, idx, coord, value):
        p = self.getPosition()
        p[idx][coord] += value
        self.setPosition(p)
    
class Image(Object2D):
    
    def __init__(self, imagePath, x, y):
        Object2D.__init__(self, [[x, y]])
        self.load(imagePath)
        
    def load(self, imagePath):
        self._path = imagePath
        self._img = pygame.image.load(imagePath)
        size = self._img.get_rect().size
        self._img = self._img.convert_alpha()
        self._width = size[0]
        self._height = size[1]
        return self
    
    def rotate(self, angle):
        self._rotation = angle
        self._img = pygame.transform.rotate(self._img, angle)
        self._img = self._img.convert_alpha()
        return self
        
    def getBounds(self):
        return (self._width, self._height)

    def getRealBounds(self):
        return self._img.get_rect().size

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height
    
    def getPath(self):
        return self._path
    
    def getImage(self):
        return self._img
        
    def scaleWithFactor(self, factor):
        newBounds = (int(float(self._width) * factor), int(float(self._height) * factor))
        return self.scale(newBounds)

    def scale(self, newBounds):
        self._width = newBounds[0]
        self._height = newBounds[1]
        self._img = pygame.transform.smoothscale(self._img, newBounds).convert_alpha()
        return self
    
    def isPointInside(self, x, y):
        exit("isPointInside is not implemented for Image class")
        
    def draw(self, display):
        Object2D.draw(self, display)
        pos = self.getPosition()[0]
        bounds = self.getRealBounds()
        display.blit(self._img, [pos[0] - bounds[0] / 2, pos[1] - bounds[1] / 2])

    def getBoundingRectangle(self):
        x, y = self.getPosition()[0]
        w = self.getWidth() / 2
        h = self.getWidth() / 2
        return [
            [x - w, y - h],
            [x + w, y - h],
            [x + w, y + h],
            [x - w, y + h]
        ]
    
class Animation():
    
    def doTick(self):
        if self._maxTicks > 0:
            if self._ticks == self._maxTicks:
                self.stop()
                return
        self._action(self, self._obj, self._ticks)
        self._ticks += 1
        
    def running(self):
        return self._running
        
    def stop(self):
        self._running = False
        
    def getTicks(self):
        return self._ticks
    
    def getObject(self):
        return self._obj
    
    def getMaxTicks(self):
        return self._maxTicks
    
    def getInterval(self):
        return self._interval
    
    def __init__(self, obj, interval, action, maxTicks = -1):
        self._maxTicks = maxTicks
        self._action = action
        self._running = True
        self._interval = interval
        self._obj = obj
        self._ticks = 0
        self.last = time.time()
        
class Frame:
    
    def __init__(self, name = "", width = 200, height = 200, fps = 60):        
        self._width = width
        self._height = height
        self._display = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self._key_downs = []
        self._key_up = []
        self._draw_handlers = []
        self._objects = []
        self._clock = pygame.time.Clock()
        self._event_handlers = {
            pygame.QUIT           : [],
            pygame.ACTIVEEVENT    : [],
            pygame.KEYDOWN        : [],
            pygame.KEYUP          : [],
            pygame.MOUSEMOTION    : [],
            pygame.MOUSEBUTTONUP  : [],
            pygame.MOUSEBUTTONDOWN: [],
            pygame.JOYAXISMOTION  : [],
            pygame.JOYBALLMOTION  : [],
            pygame.JOYHATMOTION   : [],
            pygame.JOYBUTTONUP    : [],
            pygame.JOYBUTTONDOWN  : [],
            pygame.VIDEORESIZE    : [],
            pygame.VIDEOEXPOSE    : [],
            pygame.USEREVENT      : []
        }
        self._fps = fps
        self._quit = False
        self.fpsval = 0
        
    def getObjects(self):
        return self._objects

    def addObject(self, obj, zindex = -1):
        zindex = max(zindex, min(len(self._objects), 0) )
        self._objects.insert(zindex, obj)
        return self
    
    def addObjects(self, objects):
        for obj in objects:
            self._objects.append(obj)
        return self
    
    def removeObject(self, obj):
        self._objects.remove(obj)
        return self
    
    
    def getWidth(self):
        return self._width
    
    def getHeight(self):
        return self._height
    
    def addDrawHandler(self, handler, zindex = -1):
        zindex = max(zindex, min(len(self._draw_handlers), 0) )
        self._draw_handlers.insert(zindex, handler)
        return self
        
    def removeDrawHandler(self, handler):
        self._draw_handlers.remove(handler)
        return self
    
    def getDrawHandlers(self):
        return self._draw_handlers
    
    def addEventHandler(self, eventType, handler, zindex = -1):
        zindex = max(zindex, min(len(self._event_handlers), 0))
        self._event_handlers[eventType].insert(zindex, handler)
        return self
    
    def getEventHandlers(self):
        return self._event_handlers

    def getEventHandlersForType(self, eventType):
        return self._event_handlers[eventType]

    def callHandlers(self, event):
        for handler in self.getEventHandlersForType(event.type):
            handler(event)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
            self.callHandlers(event)
        
    def start(self):
        while not self._quit:
            self.handleEvents()
            self.draw(self._display)
            pygame.display.update()
            self.fpsval = 1000.0 / self._clock.tick(self._fps)
        pygame.display.quit()
        pygame.quit()
        exit()

    
    def draw(self, display):
        for obj in self.getObjects():
            obj.draw(display)
            
        for handler in self.getDrawHandlers():
            handler(display)
    
    def getFps(self):
        return self._fps
                
class CircleWithImage(Image, Circle):
    
    def __init__(self, x, y, r, uri):
        Circle.__init__(self, x, y, r, "transparent")
        Image.__init__(self, uri, x, y)
        self.origBounds = self.getBounds()
        Image.scaleWithFactor(self, r / float(self.getWidth() / 2))
        
    def rotate(self, angle):
        return Image.rotate(self, angle)

    def getOriginalBounds(self):
        return self.origBounds
        
    def draw(self, display):
        Image.draw(self, display)

    def isPointInside(self, x, y):
        return Circle.isPointInside(self, x, y)
    
