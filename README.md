# ReadMe

Generate TI4 winner plaques for engraving

## Example outputs

 - ![Round1](./outputs/Rnd1.svg)
   - winner="MARSDEN",
   - date="13-08-2023",
   - winner_icon="Jol",
   - runner_up_icons=["Arborec", "Letnev", "Yssaril"],
   - output_file=OUTPUT_DIR / "Rnd1.svg"
 - ![Round2](./outputs/Rnd2.svg)
   - winner="FUSSEL",
   - date="15-10-2023",
   - winner_icon="Arborec",
   - runner_up_icons=["Creuss", "Xxcha", "Nekro"],
   - output_file=OUTPUT_DIR / "Rnd2.svg"
  
## Usage

Call script: `python generate.py -w DONKEY -d DD-MM-YYYY -i Arborec -r Creuss Xxcha Nekro -o filename` _or_ run GH action

N.B. You only need to use the first unique part of the name, e.g. Jol will match to Jol Nar.
