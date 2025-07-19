%% Make sure to have the add-on "ZMQ remote API"
%  running in CoppeliaSim
%% https://www.coppeliarobotics.com/helpFiles/en/zmqRemoteApiOverview.htm

%addpath('C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\programming\zmqRemoteApi\clients\matlab')

clear all
close all
clc
%
fprintf('Program started\n')
%
client = RemoteAPIClient();
sim = client.getObject('sim');

% When simulation is not running, ZMQ message handling could be a bit
% slow, since the idle loop runs at 8 Hz by default. So let's make
% sure that the idle loop runs at full speed for this program:
defaultIdleFps = sim.getInt32Param(sim.intparam_idle_fps);
sim.setInt32Param(sim.intparam_idle_fps, 0);

PioneerP3DX=sim.getObject('/PioneerP3DX');

%% Defining coppeliaSim client side parameters
np=200;
hd=50e-3;
tf=np*hd;
tc=0;
td=0;
id=1;
%
t=zeros(np,1);
xp=zeros(np,1);
yp=zeros(np,1);
zp=zeros(np,1);
fp=zeros(np,1);
%
robPosI=sim.getObjectPosition(PioneerP3DX,-1);
robOriI=sim.getObjectOrientation(PioneerP3DX,-1);
%
% Run a simulation in asynchronous mode:
sim.startSimulation();

t0=cputime;
while (tc<tf)
    tc=cputime-t0;
    %% Current sampling instant
    if (tc>td)
        t(id)=tc;
        %% Measuring
        robPos=sim.getObjectPosition(PioneerP3DX,-1);
        robOri=sim.getObjectOrientation(PioneerP3DX,-1);
        %% Saving robot pose
        xp(id)=cell2mat(robPos(1,1));
        yp(id)=cell2mat(robPos(1,2));
        zp(id)=cell2mat(robPos(1,3));
        fp(id)=cell2mat(robOri(1,3));
        %% Next sampling instant
        td=td+hd;
        id=id+1;
    end
end
%
sim.stopSimulation();
% If you need to make sure we really stopped:
while sim.getSimulationState() ~= sim.simulation_stopped
    pause(0.1);
end

%% Restore the original idle loop frequency:
sim.setInt32Param(sim.intparam_idle_fps, defaultIdleFps);

%% Plotting results
figure(1)
plot(t,xp,t,yp,t,zp,t,fp,'LineWidth',2),grid
legend('x_{p}(t)','y_{p}(t)','z_{p}(t)','\gamma_{p}(t)')
xlabel('t [s]')
%
figure(2)
axis equal
hold on
plot(xp,yp,'k:','LineWidth',2.0),grid
xlabel('x_{p}(t), m'),ylabel('y_{p}(t), m')
for i=1:round(length(xp)/20):length(xp)
    drawRobot(xp(i),yp(i),fp(i),0.04);
end
hold off

fprintf('Program ended\n');
