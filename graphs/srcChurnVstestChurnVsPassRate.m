z=xlsread('200_200 data.xlsx')
[x y]=meshgrid(1:size(z,1),1:size(z,2));
zz=z(:);xx=x(:);yy=y(:);
X = [ones(size(xx)) xx yy];
b = regress(zz,X);

scatter3(xx,yy,zz);
hold on;
zfit = b(1) + b(2)*x + b(3)*y;
mesh(x,y,zfit);
xlabel('X');ylabel('Y');zlabel('Z');
hidden off;
hold off