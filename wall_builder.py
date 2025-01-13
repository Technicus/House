# Designing a house with build123d.

# Imports
from build123d import *
from ocp_vscode import show_all, show_object


# Set scale and unit conversion.
unit = {}
unit["scale"] = 1
unit["MM"] = 1
unit["CM"] = 10 * unit["MM"]
unit["M"] = 1000 * unit["MM"]
unit["IN"] = 25.4 * unit["MM"]
unit["FT"] = 12 * unit["MM"]
unit["THOU"] = unit["MM"] / 1000


# Set dimenstion for material
# Brick
brick_dimenstion = {
    "width": 9.625 * unit["IN"] * unit["scale"],
    "length": 15.125 * unit["IN"] * unit["scale"],
    "height": 7.625 * unit["IN"] * unit["scale"],
    "joint": 0.5 * unit["IN" * unit["scale"]]
}


# Define length of foundation segments around perimeter, initial origin, and offset.
foundation_wall = {}
# foundation_wall["wall"] = length * units * scale
foundation_wall["east"] = 188.000 * unit["IN"] * unit["scale"]
foundation_wall["east_north"] = 182.500 * unit["IN"] * unit["scale"]
foundation_wall["east_south"] = 65.000 * unit["IN"] * unit["scale"]
foundation_wall["north_east"] = 490.250 * unit["IN"] * unit["scale"]
foundation_wall["north_west"] = 65.000 * unit["IN"] * unit["scale"]
foundation_wall["south"] = 311.250 * unit["IN"] * unit["scale"]
foundation_wall["south_east"] = 50.250 * unit["IN"] * unit["scale"]
foundation_wall["south_west"] = 192.250 * unit["IN"] * unit["scale"]
foundation_wall["west_north"] = 117.000 * unit["IN"] * unit["scale"]
foundation_wall["west_south"] = 312.500 * unit["IN"] * unit["scale"]
# foundation_wall["brick_stack"] = count
foundation_wall["brick_stack"] = 11
# foundation_wall["height"] = brick_height + brick_joint_height * brick_stack * units * scale
foundation_wall["height"] = ((brick_dimenstion["height"] + brick_dimenstion["joint"]) * foundation_wall["brick_stack"]) * unit["scale"]
# Set references for wall lengths and include origin reference and apply scale.
# Changing origin_x|y|z will locate the the position of perimeter  
# Offset inversion to place foundation base negative z the length of wall height. 
# The intent of this offset is to put top plane of wall at z = 0.
# Although the foundation_wall[origin_z]" could set the z instead.
# foundation_wall["origin_x|y|z"] = x|y|z
foundation_wall["origin_x"] = 0.0
foundation_wall["origin_y"] = 0.0
foundation_wall["origin_z"] = 0.0
# foundation_wall[# "offset_x|y|z": x|y|z
foundation_wall["offset_x"] = 0.0
foundation_wall["offset_y"] = 0.0
foundation_wall["offset_z"] = (foundation_wall["height"] * -1) * unit["scale"]


# Define depth width and height of footing parameters.
footing_dimenstion = {}
footing_dimenstion["width"] = brick_dimenstion["width"] * 4
footing_dimenstion["height"] = footing_dimenstion["width"]
footing_dimenstion["depth"] = foundation_wall["offset_z"] - footing_dimenstion["height"]

# Set point references for foundation wall length and include origin reference.
# Counter clockwise from origin.
foundation_corners = [
  (foundation_wall["origin_x"],foundation_wall["origin_y"]),
  (foundation_wall["origin_x"] + foundation_wall["south_west"],foundation_wall["origin_y"]),
  (foundation_wall["origin_x"] + foundation_wall["south_west"],foundation_wall["origin_y"] + foundation_wall["south_east"]),
  (foundation_wall["origin_x"] + foundation_wall["south_west"] + foundation_wall["south"],foundation_wall["origin_y"] + foundation_wall["south_east"]),
  (foundation_wall["origin_x"] + foundation_wall["south_west"] + foundation_wall["south"],foundation_wall["origin_y"] + foundation_wall["south_east"] + foundation_wall["east"]),
  (foundation_wall["origin_x"] + foundation_wall["south_west"] + foundation_wall["south"] + foundation_wall["south_east"],foundation_wall["origin_y"] + foundation_wall["south_east"] + foundation_wall["east"]),
  (foundation_wall["origin_x"] + foundation_wall["south_west"] + foundation_wall["south"] + foundation_wall["south_east"],foundation_wall["origin_y"] + foundation_wall["south_east"] + foundation_wall["east"] + foundation_wall["east_north"]),
  (foundation_wall["origin_x"] + foundation_wall["south_west"] + foundation_wall["south"] + foundation_wall["south_east"] - foundation_wall["north_east"],foundation_wall["origin_y"] + foundation_wall["south_east"] + foundation_wall["east"] + foundation_wall["east_north"]),
  (foundation_wall["origin_x"] + foundation_wall["south_west"] + foundation_wall["south"] + foundation_wall["south_east"] - foundation_wall["north_east"],foundation_wall["origin_y"] + foundation_wall["south_east"] + foundation_wall["east"] + foundation_wall["east_north"] - foundation_wall["west_north"]),
  (foundation_wall["origin_x"],foundation_wall["origin_y"] + foundation_wall["south_east"] + foundation_wall["east"] + foundation_wall["east_north"] - foundation_wall["west_north"]),
  (foundation_wall["origin_x"],foundation_wall["origin_y"])
]


def wall(position, layout_line, width, height, build_offset, construction, material):
  # position = [x,y,z]
  # layout_line = list containing x,y coordinates of wall corners
  # width = width of wall
  # height =  height of wall
  # offset = determine inset | center | outset of wall along polyline
  # construction = brick, footing, framing, exterior, interior
  # material = define material used for wall construction
  # Eventually this should become a class with parameters that define different types of walls and include different position arrangements, this will remain basic for now.
  # Create wall_line as a part.
  with BuildPart(Plane.XY.offset(position[2])) as wall_part:
    # Create a sketch with z offset height of walls to contain drawing of wall layout_line.
    with BuildSketch(Plane.XY.offset(position[2])) as wall_sketch:
      # Start a line drawing for the layout_line of the wall.
      with BuildLine(Plane.XY.offset(position[2])) as wall_line:
        # Create a path of the wall with a polyline defined by layout_line.
        wall_line = Polyline(layout_line)
      # Turn foundation_line into a face.
      make_face()
      # Start a line drawing for the inside perimeter of the foundation walls.
      # with BuildLine(Plane.XY.offset(foundation_wall["offset_z"])) as foundation_line:
      with BuildLine(Plane.XY.offset(position[2])) as wall_line_offset:
        # Create the inside perimeter of the foundation with an offset from the outside perimeter.
        match build_offset: #"outset" | "center" | "inset"
          case "outset":
            wall_line_set = offset(
              wall_line,
              +width,
              kind=Kind.INTERSECTION)
          case "center":
            wall_line_set_outer = offset(
              wall_line,
              +width/2,
              kind=Kind.INTERSECTION)
            wall_line_set_inner = offset(
              wall_line,
              -width/2,
              kind=Kind.INTERSECTION)
          case "inset":
            wall_line_set = offset(
              wall_line,
              -width,
              kind=Kind.INTERSECTION)
          # case _:
          #   action-default
      # Subtract an offset to create the inner perimeter.
      make_face(mode=Mode.SUBTRACT)
      # make_face()
    # extrude(to_extrude=basement_perimeter_walls, amount=foundation_wall["height"])
    extrude(amount=height)
  return (wall_line, wall_line_offset, wall_part)


foundation_wall = wall(
  position = (0.0, 0.0, foundation_wall["offset_z"]), # position of first point as (x, y, z) coordinate
  layout_line = foundation_corners, # list of (x, y) coordinates that define path for wall
  width = brick_dimenstion["width"], # wall width
  height = foundation_wall["height"], 
  # build_offset = "outset", # defines position of wall relative to line as "outset" | "center" | "inset"
  build_offset = "inset", # defines position of wall relative to line as "outset" | "center" | "inset"
  construction = "brick", # meta information which will later be used to identify different methods for wall construction
  material = "cinder block" # additional meta information
  )


footing = wall(
  position = (0.0, 0.0, footing_dimenstion["depth"]), # position of first point as (x, y, z) coordinate
  layout_line = foundation_corners, # list of (x, y) coordinates that define path for wall
  width = footing_dimenstion["width"], # wall width
  height = footing_dimenstion["height"], 
  # build_offset = "center", # defines position of wall relative to line as "outset" | "center" | "inset"
  build_offset = "inset", # defines position of wall relative to line as "outset" | "center" | "inset"
  construction = "poor", # meta information which will later be used to identify different methods for wall construction
  material = "concrete" # additional meta information
  )

show_object(foundation_wall[0])
show_object(foundation_wall[1])
# show_object(foundation_wall[2])
show_object(footing[2])
# show_object(footing[2])

# show_object(foundation_line)
# show_object(foundation_line_inset)
# show_object(basement_perimeter_walls)

# show_object(foundation_sketch)
# show_all()