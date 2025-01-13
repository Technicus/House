# Designing a house with build123d.

from build123d import *
from ocp_vscode import show_all


unit = {}
unit["MM"] = 1
unit["CM"] = 10 * unit["MM"]
unit["M"] = 1000 * unit["MM"]
unit["IN"] = 25.4 * unit["MM"]
unit["FT"] = 12 * unit["MM"]
unit["THOU"] = unit["MM"] / 1000


scale = 1


brick_dimenstion = {
    "width": 9.625 * unit["IN"],
    "length": 15.125 * unit["IN"],
    "height": 7.625 * unit["IN"],
    "joint": 0.5 * unit["IN"]
}


foundation_wall = {
  #"wall": inches,
  "origin_x": 0.0,
  "origin_y": 0.0,
  "east": 188.000 * unit["IN"],
  "east_north": 182.500 * unit["IN"],
  "east_south": 65.000 * unit["IN"],
  "north_east": 490.250 * unit["IN"],
  "north_west": 65.000 * unit["IN"],
  "south": 311.250 * unit["IN"],
  "south_east": 50.250 * unit["IN"],
  "south_west": 192.250 * unit["IN"],
  "west_north": 117.000 * unit["IN"],
  "west_south": 312.500 * unit["IN"],
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