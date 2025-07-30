currentDir = pwd;
cd ..
cd(currentDir);
x0=380.7;
y0=-646.8;
yaw=-0.52;
v0=3;
acc=0.0;
gear=2;
steer=0.0;
slope=-0.2;
load('a_brake.mat');
load('a_thr.mat');
load('brake.mat');
load('thr.mat');
modelName='VehicleModel_SJTU';
run('control_simulink.m');
