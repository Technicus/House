# Designing a Part in build123d
# https://build123d.readthedocs.io/en/latest/tutorial_design.html#designing-a-part-in-build123d
from build123d import *
from ocp_vscode import show_all


# units = { 
#   "MM": 1,
#   "CM": 10 * MM,
#   "M": 1000 * MM,
#   "IN": 25.4 * MM,
#   "FT": 12 * IN,
#   "THOU": IN / 1000
# }

MM = 1
CM = 10 * MM
M = 1000 * MM
IN = 25.4 * MM
FT = 12 * IN
THOU = IN / 1000


brick_dimenstion = {
    "width": 9.625 * IN,
    "length": 15.125 * IN,
    "height": 7.625 * IN,
    "joint": 0.5 * IN
}


foundation_wall = {
  #"wall": inches,
  "origin_x": 0.0,
  "origin_y": 0.0,
  "east": 188.000 * IN,
  "east_north": 182.500 * IN,
  "east_south": 65.000 * IN,
  "north_east": 490.250 * IN,
  "north_west": 65.000 * IN,
  "south": 311.250 * IN,
  "south_east": 50.250 * IN,
  "south_west": 192.250 * IN,
  "west_north": 117.000 * IN,
  "west_south": 312.500 * IN,
  "height": brick_dimenstion["height"] + brick_dimenstion["joint"] * 11
}


foundation_corner = [
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


with BuildPart() as foundation:
    # with BuildSketch(Plane.YZ) as foundation_sketch:
        with BuildLine() as foundation_line:
            # Create a perimeter of the foundation.
            foundation_perimeter = Polyline(foundation_corner)
            # Subtract an offset to create the block walls
            # foundation_wall_outline = offset(
            #     foundation_perimeter,
            #     -brick_dimenstion["width"],
            #     kind=Kind.INTERSECTION,
            #     mode=Mode.SUBTRACT,
            # )
    # extrude(amount=L)


show_all()