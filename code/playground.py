from shapely import wkt, Polygon, Point

polygon = Point(7,8)

print(type(polygon))
print(polygon)

polygon_str = polygon.wkt
print(polygon_str)

polygon_converted = wkt.loads(polygon_str)
print(type(polygon_converted))
print(polygon_converted)
