numbits = 8;





resolution=2^10; 
%Polar Coordinates setting for endpoints of sector%
Thetanum=(0:(resolution-1))*2*pi;
Thetaden = resolution;
Thetaaxis = Thetanum/Thetaden;
x=cos(Thetaaxis);y=sin(Thetaaxis);

GreycodeMatrix=grey(numbits);
%Setting up polar coordinates index variables for the sectors%
Thetaindex=reshape(1:resolution,[],2^numbits);
Thetaindex=[Thetaindex;Thetaindex(1,[2:end 1])];

for Donutnum=1:numbits %Specifies ring number or radius%
    for Sectornum=1:2^numbits %Number of individual sectors%
        %X,Y coordinates of iner radius clockwise plus xX,Y coordinates of consecutive ring anticlockwise%
        Abscissa=[Donutnum*x(Thetaindex(:,Sectornum)) (Donutnum+1)*fliplr(x(Thetaindex(:,Sectornum)))];
        Ordinates = [Donutnum*y(Thetaindex(:,Sectornum)) (Donutnum+1)*fliplr(y(Thetaindex(:,Sectornum)))];
        Colorguide = GreycodeMatrix(Sectornum,Donutnum)*ones(1,3);
        Map=patch(Abscissa,Ordinates,Colorguide);
        set(Map,'lineStyle','-')
    end
end

axis equal



