clear a;
clear s;
a = arduino('COM7','uno','Libraries','Servo');
s = servo(a,'D4','MinPulseDuration',1.30e-3,'MaxPulseDuration',2.3e-3)



