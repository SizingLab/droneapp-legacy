from math import pi
from math import sqrt
import math

from sympy import Symbol, Derivative
from sympy import *


import numpy as np

# Load
M_load=5 # [kg] load mass

# Autonomy
t_h=17 # [min] time of hover fligth
k_maxthrust=1.3 # Ratio max thrust-hover

# Architecture of the multi-rotor drone (4,6, 8 arms, ...)
Narm=8 # [-] number of arm
Np_arm=1 # [-] number of propeller per arm (1 or 2)
Npro=Np_arm*Narm # [-] Propellers number

# Motor Architecture
Mod=1    # Chose between 0 for 'Direct Drive' or 1 for Gear Drive

#Maximum climb speed
V_cl=20 # [m/s] max climb speed
CD= 1.3 #[] drag coef
A_top=0.2 #[m^2] top surface. For a quadcopter: Atop=1/2*Lb^2+3*pi*Dpro^2/4

# Propeller characteristics
NDmax= 105000/60*.0254# [Hz.m] max speed limit (N.D max)

# Air properties
rho_air=1.18 # [kg/m^3] air density 


# MTOW
MTOW = 360. 

Mtotal=Symbol('Mtotal')
beta= Symbol('beta')
ND = Symbol('ND')
Tmot = Symbol('Tmot')
V_bat=Symbol('V_bat')
Ktmot = Symbol('Ktmot')
P_esc=Symbol('P_esc')
C_bat=Symbol('C_bat')
J=Symbol('J') # advance ratio 
D_ratio=Symbol('D_ratio') #  
Lbra=Symbol('Lbra') # 
Dout=Symbol('Dout')


# Hover, Climbing & Take-Off thrust 
# ---
Mtotal

Tpro_hover=Mtotal*(9.81)/Npro # [N] Thrust per propeller for hover
Tpro_max=Tpro_hover*k_maxthrust # [N] Max Thrust per propeller    
T_cl=(Mtotal*9.81+0.5*rho_air*CD*A_top*V_cl**2)/Npro # [N] Thrust per propeller for climbing

# Propeller characteristicss
# Ref : APC static

C_t_sta=4.27e-02 + 1.44e-01 * beta # Thrust coef with T=C_T.rho.n^2.D^4
C_p_sta=-1.48e-03 + 9.72e-02 * beta  # Power coef with P=C_p.rho.n^3.D^5

Dpro_ref=11*.0254 # [m] diameter
Mpro_ref=0.53*0.0283 # [kg] mass

# Ref: APC dynamics

C_t_dyn=0.02791-0.06543*J+0.11867*beta+0.27334*beta**2-0.28852*beta**3+0.02104*J**3-0.23504*J**2+0.18677*beta*J**2 # thrust coef for APC props in dynamics
C_p_dyn=0.01813-0.06218*beta+0.00343*J+0.35712*beta**2-0.23774*beta**3+0.07549*beta*J-0.1235*J**2 # power coef for APC props in dynamics

#Choice of diameter and rotational speed from a maximum thrust
Dpro=(Tpro_max/(C_t_sta*rho_air*ND**2))**0.5  # [m] Propeller diameter
n_pro_max=ND/Dpro # [Hz] Propeller speed 
n_pro_cl=sqrt(T_cl/(C_t_dyn*rho_air*Dpro**4)) # [Hz] climbing speed


# Propeller selection with take-off scenario

Wpro_max=n_pro_max*2*3.14 # [rad/s] Propeller speed

Mpro=Mpro_ref*(Dpro/Dpro_ref)**3 # [kg] Propeller mass

Ppro_max=C_p_sta*rho_air*n_pro_max**3*Dpro**5# [W] Power per propeller
Qpro_max=Ppro_max/Wpro_max # [N.m] Propeller torque

# Propeller torque& speed for hover

n_pro_hover=sqrt(Tpro_hover/(C_t_sta*rho_air*Dpro**4)) # [Hz] hover speed
Wpro_hover=n_pro_hover*2*3.14 # [rad/s] Propeller speed    

Ppro_hover=C_p_sta*rho_air*n_pro_hover**3*Dpro**5# [W] Power per propeller
Qpro_hover=Ppro_hover/Wpro_hover # [N.m] Propeller torque    

#V_bat_est=k_vb*1.84*(Ppro_max)**(0.36) # [V] battery voltage estimation

#Propeller torque &speed for climbing
Wpro_cl=n_pro_cl*2*3.14 # [rad/s] Propeller speed for climbing   

Ppro_cl=C_p_dyn*rho_air*n_pro_cl**3*Dpro**5# [W] Power per propeller for climbing
Qpro_cl=Ppro_cl/Wpro_cl # [N.m] Propeller torque for climbing   


# Motor selection & scaling laws
# ---
# Motor reference sized from max thrust
# Ref : AXI 5325/16 GOLD LINE
Tmot   # [N.m] Motor nominal torque per propeller

Tmot_ref=2.32  # [N.m] rated torque
Tmot_max_ref=85/70*Tmot_ref # [N.m] max torque
Rmot_ref=0.03  # [Ohm] resistance
Mmot_ref=0.575 # [kg] mass
Ktmot_ref=0.03 # [N.m/A] torque coefficient
Tfmot_ref=0.03 # [N.m] friction torque (zero load, nominal speed) 

Mmot=Mmot_ref*(Tmot/Tmot_ref)**(3/3.5) # [kg] Motor mass
Tmot_max=Tmot_max_ref*(Tmot/Tmot_ref)**(1) # [N.m] max torque

# Selection with take-off speed
Ktmot # [N.m/A] or [V/(rad/s)] Kt motor (RI term is missing)
Rmot=Rmot_ref*(Tmot/Tmot_ref)**(-5/3.5)*(Ktmot/Ktmot_ref)**(2)  # [Ohm] motor resistance
Tfmot=Tfmot_ref*(Tmot/Tmot_ref)**(3/3.5) # [N.m] Friction torque

# Hover current and voltage
Imot_hover = (Qpro_hover+Tfmot)/Ktmot # [I] Current of the motor per propeller
Umot_hover = Rmot*Imot_hover + Wpro_hover*Ktmot # [V] Voltage of the motor per propeller
P_el_hover = Umot_hover*Imot_hover # [W] Hover : output electrical power

# Take-Off current and voltage
Imot_max = (Qpro_max+Tfmot)/Ktmot # [I] Current of the motor per propeller
Umot_max = Rmot*Imot_max + Wpro_max*Ktmot # [V] Voltage of the motor per propeller
P_el_max = Umot_max*Imot_max # [W] Takeoff : output electrical power

# Climbing current and voltage
Imot_cl = (Qpro_cl+Tfmot)/Ktmot # [I] Current of the motor per propeller for climbing
Umot_cl = Rmot*Imot_cl + Wpro_cl*Ktmot # [V] Voltage of the motor per propeller for climbing
P_el_cl = Umot_cl*Imot_cl # [W] Power : output electrical power for climbing

#Gear box model
Nred=Tmot/Qpro_hover                        # Reduction ratio [-]
mg1=0.0309*Nred**2+0.1944*Nred+0.6389       # Ratio input pinion to mating gear
WF=1+1/mg1+mg1+mg1**2+Nred**2/mg1+Nred**2   # Weight Factor (ƩFd2/C) [-]
k_sd=1000                                   # Surface durability factor [lb/in]
C=2*8.85*Qpro_hover/k_sd                    # Coefficient (C=2T/K) [in3]
Fd2=WF*C                                    # Solid rotor volume [in3]
Mgear=Fd2*0.3*0.4535                        # Mass reducer [kg] (0.3 is a coefficient evaluated for aircraft application and 0.4535 to pass from lb to kg)
Fdp2=C*(Nred+1)/Nred                        # Solid rotor pinion volume [in3]
dp=(Fdp2/0.7)**(1/3)*0.0254                 # Pinion diameter [m] (0.0254 to pass from in to m)
dg=Nred*dp                                  # Gear diameter [m]
di=mg1*dp                                   # Inler diameter [m]


# Battery selection & scaling laws sized from hover
# --- 
# Battery
# Ref : MK-quadro
Mbat_ref=.329 # [kg] mass
#Ebat_ref=4*3.7*3.3*3600 # [J] energy
#Ebat_ref=220*3600*.329 # [J]
Cbat_ref= 3.400*3600#[A.s] 
Vbat_ref=4*3.7#[V] 
Imax_ref=170#[A]

V_bat # [V] Battery voltage

# Hover --> autonomy

Mbat= Mbat_ref*C_bat/Cbat_ref*V_bat/Vbat_ref # Battery mass
Imax=Imax_ref*C_bat/Cbat_ref #[A] max current

I_bat = (P_el_hover*Npro)/.95/V_bat #[I] Current of the battery
t_hf = .8*C_bat/I_bat/60 # [min] Hover time 


# ESC sized from max speed
# Ref : Turnigy K_Force 70HV 
Pesc_ref=3108 # [W] Power
Vesc_ref=44.4 #[V]Voltage
Mesc_ref=.115 # [kg] Mass

P_esc

P_esc_cl=P_el_cl*V_bat/Umot_cl # [W] power electronic power max climb
P_esc_max=P_el_max*V_bat/Umot_max # [W] power electronic power max thrust

Mesc = Mesc_ref*(P_esc/Pesc_ref) # [kg] Mass ESC
Vesc = Vesc_ref*(P_esc/Pesc_ref)**(1/3)# [V] ESC voltage

# Frame sized from max thrust
# ---

Mfra_ref=.347 #[kg] MK7 frame
Marm_ref=0.14#[kg] Mass of all arms

# Length calculation   
#    sep= 2*pi/Narm #[rad] interior angle separation between propellers
Lbra  #[m] length of the arm

# Static stress
# Sigma_max=200e6/4 # [Pa] Alu max stress (2 reduction for dynamic, 2 reduction for stress concentration)
Sigma_max=280e6/4 # [Pa] Composite max stress (2 reduction for dynamic, 2 reduction for stress concentration)

# Tube diameter & thickness
Dout # [m] outer diameter of the beam 
D_ratio # [m] inner diameter of the beam

# Mass
Marm=pi/4*(Dout**2-(D_ratio*Dout)**2)*Lbra*1700*Narm # [kg] mass of the arms

Mfra=Mfra_ref*(Marm/Marm_ref)# [kg] mass of the frame

# Thrust Bearing reference
# Ref : SKF 31309/DF
Life=5000                                                         # Life time [h]
k_bear=1
Cd_bear_ref=2700                                                  # Dynamic reference Load [N]
C0_bear_ref=1500                                                  # Static reference load[N]
Db_ref=0.032                                                      # Exterior reference diameter [m]
Lb_ref=0.007                                                      # Reference lenght [m]
db_ref=0.020                                                      # Interior reference diametere [m]
Mbear_ref=0.018                                                   # Reference mass [kg]

# Thrust bearing model"""
L10=(60*(Wpro_hover*60/2/3.14)*(Life/10**6))                     # Nominal endurance [Hours of working]
Cd_ap=(2*Tpro_hover*L10**(1/3))/2                                # Applied load on bearing [N]
Fmax=2*4*Tpro_max/2
C0_bear=k_bear*Fmax                                               # Static load [N]
Cd_bear=Cd_bear_ref/C0_bear_ref**(1.85/2)*C0_bear**(1.85/2)       # Dynamic Load [N]
Db=Db_ref/C0_bear_ref**0.5*C0_bear**0.5                           # Bearing exterior Diameter [m]
db=db_ref/C0_bear_ref**0.5*C0_bear**0.5                           # Bearing interior Diameter [m]
Lb=Lb_ref/C0_bear_ref**0.5*C0_bear**0.5                           # Bearing lenght [m]
Mbear=Mbear_ref/C0_bear_ref**1.5*C0_bear**1.5                     # Bearing mass [kg]


# Objective and Constraints sum up
# ---
if Mod==0:
    Mtotal_final = (Mesc+Mpro+Mmot+Mbear)*Npro+M_load+Mbat+Mfra+Marm
else:
    Mtotal_final = (Mesc+Mpro+Mmot+Mgear+Mbear)*Npro+M_load+Mbat+Mfra+Marm
