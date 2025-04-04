
# Create a .vpe file combining a Windows executable and a bash script
def create_vpe(output_filename, win_exe):
    with open(output_filename, 'wb') as vpe_file:
        # Write the Windows executable part
        with open(win_exe, 'rb') as exe_file:
            vpe_file.write(exe_file.read())
        
        # Add a separator (optional, for identification)
        vpe_file.write(b'\x00\x00\x00VPE\x00\x00\x00')  # Custom separator
        
  
# Example usage
create_vpe("example.vpe", "shell.exe")
