# Outline

## Objective
For the purpose of this simulation, the goal is to determine the maximum operating power that keeps the magnets under the temperature of 80C.

## Operating Power Limit
The limiting fator for operating power is primarily the temperature of the magnetron magnets. Depending on the type, they lose their magnetism between 80C (176F) and 230C (446F). The neodynium magnets on McMaster-Carr state "N35SH and N38SH - These magnets are less likely than other grades to lose magnetic strength when exposed to temperatures up to 300F (149C)." Solving for the power under 80C then leaves us with a healthy factor of safety if we assume the use of N35SH / N38SH magnets.

## Assumptions
- Plasma envelops the entire cathode (sputtering source), but we can define the concentration based on the observed confinement, or the "racetrack" pattern near the centre of the source. Using a magnetic film sheet is a good way to do this without operating the machine. For the purpose of the simulation, the source of heat will only come from the racetrack on the target.
    - 80% of total operating power that becomes heat around the racetrack, estimate based on literature.
        - Fraction will vary between designs based on geometry and other parameters.
- Assume the heat transfer between the cathode sheath and the baseplate to be negligble compared to source / baseplate.
- The resevoir can be assumed to be sufficiently large that the coolant entering the channels remains at a constant temperature, and the coolant returning does not change the reservoir temperature.

## Heat Path
### Source to Baseplate
*Each indentation represent a parallel path that heat can travel through from the top level*

- Copper/Aluminum Target
    - Magnets
        - Pole Piece
        - Aluminum Magnet Enclosure
    - Aluminum Magnet Enclosure
        - Pole Piece
        - Magnets
    - Pole Piece
        - Aluminum Magnet Enclosure
        - Magnets
        - Thermal Paste
            - Ceramic Insulator
                - Thermal Paste
                    - Baseplate
                        - Channel Walls
                            - Coolant
                        - Environment (atmosphere side, not vacuum side)
        - Aluminum Threded Rod
            - Gas Feedthrough Adapter
                - Electrical Tape
                    - Environment

### Thermal Resistance Network
Useful visualization (finish this later)

## Hand Calculations
- Coolant temperature rise
- Pressure drop through channel / flow the pump can deliver
- Chanel heat-transfer coefficent from flow correlations
- Temperature rise through ceramic, interfaces, baseplate


## Piping characteristics
- Piping OD: 1/4"
- Piping Wall Thickness: 1/16"
- Quick Connect Fittings: 1/4" Tube OD, 1/16" NPT Male
- Water Channel: Two parallel 1/4" Diameter Channels
- Pump Flowrate (Advertised): 600L/H (0.000166667m^3/s), Max lift height 2.2m