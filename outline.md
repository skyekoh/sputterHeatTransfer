# Outline

## Objective
For the purpose of this simulation, the goal is to determine the maximum operating power that keeps the magnets under the temperature of 80C.

## Operating Power Limit
The limiting factor for operating power is primarily the temperature of the magnetron magnets. Depending on the type, they lose their magnetism between 80C (176F) and 230C (446F). The neodynium magnets on McMaster-Carr state "N35SH and N38SH - These magnets are less likely than other grades to lose magnetic strength when exposed to temperatures up to 300F (149C)." Solving for the power under 80C then leaves us with a healthy factor of safety if we assume the use of N35SH / N38SH magnets.

## Assumptions
- Plasma envelops the entire cathode (sputtering source), but only concentrates where the magnetic field is strongest, which is what causes the "racetrack" pattern through the centre of the source. For the purpose of the simulation, the source of heat will only come from the racetrack on the target.
    - Fraction of total operating power that becomes heat around the racetrack TBD
- The resevoir can be assumed to be sufficiently large that the coolant entering the channels remains at a constant temperature, and the coolant returning does not change the reservoir temperature.

## Heat Path
### Source to Baseplate
- Copper/Aluminum Target
    - Magnets
        - Pole Piece
    - Aluminum Magnet Enclosure
        - Pole Piece
    - Pole Piece
        - Thermal Paste
            - Ceramic Insulator
                - Thermal Paste
                    - Baseplate
                        - Channel Walls
                            - Coolant
                        - Environment       

### Thermal Resistance Network
Useful visualization (finish this later)

## Hand Calculations
- Coolant temperature rise
- Pressure drop through channel / flow the pump can deliver
- Chanel heat-transfer coefficent from flow correlations
- Temperature rise through ceramic, interfaces, bnasepalte