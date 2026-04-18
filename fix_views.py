import re

with open("core/views.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_conflict = False
conflict_blocks = [] # List of lists of lines
current_block = []

for line in lines:
    if line.startswith("<<<<<<< HEAD"):
        in_conflict = True
        conflict_blocks = [[]]
        continue
    
    if in_conflict:
        if line.startswith("======="):
            conflict_blocks.append([])
        elif line.startswith(">>>>>>>"):
            in_conflict = False
            # Take the LAST block
            if conflict_blocks:
                new_lines.extend(conflict_blocks[-1])
        else:
            conflict_blocks[-1].append(line)
    else:
        new_lines.append(line)

with open("core/views.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
