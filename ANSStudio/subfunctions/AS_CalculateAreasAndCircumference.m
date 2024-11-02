function [avgArea, totArea, avgCirc, totCirc] = AS_CalculateAreasAndCircumference(dots)

nrPoints = size(dots, 2);
areas = [];
circs = [];

for k = 1:nrPoints
    radius = (dots(3, k) - dots(1, k))/2;
    area = pi*radius^2;
    circ = 2*pi*radius;
    areas = [areas area];
    circs = [circs circ];
end

avgArea = sum(areas)/nrPoints;
totArea = sum(areas);

avgCirc = sum(circs)/nrPoints;
totCirc = sum(circs);


end

