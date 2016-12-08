data = load('/Users/Alvin/Desktop/MeasureRecord/timeMeasure/getClassStructureAndReplace.txt');
data2 = load('/Users/Alvin/Desktop/MeasureRecord/timeMeasure1/getClassStructureAndReplace.txt');

x = data(:,1);
y = data(:,2);

x1 = data2(:,1);
y1 = data2(:,2);

x_Points = [0:0.1:5];
degree = 5;

pf = polyfit(x,y,degree);
pf2 = polyfit(x1,y1,degree);
y_Points = polyval(pf,x_Points);
y1_Points = polyval(pf2,x_Points);
plot(x_Points,y_Points);
hold on;
plot(x_Points,y1_Points);
hold on;
plot(x,y,'o');
hold on;
plot(x1,y1,'o');
hold off;
title('Relation Between Time and File Size');
xlabel('File size (MB)');
ylabel('Time (sec)');
legend('First Set (100 samples)','Second Set (100 samples)');