function XY = AS_PointsOnPerimeter(points)
XY = [];
degrees = 0:.0175:2*pi;
for k = 1:size(points, 2)
    centerX = points(1, k) + (points(3, k) - points(1, k))/2;
    centerY = points(2, k) + (points(4, k)-points(2, k))/2;
    radius = (points(3, k) - points(1, k))/2;
    x = centerX + radius.*cos(degrees);
    y = centerY + radius.*sin(degrees);
    XY = [XY; x' y'];
end
