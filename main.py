import os

template = """
<kdenlivetitle LC_NUMERIC="C" duration="{frame}" height="1920" out="{frame}" width="1080">
 <item type="QGraphicsTextItem" z-index="0">
  <position x="439" y="1113">
   <transform>1,0,0,0,1,0,0,0,1</transform>
  </position>
  <content alignment="4" box-height="120" box-width="201" font="Segoe UI Black" font-color="255,255,0,255" font-italic="0" font-outline="6" font-outline-color="0,0,0,255" font-pixel-size="90" font-underline="0" font-weight="400" letter-spacing="0" line-spacing="0" shadow="0;#64000000;3;3;3" tab-width="80" typewriter="0;2;1;0;0">{text}</content>
 </item>
 <startviewport rect="0,0,1080,1920"/>
 <endviewport rect="0,0,1080,1920"/>
 <background color="0,0,0,0"/>
</kdenlivetitle>
"""

FRAME_RATE = 30
OUTPUT_DIR = "TITLES_FROM_PY"



def timestamp_to_milliseconds(timestamp):
    hours, minutes, seconds_milliseconds = timestamp.split(":")
    seconds, milliseconds = seconds_milliseconds.split(",")
    total_milliseconds = (int(hours) * 3600 + int(minutes) * 60 + int(seconds)) * 1000 + int(milliseconds)
    return total_milliseconds


def convert_timestamp_to_frame_count(timestamp_str):
    start, end = timestamp_str.split(" --> ")
    start_ms = timestamp_to_milliseconds(start)
    end_ms = timestamp_to_milliseconds(end)
    difference_ms = end_ms - start_ms
    frames = int(difference_ms * FRAME_RATE / 1000)
    return frames


def create_live_title(content, output_dir, index):
    filename = os.path.join(output_dir, f"live_title_{index}.kdenlivetitle")
    with open(filename, "w") as file:
        file.write(content)
    print(f"Created file: {filename} in {output_dir}")


def main():
    SUBS_FRAMES = []
    SUBS_TXT = []

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open("subs.srt", "r") as file:
        lines = file.readlines()  # Read all lines into a list
        SUBS_CNT = sum(1 for line in lines if line.strip().isdigit())
        left  = 0
        right = 3
        for i in range(SUBS_CNT):
            line_time_duration = lines[left:right][1].rstrip("\n")
            line_duration_frames = convert_timestamp_to_frame_count(line_time_duration)
            line_txt = lines[left:right][2].rstrip("\n")
            left  += 4
            right += 4
            content = template.format(frame=line_duration_frames, text=line_txt)
            create_live_title(content, OUTPUT_DIR, i)

        print(f"\nSUBS COUNT: {SUBS_CNT}")


main()