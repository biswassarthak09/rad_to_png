import subprocess

def run_command_with_output(command, output_file=None):
    try:
        if output_file:
            with open(output_file, "wb") as out_file:
                subprocess.run(command, stdout=out_file, check=True)
        else:
            subprocess.run(command, check=True)
        print(f"Command executed successfully: {' '.join(command)}")
    except FileNotFoundError:
        print(f"Error: Command not found - {command[0]}")
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}\n{e}")

def generate_octree(mat_files, rad_files, oct_file):
    oconv = ["oconv"] + mat_files + rad_files
    run_command_with_output(oconv, oct_file)

def generate_hdr(view_file, oct_file, output_hdr):
    rpict = ["rpict", "-vf", view_file, "-w", "-av", "0", "0", "0", "-ab", "1", "-ad", "256", oct_file]
    run_command_with_output(rpict, output_hdr)

def generate_png(output_hdr, output_pfilt, output_tiff, output_png):
    pfilt = ["pfilt", "-e", ".5", output_hdr]
    ra_tiff = ["ra_tiff", output_pfilt, output_tiff]
    convert = ["convert", output_tiff, output_png]
    run_command_with_output(pfilt, output_pfilt)
    run_command_with_output(ra_tiff)
    run_command_with_output(convert)

def destroy(files):
    try:
        for f in files:
            if f: 
                subprocess.run(["rm", f], check=True)
                print(f"Deleted: {f}")
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")