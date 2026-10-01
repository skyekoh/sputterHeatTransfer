"""Estimate water-side h for the two parallel drilled channels in outline.md.

Python 3, standard library only. Default: 7.25-inch channels, advertised 600 L/h total, equal split.
Examples (flow inputs are illustrative, not measured):
  python heat_transfer_coefficient.py
  python heat_transfer_coefficient.py --length-mm 100 --total-flow-lph 60
  python heat_transfer_coefficient.py --length-mm 100 --branch-flow-lph 20 40
  python heat_transfer_coefficient.py --length-mm 100 --advertised-flow

Geometry: two 1/4-inch circular channels; tubing OD 1/4 inch, wall 1/16 inch.
Water properties: approximate values at 20 C; no glycol or temperature correction.
Actual loop flow must be measured or obtained from a pump/system curve.
600 L/h is an advertised pump flow, NOT a predicted operating flow.
2.2 m shutoff head and advertised flow are not simultaneous operating conditions.

Correlations: fully developed circular laminar Nu=3.66 (constant wall temperature)
or 4.36 (constant heat flux); turbulent smooth-tube Gnielinski.
Developing-flow effects are flagged, not corrected. These idealized correlations
are reference estimates for the nonuniformly heated baseplate.
Reference:
https://ansyshelp.ansys.com/public/Views/Secured/MotorCAD/v252/en/Motor-CAD_UG/MotorCAD/topics/enclosedchannelconvectioncorrelation.html
"""
import argparse
import math

CHANNEL_LENGTH_MM = 7.25 * 25.4
CHANNEL_DIAMETER_M = 0.25 * 0.0254
TUBE_OD_M = 0.25 * 0.0254
TUBE_WALL_M = 0.0625 * 0.0254
TUBE_ID_M = TUBE_OD_M - 2 * TUBE_WALL_M
RHO = 998.2         # kg/m^3
MU = 1.002e-3      # Pa s
CP = 4182.0        # J/(kg K)
K_WATER = 0.598     # W/(m K)


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("Input must be finite and greater than zero.")
    return number


def calculate_channel(flow_lph, length_mm, wall_condition="temperature"):
    """Return SI results for one circular channel; flow is per channel."""
    if any(not math.isfinite(x) or x <= 0 for x in (flow_lph, length_mm)):
        raise ValueError("Flow and length must be finite and positive.")
    if wall_condition not in ("temperature", "flux"):
        raise ValueError("Wall condition must be temperature or flux.")
    diameter = CHANNEL_DIAMETER_M
    length = length_mm / 1000
    area = math.pi * diameter**2 / 4
    velocity = (flow_lph / 3_600_000) / area
    reynolds = RHO * velocity * diameter / MU
    prandtl = MU * CP / K_WATER
    warnings = []
    nu = None
    if reynolds < 2300:
        regime = "laminar"
        correlation = "Fully developed circular channel"
        nu = 3.66 if wall_condition == "temperature" else 4.36
        hydrodynamic_length = 0.05 * reynolds * diameter
        thermal_length = hydrodynamic_length * prandtl
        warnings.append(
            f"Laminar entrance estimates: hydraulic {hydrodynamic_length*1000:.1f} mm, "
            f"thermal {thermal_length*1000:.1f} mm."
        )
        if length < hydrodynamic_length or length < thermal_length:
            warnings.append(
                "Channel length is below an entrance-length estimate. Reported h is "
                "a fully developed reference, not a developing-flow prediction. "
                "Check upstream velocity development and heated entrance effects."
            )
    elif reynolds < 4000:
        regime = "transitional"
        correlation = "No correlation selected"
        warnings.append("Transition is uncertain; no single h is reported.")
    elif reynolds <= 1e6 and 0.5 <= prandtl <= 2000:
        regime = "turbulent"
        correlation = "Gnielinski, smooth circular channel"
        friction = (0.790 * math.log(reynolds) - 1.64)**-2
        nu = ((friction/8) * (reynolds-1000) * prandtl /
              (1 + 12.7 * math.sqrt(friction/8) * (prandtl**(2/3)-1)))
        if reynolds < 10000:
            warnings.append("Low turbulent Reynolds number: verify the actual flow regime.")
        if length / diameter < 10:
            warnings.append("L/D < 10: short-channel/entrance effects require refinement.")
    else:
        regime = "outside implemented correlation range"
        correlation = "No correlation selected"
        warnings.append("No h reported outside the implemented correlation range.")
    h = None if nu is None else nu * K_WATER / diameter
    wetted_area = math.pi * diameter * length
    return dict(velocity=velocity, reynolds=reynolds, prandtl=prandtl,
                regime=regime, correlation=correlation, nu=nu, h=h,
                wetted_area=wetted_area,
                resistance=None if h is None else 1/(h*wetted_area),
                warnings=warnings)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--length-mm", default=CHANNEL_LENGTH_MM, type=positive,
                        help="Default 184.15 mm (7.25 inches). Heated length of EACH channel in mm (equal lengths assumed).")
    flow = parser.add_mutually_exclusive_group()
    flow.add_argument("--total-flow-lph", type=positive,
                      help="Actual total baseplate flow in L/h; assumes equal splitting.")
    flow.add_argument("--branch-flow-lph", nargs=2, type=positive,
                      metavar=("CHANNEL_1", "CHANNEL_2"),
                      help="Individual channel flows in L/h for unequal splitting.")
    flow.add_argument("--advertised-flow", action="store_true",
                      help="Illustrative 600 L/h total scenario, not actual pump flow.")
    parser.add_argument("--wall-condition", choices=("temperature", "flux"),
                        default="temperature", help="Idealized laminar wall condition.")
    args = parser.parse_args()
    if args.branch_flow_lph:
        flows = args.branch_flow_lph
    else:
        total = args.total_flow_lph if args.total_flow_lph is not None else 600.0
        flows = [total/2, total/2]
    print("Water properties fixed at 20 C; smooth circular channels; single-phase water.")
    print(f"Channel diameter: {CHANNEL_DIAMETER_M*1000:.3f} mm")
    print(f"Tubing internal diameter from outline: {TUBE_ID_M*1000:.3f} mm")
    print("Tubing/fittings affect achievable flow; this script does not solve pump pressure drop.")
    print(f"Channel heated length: {args.length_mm:.2f} mm")
    if args.advertised_flow or (args.total_flow_lph is None and not args.branch_flow_lph):
        print("SCENARIO ONLY: 600 L/h advertised flow; actual loop flow remains unknown.")
    if not args.branch_flow_lph:
        print("Assumption: equal flow splitting between the two parallel channels.")
    for index, rate in enumerate(flows, 1):
        result = calculate_channel(rate, args.length_mm, args.wall_condition)
        print(f"\nChannel {index}: {rate:.3f} L/h")
        print(f"  Velocity: {result['velocity']:.4f} m/s")
        print(f"  Re: {result['reynolds']:.1f}; Pr: {result['prandtl']:.3f}")
        print(f"  Regime: {result['regime']}; correlation: {result['correlation']}")
        print(f"  Wetted area: {result['wetted_area']:.6g} m^2")
        if result["h"] is not None:
            print(f"  Nu: {result['nu']:.3f}")
            print(f"  h: {result['h']:.1f} W/(m^2 K)")
            print(f"  Convective resistance: {result['resistance']:.4f} K/W")
        for warning in result["warnings"]:
            print(f"  NOTE: {warning}")
    print("\nResistance uses each channel's wetted area and a representative bulk-water")
    print("temperature. It excludes solid/contact resistance and coolant warming.")


if __name__ == "__main__":
    main()
