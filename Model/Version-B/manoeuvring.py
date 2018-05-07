import math
import warnings

"""" Function to describe manoeuvring capabilities """

def manoeuverShip(ship, dt):

    # Ship characteristics
    L = ship.LBP
    B = ship.B
    Cb = ship.Cb

    # Current state of ship
    beta = math.radians(ship.drift)
    omega_z = math.radians(ship.headingChange)

    delta = math.radians(ship.rudderAngle)
    tau = ship.telegraphSpeed

    # update ship speed
    v = tau * ship.vmax * 1852 / 3600

    # Dimensionless factors
    try:
        omegadot_z = omega_z * L / v
    except ZeroDivisionError:
        return

    # Coefficients calculated
    hullCoeff = 0.5 * L / (B * Cb)

    # Coefficients estimated from [Artyszuk, 2016]
    k_11 = 0.056 # surge added mass coefficient
    k_22 = 1.004 # sway added mass coefficient
    r_z = 0.247 # ship's gyration dimensionless radius (Jz / (m * L^2))
    r_66 = 0.225 # added gyration dimensionless radius (m66 / (m * L^2))

    Yb = 0.0043
    Yw = 0.0260
    Nb = 0.0024
    Nw = -0.0630

    A_R = 0.0177 # dimensionless rudder ratio (Ar/(L*T))
    w = 0.326 # propeller wake fraction
    c_Th = 2.127 # Thrust coefficient propeller
    dCLda = 0.0385 # rudder lift coefficient derivative

    a_H = 0.6 # empirical amplification factor of (effective) rudder force due to hull‐rudder interaction
    c_Ry = 1.0 # empirical multiplier (≥1 or <1) to the rudder geometric local drift angle
    x_Reff = -0.5 # effective rudder longitudinal position

    checkInput(Yb, c_Ry, a_H, Yw, x_Reff, Nb, Nw)

    # Coefficient calculations
    R = hullCoeff * A_R * (1 - w)**2 * (1 + c_Th) * dCLda * (180/math.pi) * (1 + a_H)

    a_1H = (hullCoeff / (1 + k_22)) * (180 / math.pi) * Yb
    a_1R = - (R / (1 + k_22)) * (c_Ry / ((1 - w) * math.sqrt(1 + c_Th)))
    b_1H = - Yw * hullCoeff / (1 + k_22)
    b_1R = - a_1R * x_Reff
    b_1C = (1 + k_11) / (1 + k_22)
    c_1  = - R / (1 + k_22)

    a_2H = (hullCoeff / (r_z**2 + r_66**2)) * (180/math.pi) * Nb
    a_2R = - a_1R * x_Reff * (1 + k_22) / (r_z**2 + r_66**2)
    b_2H = Nw * hullCoeff / (r_z**2 + r_66**2)
    b_2R = a_1R * x_Reff**2 * (1 + k_22) / (r_z**2 + r_66**2)
    c_2 = - c_1 * x_Reff * (1 + k_22) / (r_z**2 + r_66**2)

    a_1 = a_1H + a_1R
    b_1 = b_1H + b_1R + b_1C
    a_2 = a_2H + a_2R
    b_2 = b_2H + b_2R

    # Calculate changes
    dBeta = (dt * v / L) * (a_1 * beta + b_1 * omegadot_z + c_1 * delta)
    dOmegadot_z = (dt * v / L) * (a_2 * beta + b_2 * omegadot_z + c_2 * delta)

    beta = .1*dBeta
    omegadot_z += dOmegadot_z
    omega_z = omegadot_z * v / L

    # Update and calculate new orientation of ship
    ship.headingChange = math.degrees(omega_z)
    ship.heading += ship.headingChange * dt

    ship.drift = math.degrees(beta)

    ship.course = ship.heading + ship.drift

    # Calculate new position
    ship.location[0] += dt * v * math.sin(math.radians(ship.course))
    ship.location[1] += dt * v * math.cos(math.radians(ship.course))
    ship.speed = v * 3600 / 1852

def checkInput(Yb, c_Ry, a_H, Yw, x_Reff, Nb, Nw):
    # Check if estimated values are between limits
    if Yb <= 0:
        warnings.warn("Yb' is less than or equal to 0")

    if c_Ry <= 0:
        warnings.warn("c_Ry is less than or equal to 0")

    if a_H <= 0:
        warnings.warn("a_H is less than or equal to 0")

    if Yw <= 0:
        warnings.warn("Yw' is less than or equal to 0")

    if x_Reff >= 0:
        warnings.warn("x_Reff' is more than or equal to 0, which means rudder is not configured correctly")

    if Nb <= 0:
        warnings.warn("Nb' is less than or equal to 0")

    if Nw >= 0:
        warnings.warn("Nw' is less than or equal to 0")