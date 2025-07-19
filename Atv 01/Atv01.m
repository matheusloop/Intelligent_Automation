close all

%% Parâmetros do PioneerP3DX (SI units)
D  = 195e-3;                        % Diâmetro das rodas
R  = D/2;                           % Raio das rodas
d  = 44.51e-3;                      % Distância do centro de massa ao eixo das rodas
L  = 0.1655;                        % Largura do robô / 2
mc = 13;                            % Massa do chassi
mw = 1.5;                           % Massa da roda + motor
m  = mc + 2*mw;                     % Massa total do robô
Ic = 130.7e-3;                      % Momento de inércia do chassi
Iw = 40e-3;                         % Momento de inércia da roda em torno do eixo
Im = 20e-3;                         % Momento de inércia da roda em torno do diâmetro
I  = Ic + mc*d^2 + 2*mw*L^2 + 2*Im; % Inércia total
Ra = 710e-3;                        % Resistência de armadura do motor
La = 0.66e-3;                       % Indutância da armadura
Vs = 12;                            % Tensão máxima de armadura
Kb = 23e-3;                         % Constante de força eletromotriz
Kt = 29e-3;                         % Constante de torque
N  = 38.3;                          % Razão da caixa de reduçã

%% Simulação da Dinâmica do PioneerP3DX
out = sim("simulacaoPioneerP3DX.slx");

%Entradas do modelo
time = out.Va_R.time;
Va_R = out.Va_R.signals.values;
Va_L = out.Va_L.signals.values;

%Saídas de Newton-Euler
NE_xa = out.NewtonEuller_xa.signals.values;
NE_ya = out.NewtonEuller_ya.signals.values;
NE_theta = out.NewtonEuller_theta.signals.values;

%Saídas de Lagrange
L_xa = out.Lagrange_xa.signals.values;
L_ya = out.Lagrange_ya.signals.values;
L_theta = out.Lagrange_theta.signals.values;

%% Plot das entrada
figure()
subplot(1,2,1)
plot(time, Va_R, "LineWidth",2);
title("Tensão de armadura - Roda Direita")
xlabel("tempo [s]");
ylabel("Tensão [V]");
grid on;

subplot(1,2,2)
plot(time, Va_L, "LineWidth",2);
title("Tensão de armadura - Roda Esquerda")
xlabel("tempo [s]");
ylabel("Tensão [V]");
grid on;

%% Plot das grandezas
figure
subplot(2,1,1)
yyaxis left
plot(time, NE_xa, 'r', 'DisplayName', 'x')
hold on
plot(time, NE_ya, 'b', 'DisplayName', 'y')
ylabel('x e y (m)')

yyaxis right
plot(time, NE_theta, 'm:','LineWidth', 2, 'DisplayName', '\theta')
ylabel('\theta (rad)')

xlabel('Tempo (s)')
title('Evolução das saídas no tempo - Newton-Euler')
legend('Location', 'best')
grid on

subplot(2,1,2)
yyaxis left
plot(time, L_xa, 'r', 'DisplayName', 'x')
hold on
plot(time, L_ya, 'b', 'DisplayName', 'y')
ylabel('x e y (m)')

yyaxis right
plot(time, L_theta, 'm:', 'LineWidth', 2, 'DisplayName', '\theta')
ylabel('\theta (rad)')

xlabel('Tempo (s)')
title('Evolução das saídas no tempo - Lagrange')
legend('Location', 'best')
grid on


%% Plot da trajetória - Separados
figure()
subplot(1,2,1)
hold on
plot(NE_xa, NE_ya, "LineWidth",2);
for i=1:round(length(NE_xa)/30):length(NE_xa)
    drawRobot(NE_xa(i),NE_ya(i),NE_theta(i),0.01, [i/length(NE_xa), 1-i/length(NE_xa), 0]);
end
drawRobot(NE_xa(end),NE_ya(end),NE_theta(end),0.01, [1, 0, 0]);
title("Tragetória Newton-Euller")
xlabel("x [m]");
ylabel("y [m]");
grid on;
hold off

subplot(1,2,2)
hold on
plot(L_xa, L_ya, "LineWidth",2);
for i=1:round(length(L_xa)/30):length(L_xa)
    drawRobot(L_xa(i),L_ya(i),L_theta(i),0.01, [i/length(L_xa), 1-i/length(L_xa), 0]);
end
drawRobot(L_xa(end),L_ya(end),L_theta(end),0.01, [1, 0, 0]);
title("Tragetória Lagrange")
xlabel("x [m]");
ylabel("y [m]");
grid on;
hold off

%% Plot da trajetória - Comparação
figure()
hold on
plot(NE_xa, NE_ya, "LineWidth",2);
plot(L_xa, L_ya, "m", "LineWidth",2);

for i=1:round(length(NE_xa)/30):length(NE_xa)
    drawRobot(NE_xa(i),NE_ya(i),NE_theta(i),0.01, [i/length(NE_xa), 1-i/length(NE_xa), 0]);
end
drawRobot(NE_xa(end),NE_ya(end),NE_theta(end),0.01, [1, 0, 0]);

for i=1:round(length(L_xa)/30):length(L_xa)
    drawRobot(L_xa(i),L_ya(i),L_theta(i),0.01, [i/length(L_xa), 1-i/length(L_xa), 0]);
end
drawRobot(L_xa(end),L_ya(end),L_theta(end),0.01, [1, 0, 0]);

hold off
title("Comparação")
xlabel("x [m]");
ylabel("y [m]");
grid on;
legend("Tragetória Newton-Euller", "Tragetória Lagrange")








