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

# Create basement_perimeter_walls as a part.
with BuildPart(Plane.XY.offset(foundation_wall["offset_z"])) as basement_perimeter_walls:
  # Create a sketch with z offset height of walls to contain drawing of wall outline.
  with BuildSketch(Plane.XY.offset(foundation_wall["offset_z"])) as foundation_sketch:
    # Start a line drawing for the outside perimeter of the foundation walls.
    # with BuildLine(Plane.XY.offset(foundation_wall["offset_z"])) as foundation_line:
    with BuildLine(Plane.XY.offset(foundation_wall["offset_z"])) as foundation_line:
      # Create a perimeter of the foundation with a polyline defined by foundation_corners.
      foundation_perimeter = Polyline(foundation_corners)
    # Turn foundation_line into a face.
    make_face()
    # Start a line drawing for the inside perimeter of the foundation walls.
    # with BuildLine(Plane.XY.offset(foundation_wall["offset_z"])) as foundation_line:
    with BuildLine(Plane.XY.offset(foundation_wall["offset_z"])) as foundation_line_inset:
      # Create the inside perimeter of the foundation with an offset from the outside perimeter.
      foundation_perimeter_inset = offset(
        foundation_perimeter,
        -brick_dimenstion["width"],
        kind=Kind.INTERSECTION)
    # Subtract an offset to create the inner perimeter.
    make_face(mode=Mode.SUBTRACT)
    # make_face()
  # extrude(to_extrude=basement_perimeter_walls, amount=foundation_wall["height"])
  extrude(amount=foundation_wall["height"])
  
show_object(foundation_line)
show_object(foundation_line_inset)
show_object(basement_perimeter_walls)

# show_object(basement_perimeter_walls)
# show_object(foundation_sketch)
# show_all()