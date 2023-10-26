import subprocess
import textwrap

async def gigachad_vid(text1,text2):
    text1 = textwrap.fill(text1,30)
    text2 = textwrap.fill(text2,30)
    # Define the first command as a list of strings
    command1 = ['ffmpeg','-y', '-i', 'combined.mp4','-deadline','realtime','-cpu-used','-4', '-vf',
                f"drawtext=fontfile='/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Medium.ttf':text='{text1}':fontsize=12:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0,7.33)'",
                '-c:a', 'copy', 'output.mp4']

    # Run the first command and save the output
    result1 = subprocess.run(command1)

    # Check for errors
    if result1.returncode == 0:
        command2 = ['ffmpeg','-y', '-i', 'output.mp4','-deadline','realtime','-cpu-used','-4', '-vf',
                    f"drawtext=fontfile='/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Medium.ttf':text='{text2}':fontsize=10:fontcolor=white:bordercolor=black:borderw=3:x=(w-text_w)/2:y=25:enable='between(t,7.33,100)'",
                    '-c:a', 'copy', 'output_final.mp4']

        # Run the second command and save the output
        result2 = subprocess.run(command2)

        # Check for errors
        if result2.returncode != 0:
            print(result2.stderr.decode())

async def ahmet2_vid(text1,text2):
    text1 = textwrap.fill(text1,30)
    text2 = textwrap.fill(text2,30)
    # Define the first command as a list of strings
    command1 = ['ffmpeg','-y', '-i', 'ahmet2.mp4','-deadline','realtime','-cpu-used','-4', '-vf',
                f"drawtext=fontfile='/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Medium.ttf':text='{text1}':fontsize=12:fontcolor=white:x=10:y=(h-text_h)/2:enable='between(t,2.79,4.45)'",
                '-c:a', 'copy', 'output_ahmet.mp4']

    # Run the first command and save the output_ahmet
    result1 = subprocess.run(command1)

    # Check for errors
    if result1.returncode == 0:
        command2 = ['ffmpeg','-y', '-i', 'output_ahmet.mp4','-deadline','realtime','-cpu-used','-4', '-vf',
                    f"drawtext=fontfile='/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Medium.ttf':text='{text2}':fontsize=10:fontcolor=white:bordercolor=black:borderw=3:x=(w-text_w)/3:y=25:enable='between(t,4.72,6.1)'",
                    '-c:a', 'copy', 'output_ahmet_2.mp4']

        # Run the second command and save the output_ahmet
        result2 = subprocess.run(command2)

        # Check for errors
        if result2.returncode != 0:
            print(result2.stderr.decode())

    command3 = ['ffmpeg','-y', '-i', 'output_ahmet_2.mp4','-deadline','realtime','-cpu-used','-4', '-vf',
                f"drawtext=fontfile='/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Medium.ttf':text='{text1}':fontsize=10:fontcolor=white:bordercolor=black:borderw=3:x=10:y=(h-text_h)/2:enable='between(t,6.5,10.5)'",
                '-c:a', 'copy', 'output_ahmet_3.mp4']

    # Run the second command and save the output_ahmet
    result3 = subprocess.run(command2)

    # Check for errors
    if result3.returncode != 0:
        print(result3.stderr.decode())
