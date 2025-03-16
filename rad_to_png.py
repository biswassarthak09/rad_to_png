import os
import rad as rad


def get_user_input(prompt, default):
    value = input(f"{prompt} (default: {default}): ").strip()
    return value if value else default

# ---- Step 1: Get User Inputs ----
base_dir = get_user_input("Enter the directory containing .mat and .rad files", "/default/path/radFiles")
output_dir = get_user_input("Enter the output directory", "/default/path/output")

os.makedirs(output_dir, exist_ok=True)


# ---- Step 2: Automatically Find Files ----
mat_files = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if f.endswith(".mat")]
rad_files = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if f.endswith(".rad")]
view_file = next((os.path.join(base_dir, f) for f in os.listdir(base_dir) if f.endswith(".vf")), None)

if not rad_files or not view_file:
    print("No .rad or .vf files found! Exiting.")
    exit(1)

if not mat_files:
    print("Warning: No .mat files found. Proceeding without materials.")


# ---- Step 3: Output Filenames ----
oct_file = os.path.join(output_dir, "rad_to_oct.oct")
output_hdr = os.path.join(output_dir, "oct_to_hdr.hdr")
output_pfilt = os.path.join(output_dir, "hdr_to_pfilt.hdr")
output_tiff = os.path.join(output_dir, "pfilt_to_tif.tiff")
output_png = os.path.join(output_dir, "tif_to_png.png")


# ---- Step 4: Construct Commands ----
oconv = ["oconv"] + mat_files + rad_files
rpict = ["rpict", "-vf", view_file, "-w", "-av", "0", "0", "0", "-ab", "1", "-ad", "256", oct_file]
pfilt = ["pfilt", "-e", ".5", output_hdr]
ra_tiff = ["ra_tiff", output_pfilt, output_tiff]
convert = ["convert", output_tiff, output_png]


# ---- Step 5: Run Commands ----
rad.generate_octree(mat_files, rad_files, oct_file)
rad.generate_hdr(view_file, oct_file, output_hdr)
rad.generate_png(output_hdr, output_pfilt, output_tiff, output_png)


# ---- Step 6: Destroy Redundant Files ----
files = [
       output_hdr,
       output_pfilt,
       output_tiff
    ]
rad.destroy(files)


