# Python Script, API Version = V19 Beta

chord = 150
c2 = chord/2

TEy = 6.5/2
TEAR= 6
TEx = TEy*TEAR
TEc = -(c2-TEx)
x1 = 54.2658227848102
y1 = 3.24348409465260

LEy= 2
LEAR = 6
LEx = LEy*LEAR
LEc = c2-LEx
x2 = 63.7594931672704
y2 = 1.99599021741695


# Set Sketch Plane
sectionPlane = Plane.Create(Frame.Create(Point.Create(MM(0), MM(0), MM(0)), 
    Direction.Create(0, 1, 0), 
    Direction.DirX))
result = ViewHelper.SetSketchPlane(sectionPlane, None)
# EndBlock

# Sketch Leading Edge Ellipse
origin = Point2D.Create(MM(0), MM(LEc))
majorDir = -DirectionUV.DirV
minorDir = -DirectionUV.DirU
result = SketchEllipse.Create(origin, majorDir, minorDir, MM(LEx), MM(LEy))
# EndBlock

# Sketch Trailing Edge Ellipse
origin = Point2D.Create(MM(0), MM(TEc))
majorDir = -DirectionUV.DirV
minorDir = -DirectionUV.DirU
result = SketchEllipse.Create(origin, majorDir, minorDir, MM(TEx), MM(TEy))
# EndBlock

# Sketch Line - Top of LE to top of TE
start = Point2D.Create(MM(y1), MM(-x1))
end = Point2D.Create(MM(y2), MM(x2))
result = SketchLine.Create(start, end)
# EndBlock

# Sketch Line - Bot of LE to bot of TE
start = Point2D.Create(MM(-y1), MM(-x1))
end = Point2D.Create(MM(-y2), MM(x2))
result = SketchLine.Create(start, end)
# EndBlock

# Sketch Circle
plane = Plane.Create(Frame.Create(Point.Create(MM(0), MM(0), MM(0)), 
    Direction.DirY, 
    Direction.DirX))
result = ViewHelper.SetSketchPlane(plane)
origin = Point2D.Create(MM(0), MM(0))
result = SketchCircle.Create(origin, MM(2*chord))
# EndBlock

# Sketch Rectangle
point1 = Point2D.Create(MM(chord*10),MM(-chord*10))
point2 = Point2D.Create(MM(-chord*10),MM(-chord*10))
point3 = Point2D.Create(MM(-chord*10),MM(chord*10))
result = SketchRectangle.Create(point1, point2, point3)
# EndBlock

# Set Sketch Plane
mode = InteractionMode.Section
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# Detach Faces
selBodies = BodySelection.Create(GetRootPart().Bodies[0])
result = DetachFaces.Execute(selBodies)
# EndBlock

# Create Named Selection of Foil
sel = BodySelection.Create([GetRootPart().Bodies[2],
    GetRootPart().Bodies[4],
    GetRootPart().Bodies[3]])
sel.CreateAGroup("FoilBody")

